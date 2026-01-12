#!/usr/bin/env python3
"""
ArgCausalDisco -> ABA-ASP end-to-end integration script.

This script generates one discrete and one continuous dataset using
ArgCausalDisco's `data_utils`, converts them to ABA predicates with the
`aba_asp.utils.data_utils` helpers, and then attempts to run ABA-ASP
(Prolog or Clingo) on the resulting predicate files via the
`ABASPRunner` utility.

Outputs:
- Predicate files in `causal/outputs/argcausaldisco/`
- Solver logs/results (JSON) when solvers are available

Usage (from repo root, recommended env: `aba-env`):
    conda run -n aba-env python causal/argcausaldisco_integration.py
"""

from __future__ import annotations

import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# --- Path setup -----------------------------------------------------------
THIS_DIR = Path(__file__).resolve().parent
ABA_ASP_ROOT = THIS_DIR.parent
REPO_ROOT = ABA_ASP_ROOT.parent
ARGCAUSALDISCO_ROOT = REPO_ROOT / "ArgCausalDisco"

# Allow imports from aba_asp and ArgCausalDisco when running as a script
# Add repo root so "aba_asp" and "ArgCausalDisco" are importable as packages
for p in (REPO_ROOT, ARGCAUSALDISCO_ROOT, THIS_DIR):
    sys.path.insert(0, str(p))

# --- Imports that rely on the added paths --------------------------------
from aba_asp.utils.data_utils import (  # type: ignore
    dataframe_to_predicates,
    infer_variable_types,
    bin_continuous_variable,
    save_predicates_to_file,
)
from run_aba_asp import ABASPRunner  # type: ignore  # Import from same directory
from ArgCausalDisco.utils.data_utils import (  # type: ignore
    simulate_discrete_data,
    simulate_linear_continuous_data,
    simulate_dag,
)

# --- Logging --------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("argcausaldisco_integration")


@dataclass
class ExampleOutput:
    name: str
    predicates_path: Path
    positive_example: Optional[str]
    prolog_status: Optional[str]
    clingo_status: Optional[str]


def _ensure_output_dir() -> Path:
    """Create and return the output directory for this script."""
    out_dir = THIS_DIR / "outputs" / "argcausaldisco"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def pick_target_variable(df: pd.DataFrame, target_col: Optional[str] = None) -> Tuple[str, List[str], List[str]]:
    """Pick a target variable and split samples into pos/neg examples.

    Uses numeric sample IDs (1..N) to match BK format. Constructs target atoms
    as target_var(ID).

    Splitting strategy (aims to always produce both pos+neg when possible):
    - If values contain 0 and 1 (or are boolean-ish): pos = value != 0, neg = value == 0
    - Else if there are >=2 distinct values: neg = (value == min_value), pos = (value != min_value)

    If target_col is None, tries columns left-to-right and selects the first
    that yields both positive and negative examples.

    Args:
        df: DataFrame with causal data
        target_col: Column to use as target. If None, auto-selects.

    Returns:
        Tuple of (target_variable_name, positive_examples, negative_examples)
    """

    def _split_for_column(col: str) -> Tuple[List[str], List[str]]:
        series = df[col]
        values = series.to_list()
        unique_values = sorted({float(v) for v in values})

        positive_examples: List[str] = []
        negative_examples: List[str] = []

        if not unique_values:
            return positive_examples, negative_examples

        # Prefer 0-vs-nonzero if 0 is present (covers binary/boolean and many generated datasets)
        if 0.0 in unique_values:
            for idx in df.index:
                sample_id = idx + 1
                atom = f"{col}({sample_id})"
                if float(series.iloc[idx]) != 0.0:
                    positive_examples.append(atom)
                else:
                    negative_examples.append(atom)
            return positive_examples, negative_examples

        # Otherwise, use a deterministic value-vs-rest split
        if len(unique_values) >= 2:
            min_value = unique_values[0]
            for idx in df.index:
                sample_id = idx + 1
                atom = f"{col}({sample_id})"
                if float(series.iloc[idx]) == min_value:
                    negative_examples.append(atom)
                else:
                    positive_examples.append(atom)
            return positive_examples, negative_examples

        # Single-valued column -> cannot split
        return positive_examples, negative_examples

    # Candidate columns: either a requested target, or try all columns
    candidate_cols = [target_col] if target_col is not None else list(df.columns)

    chosen_target: Optional[str] = None
    chosen_pos: List[str] = []
    chosen_neg: List[str] = []

    for col in candidate_cols:
        if col is None or col not in df.columns:
            continue
        pos, neg = _split_for_column(col)
        if pos and neg:
            chosen_target, chosen_pos, chosen_neg = col, pos, neg
            break

        # If the user explicitly requested a target column, return even if split is degenerate
        if target_col is not None:
            chosen_target, chosen_pos, chosen_neg = col, pos, neg
            break

    # Fallback (should be rare): just use first column and nonzero-vs-zero
    if chosen_target is None:
        chosen_target = df.columns[0]
        chosen_pos, chosen_neg = _split_for_column(chosen_target)

    logger.info("Selected target variable: %s", chosen_target)
    logger.info("Positive examples: %d, Negative examples: %d", len(chosen_pos), len(chosen_neg))
    return chosen_target, chosen_pos, chosen_neg


