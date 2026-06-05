#!/usr/bin/env python3
"""
ABA-ASP Runner for Causal Integration

This script provides utilities to run ABA-ASP solvers on causal predicate files.
It bridges the gap between Python data processing and Prolog/ASP-based ABA learning.

Author: Integration utilities
License: Same as ABA-ASP project
"""

import sys
import logging
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import json
import re
import tempfile

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

ABA_ASP_PATH = Path(__file__).parent.parent

# Check for swipl binary - try build tree, custom install, then system
SWIPL_BUILD = Path("/vol/bitbucket/fr920/swipl/build/src/swipl")
SWIPL_CUSTOM = Path("/vol/bitbucket/fr920/swipl/bin/swipl")


def _swipl_env(base_env: Optional[dict] = None) -> dict:
    """Return environment with SWI paths configured.

    Prefers the built tree layout where the runtime lives under `build/home`.
    """
    env = dict(base_env) if base_env is not None else os.environ.copy()

    if not SWIPL_PATH:
        return env

    swipl_path = Path(SWIPL_PATH)
    lib_dir = swipl_path.parent  # e.g., .../swipl/build/src
    env["LD_LIBRARY_PATH"] = f"{lib_dir}:" + env.get("LD_LIBRARY_PATH", "")

    # If the build tree has a dedicated SWI home (build/home), use it; otherwise fall back
    # to the parent directory so swipl can locate its boot files.
    home_candidate = swipl_path.parent.parent / "home"
    env["SWI_HOME_DIR"] = (
        str(home_candidate)
        if home_candidate.exists()
        else str(swipl_path.parent.parent)
    )

    return env