def _convert_to_predicates(
    df: pd.DataFrame,
    var_types: Dict[str, str],
    name: str,
    output_dir: Path,
    continuous_bins: int,
) -> Path:
    """Convert a DataFrame to predicates and save to disk."""
    logger.info("Converting %s to predicates (bins=%s)...", name, continuous_bins)
    preds = dataframe_to_predicates(
        df,
        var_types=var_types,
        continuous_bins=continuous_bins,
        separate_samples=True,
        sample_separator="%",
    )
    dest = output_dir / f"{name}.aba"
    save_predicates_to_file(preds, dest)
    logger.info("Saved predicates to %s", dest)
    return dest


def generate_aba_background_knowledge(
    df: pd.DataFrame,
    var_types: Dict[str, str],
    name: str,
    output_dir: Path,
    exclude_cols: Optional[List[str]] = None,
    continuous_bins: int = 2,
    bin_strategy: str = "quantile",
) -> Path:
    """Build foldable ABA-ASP background knowledge and companion CSVs.

    - Uses numeric sample IDs (1..N) and reusable feature predicates.
    - Binary 0/1 variables emit only positive cases (x0(A) when value==1).
    - Non-binary discrete variables emit value-specific predicates (x0_val_7(A)).
    - Continuous variables are binned (quantile/uniform) into x0_binK(A).
    - Columns in ``exclude_cols`` are skipped (e.g., the learning target).
    - Outputs: ``{name}.bk.aba`` plus ``{name}.csv`` and ``{name}.binned.csv`` (if any continuous vars).
    """
    lines = []
    lines.append("% Background knowledge with foldable rules")
    lines.append("% Generated from ArgCausalDisco data")
    lines.append("")
    
    exclude = set(exclude_cols or [])

    # For each variable, create feature predicates reused across samples
    # Match autism-style: predicate(A) :- A=1. predicate(A) :- A=2. ...
    for col in df.columns:
        if col in exclude:
            lines.append(f"% Skipping excluded variable: {col}")
            lines.append("")
            continue
        lines.append(f"% Feature predicates for variable: {col}")
        vtype = var_types.get(col, "categorical")
        
        if vtype in ("categorical", "discrete"):
            # Check if this is a binary 0/1 variable
            unique_values = sorted(set(int(v) for v in df[col].tolist()))
            is_binary_01 = unique_values == [0, 1]
            
            if is_binary_01:
                # For binary 0/1 variables: only encode the true cases
                # x0(A) :- A=1.  (no need for x0_val_0)
                lines.append(f"% Binary variable (0/1): encoding only positive cases")
                for idx in df.index:
                    sample_id = idx + 1
                    value = int(df[col].iloc[idx])
                    if value == 1:  # Only add rules for true cases
                        lines.append(f"{col}(A) :- A={sample_id}.")
            else:
                # For non-binary discrete: use value-specific predicates
                for idx in df.index:
                    sample_id = idx + 1  # numeric ID
                    value = int(df[col].iloc[idx])
                    pred_name = f"{col}_val_{value}"
                    lines.append(f"{pred_name}(A) :- A={sample_id}.")
        else:
            # Continuous: bin using the shared utility (matches aba_asp.utils.data_utils)
            values = df[col].astype(float).to_numpy()
            binned, bin_ranges = bin_continuous_variable(
                values,
                n_bins=continuous_bins,
                strategy=bin_strategy,
            )
            lines.append(f"% Continuous binning: bins={continuous_bins}, strategy={bin_strategy}")
            lines.append(f"% Bin ranges: {bin_ranges}")
            for idx in df.index:
                sample_id = idx + 1
                bin_idx = int(binned[idx])
                pred_name = f"{col}_bin{bin_idx}"
                lines.append(f"{pred_name}(A) :- A={sample_id}.")
        lines.append("")
    
    # Write .bk.aba file and use basename with .bk suffix (matches examples)
    bk_path = output_dir / f"{name}.bk.aba"
    bk_path.write_text("\n".join(lines))
    logger.info("Generated ABA background knowledge (%d lines) at %s", len(lines), bk_path)
    
    # Also save the dataset as CSV for correspondence checking
    csv_path = output_dir / f"{name}.csv"
    # Add sample_id column to match the numeric IDs used in predicates
    df_with_ids = df.copy()
    df_with_ids.insert(0, 'sample_id', range(1, len(df) + 1))
    df_with_ids.to_csv(csv_path, index=False)
    logger.info("Saved dataset to %s", csv_path)
    
    # If there are continuous variables, also save a binned version for reference
    has_continuous = any(var_types.get(col, "categorical") == "continuous" for col in df.columns)
    if has_continuous:
        csv_binned_path = output_dir / f"{name}.binned.csv"
        df_binned = df.copy()
        
        # Add binned versions alongside original continuous values
        for col in df.columns:
            if col in exclude:
                continue
            vtype = var_types.get(col, "categorical")
            if vtype == "continuous":
                values = df[col].astype(float).to_numpy()
                binned, _ = bin_continuous_variable(
                    values,
                    n_bins=continuous_bins,
                    strategy=bin_strategy,
                )
                # Add as new column: x2_bin instead of x2
                bin_col_name = f"{col}_bin"
                df_binned[bin_col_name] = binned.astype(int)
        
        # Add sample_id and reorder columns to show original then binned
        df_binned.insert(0, 'sample_id', range(1, len(df_binned) + 1))
        df_binned.to_csv(csv_binned_path, index=False)
        logger.info("Saved binned dataset to %s", csv_binned_path)
    
    return bk_path


def _extract_learned_rules(predicate_file: Path) -> List[str]:
    """Extract rules *introduced by learning* from the ABA-ASP solution.

    ABA-ASP writes a solution file that typically contains both the original
    background knowledge rules and the learned additions (folded rules,
    introduced assumptions, contraries, etc.).

    This function returns the *delta*: solution rules minus BK rules.
    """

    def _parse_rule_lines(text: str) -> List[str]:
        out: List[str] = []
        for raw in text.split("\n"):
            line = raw.strip()
            if not line or line.startswith("%"):
                continue
            if ":-" in line or line.endswith("."):
                out.append(line)
        return out

    learned: List[str] = []
    
    # Derive base name correctly: for name.bk.aba -> base=name; for name.aba -> base=name
    stem = predicate_file.stem  # e.g., 'arg_disc.bk' or 'arg_disc'
    if stem.endswith('.bk'):
        base = stem[:-3]
    else:
        base = stem
    aba_asp_root = ABA_ASP_ROOT
    
    # Try different potential locations
    sol_candidates = [
        aba_asp_root / f"{base}.bk.sol.aba",
        aba_asp_root / f"{base}.sol.aba",
        predicate_file.parent / f"{base}.bk.sol.aba",
        predicate_file.parent / f"{base}.sol.aba",
    ]
    
    # Some ABA-ASP outputs include per-sample indicator rules in the solution
    # file (e.g., x0_val_2(A) :- A=7.). These are effectively data/BK facts and
    # are not useful to present as part of the learned hypothesis.
    _per_sample_indicator_re = re.compile(r"^[A-Za-z0-9_]+\(A\)\s*:-\s*A=\d+\.$")

    for solution_file in sol_candidates:
        if solution_file.exists():
            logger.debug("Found solution file: %s", solution_file)
            solution_rules = _parse_rule_lines(solution_file.read_text())
            bk_rules = _parse_rule_lines(predicate_file.read_text())

            bk_set = set(bk_rules)
            learned = [r for r in solution_rules if r not in bk_set]

            # Filter out per-sample indicator rules that can be copied/expanded
            # into the solution, to avoid misreporting BK/data as learned rules.
            learned = [r for r in learned if not _per_sample_indicator_re.match(r)]
            return learned
    
    logger.debug("No solution file found for %s in candidates: %s", base, sol_candidates)
    return learned