def _find_swipl() -> Optional[str]:
    """
    Find SWI-Prolog binary.
    
    Returns:
        Path to swipl executable or None if not found
    """
    # Try custom location
    custom_paths = [
        SWIPL_BUILD,
        Path("/vol/bitbucket/fr920/swipl/app/swipl"),
        SWIPL_CUSTOM,
    ]
    
    for path in custom_paths:
        if path.exists() and path.is_file():
            return str(path)
    
    # Try to find system swipl
    try:
        result = subprocess.run(
            ['which', 'swipl'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    return None


SWIPL_PATH = _find_swipl()

_EXAMPLE_ATOM_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\(\d+\)$")
_QUERY_RESULT_RE = re.compile(
    r"^ABA_QUERY_RESULT\s+(\S+)\s+(true|false)\s*$", re.IGNORECASE
)
_PROLOG_SUBPROCESS_BUFFER_S = 2.0


def _prolog_path_literal(path: Path) -> str:
    """Escape a filesystem path for use inside Prolog single-quoted atoms."""
    return str(path.resolve()).replace("\\", "/").replace("'", "''")


def _validate_example_atoms(examples: Sequence[str]) -> None:
    for example in examples:
        if not _EXAMPLE_ATOM_RE.match(example.strip()):
            raise ValueError(f"Invalid example atom: {example!r}")


def _run_prolog_script(
    script: str,
    *,
    cwd: Path,
    timeout_s: float,
) -> subprocess.CompletedProcess[str]:
    if not SWIPL_PATH:
        raise RuntimeError("SWI-Prolog is not available on this system")

    env = _swipl_env()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pl", delete=False) as tmp:
        tmp.write(script)
        tmp_path = Path(tmp.name)

    try:
        return subprocess.run(
            [SWIPL_PATH, "-q", "-f", "none", "-s", str(tmp_path)],
            capture_output=True,
            text=True,
            env=env,
            cwd=str(cwd.resolve()),
            timeout=timeout_s,
        )
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass


def _parse_query_result_lines(stdout: str) -> dict[str, bool]:
    results: dict[str, bool] = {}
    for line in stdout.splitlines():
        match = _QUERY_RESULT_RE.match(line.strip())
        if match:
            results[match.group(1)] = match.group(2).lower() == "true"
    return results


def _build_batch_query_script(aba_file: Path, examples: Sequence[str], timeout_s: float) -> str:
    aba_literal = _prolog_path_literal(aba_file)
    example_terms = ", ".join(f"'{ex}'" for ex in examples)
    return f"""
:- style_check(-discontiguous).
:- consult('{aba_literal}').

aba_query_entails(Goal, Timeout) :-
    catch(
        call_with_time_limit(Timeout, call(Goal)),
        time_limit_exceeded,
        fail
    ).

aba_emit_results([]).
aba_emit_results([Example|Rest]) :-
    term_string(Goal, Example),
    ( aba_query_entails(Goal, {timeout_s}) -> Status = true ; Status = false ),
    format('ABA_QUERY_RESULT ~w ~w~n', [Example, Status]),
    aba_emit_results(Rest).

:- aba_emit_results([{example_terms}]).
:- halt.
"""


def query_examples(
    aba_file: Path,
    examples: Sequence[str],
    timeout_s: float = 5.0,
) -> dict[str, bool]:
    """Query entailment of example atoms against a loaded ``.aba`` program.

    Loads ``aba_file`` (background knowledge or solution) in SWI-Prolog and
    tests each example goal with ``call_with_time_limit/2``. A per-example
    wall-clock cap is also enforced via the subprocess timeout.

    Returns:
        Mapping from each example string to whether Prolog succeeded on ``call/1``.
    """
    if not examples:
        return {}

    if not SWIPL_PATH:
        raise RuntimeError("SWI-Prolog is not available on this system")

    aba_file = Path(aba_file)
    if not aba_file.is_file():
        raise FileNotFoundError(f"ABA file not found: {aba_file}")

    examples_tuple = tuple(ex.strip() for ex in examples)
    _validate_example_atoms(examples_tuple)

    script = _build_batch_query_script(aba_file, examples_tuple, timeout_s)
    batch_timeout = timeout_s * len(examples_tuple) + _PROLOG_SUBPROCESS_BUFFER_S

    try:
        completed = _run_prolog_script(
            script,
            cwd=aba_file.parent,
            timeout_s=batch_timeout,
        )
    except subprocess.TimeoutExpired:
        logger.warning("Prolog batch query timed out for %s", aba_file)
        return {example: False for example in examples_tuple}

    if completed.returncode != 0:
        logger.warning(
            "Prolog query failed (rc=%s) for %s: %s",
            completed.returncode,
            aba_file,
            completed.stderr[:500],
        )
        return {example: False for example in examples_tuple}

    parsed = _parse_query_result_lines(completed.stdout)
    return {example: parsed.get(example, False) for example in examples_tuple}


class ABASPRunner:
    """Runner for ABA-ASP solvers on causal data.

    Supports both Prolog and ASP-based approaches.

    Example:
        >>> from pathlib import Path
        >>> runner = ABASPRunner()
        >>> if runner.prolog_available:
        ...     res = runner.run_prolog_aba_asp(
        ...         Path('example.bk.aba'),
        ...         positive_examples=['x2(1)','x2(3)'],
        ...         negative_examples=['x2(2)'],
        ...         learning_options={'folding_steps':'10'},
        ...     )
        ...     print(res.get('status'))  # doctest: +SKIP
        completed
    """
    
    def __init__(self, aba_asp_path: Optional[Path] = None):
        """
        Initialize ABA-ASP runner.
        
        Args:
            aba_asp_path: Path to aba_asp directory (default: parent of causal folder)
        """
        self.aba_asp_path = aba_asp_path or ABA_ASP_PATH
        self.prolog_available = self._check_prolog_available()
        self.clingo_available = self._check_clingo_available()
        
        if not self.prolog_available and not self.clingo_available:
            logger.warning("Neither SWI-Prolog nor Clingo found. Some features will be unavailable.")
    
    def _check_prolog_available(self) -> bool:
        """Check if SWI-Prolog is available."""
        if not SWIPL_PATH:
            logger.debug("SWI-Prolog not found in any standard location")
            return False

        try:
            env = _swipl_env()

            result = subprocess.run(
                [SWIPL_PATH, '--version'],
                capture_output=True,
                timeout=5,
                text=True,
                env=env,
            )
            if result.returncode == 0:
                logger.info(f"SWI-Prolog found at: {SWIPL_PATH}")
                return True
            logger.warning(f"SWI-Prolog found but version check failed: {result.stderr}")
            return False
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception) as e:
            logger.debug(f"SWI-Prolog check failed: {e}")
            return False
    
    def _check_clingo_available(self) -> bool:
        """Check if Clingo is available."""
        try:
            result = subprocess.run(
                ['clingo', '--version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def run_prolog_aba_asp(
        self,
        predicate_file: Path,
        positive_examples: List[str],
        negative_examples: List[str] = None,
        background_knowledge: Optional[Path] = None,
        output_file: Optional[Path] = None,
        learning_options: Optional[Dict[str, str]] = None,
        timeout_s: float = 120.0,
    ) -> Dict:
        """
        Run ABA-ASP using SWI-Prolog.
        
        Args:
            predicate_file: Path to .aba predicate file
            positive_examples: List of positive example predicates
            negative_examples: List of negative example predicates (optional)
            background_knowledge: Path to background knowledge file
            output_file: Path to save results
            learning_options: Dict of learning options (e.g., {'folding_mode': 'greedy', 'folding_steps': '20'})
            timeout_s: Wall-clock cap for the SWI-Prolog subprocess (matches YAML ``prolog_timeout_s``).
            
        Returns:
            Dictionary with results and metadata
        """
        if not self.prolog_available:
            raise RuntimeError("SWI-Prolog is not available on this system")
        
        logger.info(f"Running ABA-ASP with Prolog on {predicate_file.name}")
        
        # Build Prolog query
        pos_ex_str = ', '.join([f'{ex}' for ex in positive_examples])
        neg_ex_str = ', '.join([f'{ex}' for ex in (negative_examples or [])])
        
        predicate_file = Path(predicate_file)
        if not predicate_file.exists():
            raise FileNotFoundError(f"Predicate file not found: {predicate_file}")
        
        # Build learning options
        options_str = ""
        if learning_options:
            for key, value in learning_options.items():
                options_str += f"\n        :- set_lopt({key}({value}))."
        
        # Create Prolog command
        prolog_code = f"""
        % Load ABA-ASP library
        :- consult('{self.aba_asp_path / 'aba_asp.pl'}').

        % Keep output readable: BK generation can interleave clauses, which
        % triggers SWI-Prolog "discontiguous" warnings on consult.
        :- style_check(-discontiguous).
        
        % Set learning options{options_str}
        
        % Load predicates
        :- consult('{predicate_file.resolve()}').
        
        % Run ABA-ASP
        :- aba_asp(
            '{predicate_file.stem}',
            [{pos_ex_str}],
            [{neg_ex_str}]
        ).
        
        % Halt after execution
        :- halt.
        """
        
        logger.info(f"Prolog code (first 500 chars):\n{prolog_code[:500]}...")
        
        try:
            # Run Prolog
            # IMPORTANT: Feeding directives via stdin while also starting SWI-Prolog
            # with `-t halt` can cause it to exit before executing the provided code.
            # To make execution deterministic, write the generated program to a
            # temporary file and run SWI-Prolog with `-s`.
            env = _swipl_env()

            with tempfile.NamedTemporaryFile(mode='w', suffix='.pl', delete=False) as tmp:
                tmp.write(prolog_code)
                tmp_path = Path(tmp.name)

            try:
                process = subprocess.Popen(
                    [SWIPL_PATH, '-q', '-f', 'none', '-s', str(tmp_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env,
                    cwd=str(predicate_file.parent.resolve()),
                )

                try:
                    stdout, stderr = process.communicate(timeout=timeout_s)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate()
                    raise TimeoutError(
                        f"Prolog subprocess exceeded timeout_s={timeout_s}"
                    ) from None
            finally:
                try:
                    tmp_path.unlink(missing_ok=True)
                except Exception:
                    pass
            
            logger.info(f"Prolog execution completed with return code: {process.returncode}")
            
            if stdout:
                logger.info(f"Output:\n{stdout}")
            if stderr:
                logger.warning(f"Errors/Warnings:\n{stderr}")
            
            results = {
                'status': 'completed' if process.returncode == 0 else 'failed',
                'return_code': process.returncode,
                'stdout': stdout,
                'stderr': stderr,
                'predicate_file': str(predicate_file),
                'method': 'prolog',
            }
            
            if output_file:
                self._save_results(results, output_file)
            
            return results
            
        except TimeoutError:
            raise
        except Exception as e:
            logger.error(f"Error running Prolog: {e}")
            return {'status': 'error', 'error': str(e), 'method': 'prolog'}
    
    def run_clingo_asp(
        self,
        asp_file: Path,
        predicate_file: Path,
        output_file: Optional[Path] = None,
    ) -> Dict:
        """
        Run ABA-ASP using Clingo ASP solver.
        
        Args:
            asp_file: Path to .asp encoding file
            predicate_file: Path to predicate file
            output_file: Path to save results
            
        Returns:
            Dictionary with results
        """
        if not self.clingo_available:
            raise RuntimeError("Clingo is not available on this system")
        
        logger.info(f"Running ABA-ASP with Clingo")
        logger.info(f"  Encoding: {asp_file}")
        logger.info(f"  Predicates: {predicate_file}")
        
        try:
            # Run clingo
            cmd = [
                'clingo',
                str(asp_file),
                str(predicate_file),
                '--models=1',
                '-Wno-atom-undefined',
                '--verbose=3'
            ]
            
            logger.info(f"Command: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=60)
            
            logger.info(f"Clingo execution completed with return code: {process.returncode}")
            
            if stdout:
                logger.info(f"Output:\n{stdout[:1000]}...")
            if stderr:
                logger.warning(f"Errors/Warnings:\n{stderr}")
            
            results = {
                'status': 'completed' if process.returncode == 0 else 'failed',
                'return_code': process.returncode,
                'stdout': stdout,
                'stderr': stderr,
                'asp_file': str(asp_file),
                'predicate_file': str(predicate_file),
                'method': 'clingo',
            }
            
            if output_file:
                self._save_results(results, output_file)
            
            return results
            
        except subprocess.TimeoutExpired:
            logger.error("Clingo execution timed out")
            return {'status': 'timeout', 'method': 'clingo'}
        except Exception as e:
            logger.error(f"Error running Clingo: {e}")
            return {'status': 'error', 'error': str(e), 'method': 'clingo'}
    
    def _save_results(self, results: Dict, output_file: Path) -> None:
        """Save results to JSON file."""
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")
    
    def status(self) -> Dict[str, bool]:
        """Return availability status of solvers."""
        return {
            'prolog_available': self.prolog_available,
            'clingo_available': self.clingo_available,
        }


def run_discrete_example():
    """Run ABA-ASP on discrete causal example."""
    logger.info("=" * 70)
    logger.info("Running ABA-ASP on Discrete Causal Example")
    logger.info("=" * 70)
    
    predicate_file = Path(__file__).parent / 'outputs' / 'discrete_causal.aba'
    
    if not predicate_file.exists():
        logger.error(f"Predicate file not found: {predicate_file}")
        logger.error("Please run test_causal_integration.py first to generate predicates")
        return
    
    runner = ABASPRunner()
    status = runner.status()
    logger.info(f"Solver status: {status}")
    
    if status['prolog_available']:
        logger.info("\nAttempting Prolog-based execution...")
        try:
            results = runner.run_prolog_aba_asp(
                predicate_file,
                positive_examples=['disease(1)', 'symptom1(1)'],
                negative_examples=['disease(5)'],
                output_file=Path(__file__).parent / 'outputs' / 'discrete_results.json'
            )
            logger.info(f"Prolog results: {results['status']}")
        except Exception as e:
            logger.warning(f"Prolog execution failed: {e}")
    else:
        logger.warning("SWI-Prolog not available. Skipping Prolog-based execution.")
    
    if status['clingo_available']:
        logger.info("\nAttempting Clingo-based execution...")
        asp_file = Path(__file__).parent.parent / 'asp_engine.pl'
        if asp_file.exists():
            try:
                results = runner.run_clingo_asp(
                    asp_file,
                    predicate_file,
                    output_file=Path(__file__).parent / 'outputs' / 'discrete_clingo_results.json'
                )
                logger.info(f"Clingo results: {results['status']}")
            except Exception as e:
                logger.warning(f"Clingo execution failed: {e}")
        else:
            logger.warning(f"ASP engine file not found: {asp_file}")
    else:
        logger.warning("Clingo not available. Skipping Clingo-based execution.")


def run_continuous_example():
    """Run ABA-ASP on continuous causal example."""
    logger.info("\n" + "=" * 70)
    logger.info("Running ABA-ASP on Continuous Causal Example")
    logger.info("=" * 70)
    
    predicate_file = Path(__file__).parent / 'outputs' / 'continuous_causal.aba'
    
    if not predicate_file.exists():
        logger.error(f"Predicate file not found: {predicate_file}")
        logger.error("Please run test_causal_integration.py first to generate predicates")
        return
    
    runner = ABASPRunner()
    status = runner.status()
    
    if status['prolog_available']:
        logger.info("\nAttempting Prolog-based execution...")
        try:
            results = runner.run_prolog_aba_asp(
                predicate_file,
                positive_examples=['x0_bin0(1)', 'x1_bin1(1)'],
                negative_examples=['x0_bin4(1)'],
                output_file=Path(__file__).parent / 'outputs' / 'continuous_results.json'
            )
            logger.info(f"Prolog results: {results['status']}")
        except Exception as e:
            logger.warning(f"Prolog execution failed: {e}")
    else:
        logger.warning("SWI-Prolog not available.")


if __name__ == '__main__':
    logger.info("\n" + "=" * 70)
    logger.info("ABA-ASP Causal Runner")
    logger.info("=" * 70)
    
    runner = ABASPRunner()
    logger.info(f"\nSystem status:")
    logger.info(f"  SWI-Prolog: {'Available' if runner.prolog_available else 'Not found'}")
    logger.info(f"  Clingo: {'Available' if runner.clingo_available else 'Not found'}")
    
    # Run examples
    run_discrete_example()
    run_continuous_example()
    
    logger.info("\n" + "=" * 70)
    logger.info("Runner execution completed")
    logger.info("=" * 70)