def _run_solvers(
    runner: ABASPRunner,
    predicate_file: Path,
    example_name: str,
    pos_atom: Optional[str],
    output_dir: Path,
    positive_examples: Optional[List[str]] = None,
    negative_examples: Optional[List[str]] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """Attempt Prolog run; return statuses (Clingo unused here)."""
    prolog_status: Optional[str] = None
    clingo_status: Optional[str] = None

    pos_list = positive_examples if positive_examples is not None else []
    neg_list = negative_examples if negative_examples is not None else []

    # Prolog run with nondeterministic folding mode (greedy too expensive for complex data)
    if runner.prolog_available:
        try:
            learning_options = {
                'folding_steps': '15',
            }
            logger.info("Using learning options (default nd folding): %s", learning_options)
            
            result = runner.run_prolog_aba_asp(
                predicate_file,
                positive_examples=pos_list,
                negative_examples=neg_list,
                output_file=output_dir / f"{example_name}_prolog.json",
                learning_options=learning_options,
            )
            prolog_status = result.get("status")
            logger.info("Prolog status for %s: %s", example_name, prolog_status)
            
            # Extract and display learned rules from generated solution file
            learned_rules = _extract_learned_rules(predicate_file)
            if learned_rules:
                logger.info("Learned rules for %s:", example_name)
                for rule in learned_rules[:15]:  # Show first 15 rules
                    logger.info("  %s", rule)
            else:
                logger.info("No learned rules found for %s (no solution file generated or learning failed)", example_name)
        except Exception as exc:  # pragma: no cover - runtime dependent
            prolog_status = f"error: {exc}"
            logger.warning("Prolog run failed for %s: %s", example_name, exc)
    else:
        logger.warning("SWI-Prolog not available; skipping Prolog run for %s", example_name)

    return prolog_status, clingo_status


def _generate_discrete_example(sample_size: int = 12, seed: int = 7) -> Tuple[pd.DataFrame, Dict[str, str], str]:
    """Generate a small discrete dataset using ArgCausalDisco's simulate_discrete_data."""
    logger.info("Generating discrete causal data using ArgCausalDisco.utils.data_utils.simulate_discrete_data...")
    edges = {(0, 1), (1, 2)}
    data = simulate_discrete_data(
        num_of_nodes=3,
        sample_size=sample_size,
        truth_DAG_directed_edges=edges,
        random_seed=seed,
    )
    columns = ["x0", "x1", "x2"]
    df = pd.DataFrame(data, columns=columns)
    var_types = {c: "categorical" for c in columns}
    description = "ArgCausalDisco discrete simulation: x0 -> x1 -> x2"
    logger.info("Generated discrete data shape=%s, head=\n%s", df.shape, df.head())
    return df, var_types, description


def _generate_continuous_example(sample_size: int = 16, seed: int = 13) -> Tuple[pd.DataFrame, Dict[str, str], str]:
    """Generate a small continuous dataset using ArgCausalDisco's simulate_linear_continuous_data."""
    logger.info("Generating continuous causal data using ArgCausalDisco.utils.data_utils.simulate_linear_continuous_data...")
    edges = {(0, 1), (1, 2)}
    data = simulate_linear_continuous_data(
        num_of_nodes=3,
        sample_size=sample_size,
        truth_DAG_directed_edges=edges,
        random_seed=seed,
        noise_type="gaussian",
    )
    columns = ["x0", "x1", "x2"]
    df = pd.DataFrame(data, columns=columns)
    var_types = {c: "continuous" for c in columns}
    description = "ArgCausalDisco continuous simulation: x0 -> x1 -> x2 (linear Gaussian)"
    logger.info("Generated continuous data shape=%s, head=\n%s", df.shape, df.head())
    return df, var_types, description


def _summarize_example(
    name: str,
    df: pd.DataFrame,
    var_types: Dict[str, str],
    predicate_path: Path,
    target_var: Optional[str],
    prolog_status: Optional[str],
) -> None:
    """Print compact stats similar to the simple ABA-ASP example."""
    lines = [ln.strip() for ln in predicate_path.read_text().splitlines() if ln.strip()]
    samples, n_vars = df.shape
    logger.info(
        "Stats for %s: samples=%s vars=%s var_types=%s predicates=%s",
        name,
        samples,
        n_vars,
        ", ".join(f"{k}:{v}" for k, v in var_types.items()),
        len(lines),
    )
    if target_var:
        logger.info("Target concept: %s", target_var)
    logger.info("First 3 predicate lines:\n%s", "\n".join(lines[:3]))
    logger.info("Prolog status: %s", prolog_status)


def run_examples() -> List[ExampleOutput]:
    """Generate discrete and continuous examples, convert, and run ABA-ASP."""
    output_dir = _ensure_output_dir()
    runner = ABASPRunner()

    logger.info("Solver availability: %s", runner.status())

    results: List[ExampleOutput] = []

    for name, generator, bins in [
        ("arg_disc", _generate_discrete_example, 4),
        ("arg_cont", _generate_continuous_example, 5),
    ]:
        logger.info("\n=== Running example: %s ===", name)
        df, var_types, description = generator()

        # Infer types to validate integration, but prefer the explicit ones
        inferred = infer_variable_types(df)
        logger.info("Inferred types: %s (overriding with explicit: %s)", inferred, var_types)

        # Generate background knowledge
        predicate_path = generate_aba_background_knowledge(
            df,
            var_types=var_types,
            name=name,
            output_dir=output_dir,
        )
        
        # Pick target variable and split pos/neg examples
        target_var, positive_examples, negative_examples = pick_target_variable(df)
        if target_var:
            logger.info("Target variable: %s", target_var)
            logger.info("Positive examples (%d): %s", len(positive_examples), positive_examples[:5])
            logger.info("Negative examples (%d): %s", len(negative_examples), negative_examples[:5])
        else:
            logger.warning("No target variable found for %s; solver runs may be skipped", name)
            positive_examples = []
            negative_examples = []

        prolog_status, clingo_status = _run_solvers(
            runner,
            predicate_path,
            example_name=name,
            pos_atom=None,
            output_dir=output_dir,
            positive_examples=positive_examples,
            negative_examples=negative_examples,
        )

        _summarize_example(
            name,
            df,
            var_types,
            predicate_path,
            target_var,
            prolog_status,
        )

        results.append(
            ExampleOutput(
                name=name,
                predicates_path=predicate_path,
                positive_example=target_var,
                prolog_status=prolog_status,
                clingo_status=clingo_status,
            )
        )

        logger.info("Summary for %s: %s", name, description)
        logger.info("Predicates saved to %s", predicate_path)
        logger.info("Prolog status: %s | Clingo status: %s", prolog_status, clingo_status)

    return results


def main() -> None:
    logger.info("Starting ArgCausalDisco -> ABA-ASP integration run...")
    outputs = run_examples()

    logger.info("\n=== Run complete. Artifacts ===")
    for item in outputs:
        logger.info(
            "%-8s -> %s | pos=%s | prolog=%s | clingo=%s",
            item.name,
            item.predicates_path,
            item.positive_example,
            item.prolog_status,
            item.clingo_status,
        )


if __name__ == "__main__":
    main()
