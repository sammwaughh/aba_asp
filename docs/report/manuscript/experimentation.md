# Experimentation

> Markdown mirror of `docs/report/manuscript/experimentation.tex`, for ChatGPT Project context.
> The `.tex` file remains the authoritative source; this mirror is not for compilation. Wording is
> preserved; LaTeX headings are converted to Markdown headings, mathematical notation is kept as
> inline LaTeX, `\cite{key}` is rendered as `[cite: key]` (references not resolved), and LaTeX
> tables are rendered as Markdown tables with all cell values preserved.

## Qualitative investigation: parent-set recovery

The first experimental step was a qualitative investigation of whether ABA Learning can recover simple local parent structure from controlled synthetic data. The current implementation converts a data table into ABA background predicates and runs ABA Learning for a chosen target variable. We first seek to explore and later establish more rigorously under what conditions the bodies of the learned target rules contain the true direct parents of the target. This is a first step towards exploring when and how ABA Learning can learn causality.

This is the first natural diagnostic to run. If a known synthetic graph has target variable \(x_2\), and the true direct parents of \(x_2\) are known, then the learned rules for \(x_2\) can be compared directly with that parent set. The investigation uses the three canonical three-node motifs:
\[
x_0 \rightarrow x_1 \rightarrow x_2
\qquad
x_0 \rightarrow x_1,\; x_0 \rightarrow x_2
\qquad
x_0 \rightarrow x_2 \leftarrow x_1,
\]
corresponding to a chain, a fork and a collider. These motifs separate three different local recovery problems: distinguishing a direct parent from an ancestor in the chain, distinguishing a direct parent from a sibling proxy in the fork, and recovering a two-parent mechanism in the collider. They are also the smallest motifs in which the usual causal-graph intuitions about paths, common causes and common effects arise [cite: glymour2019review, vowels2022d].

**Setup.**

Each experimental cell began from a small tabular dataset with one row per sample and one column per variable. The columns were \(x_0\), \(x_1\), and \(x_2\), and the row index was used as the sample identifier. For QL1 the tables were small handcrafted examples with four to five rows. For QL2 the tables were complete noiseless truth tables over the candidate explanatory variables \((x_0,x_1)\). For QL3 the tables were finite noisy samples with \(n=20\), generated from the specified chain, fork or collider mechanism. Thus the learner did not receive a graph directly. It received only a table of observed values, from which ABA background predicates and positive/negative examples were constructed.

All qualitative runs used target \(x_2\). The target column was excluded from the background knowledge, so the learner could not simply reuse the target as a feature. For each cell, the positive examples were atoms \(x_2(i)\) for samples in the positive target class, and the negative examples were atoms \(x_2(i)\) for the remaining samples. Binary variables were encoded as bare predicates such as \(x_0(A)\), categorical variables as value-specific predicates such as \(\texttt{x0\_val\_2(A)}\), and continuous variables as binned predicates such as \(\texttt{x0\_bin2(A)}\). Continuous cells used three uniform bins. The learner used a non-deterministic folding mode with a folding budget of 15.

For a cell with target \(t=x_2\), let \(P_t\) denote the true parent set in the generating graph and let \(R_t\) denote the set of base variables recovered from the bodies of non-trivial learned \(x_2\)-rules, after stripping value and bin suffixes. For example, \(\texttt{x1\_val\_2(A)}\) and \(\texttt{x1\_bin1(A)}\) both contribute \(x_1\) to \(R_t\). Parent-set recovery is evaluated using variable-level precision, recall, and \(F_1\) score:
\[
\mathrm{Prec}_{\mathrm{var}}=\frac{|R_t\cap P_t|}{|R_t|},
\qquad
\mathrm{Rec}_{\mathrm{var}}=\frac{|R_t\cap P_t|}{|P_t|},
\]
\[
F_{1,\mathrm{var}}
=
\frac{2\cdot \mathrm{Prec}_{\mathrm{var}}\cdot \mathrm{Rec}_{\mathrm{var}}}
{\mathrm{Prec}_{\mathrm{var}}+\mathrm{Rec}_{\mathrm{var}}},
\qquad
\]
When \(R_t=\emptyset\) and \(P_t\neq\emptyset\), recall, \(F_1\) is taken to be zero, while precision is undefined. An \(F_1\) score of \(1\) corresponds to exact parent-set recovery.

## QL1: initial motif-by-data-mode probe

The first run, QL1, used nine small handcrafted cells: three motifs crossed with three data modes. The data tables had four to five rows. This run was intended as a tiny, rapid diagnostic, not as a definitive benchmark. Our goal was to test the infrastructure setup to run later tests at scale. All nine cells solved. (Table: QL1 initial qualitative probe).

*Table: QL1 initial qualitative probe. Each cell reports the recovered base variables in learned \(x_2\)-rules and the resulting \(F_1\) score.*

| Motif | Mode | True parents | Recovered variables | \(F_1\) | Classification |
|---|---|---|---|---|---|
| Chain | Binary | \(\{x_1\}\) | \(\{x_0,x_1\}\) | 0.67 | Parent superset |
| Chain | Categorical-3 | \(\{x_1\}\) | \(\{x_0\}\) | 0.00 | Non-parent/proxy |
| Chain | Continuous-binned | \(\{x_1\}\) | \(\{x_0\}\) | 0.00 | Non-parent/proxy |
| Fork | Binary | \(\{x_0\}\) | \(\{x_0\}\) | 1.00 | Exact |
| Fork | Categorical-3 | \(\{x_0\}\) | \(\{x_0\}\) | 1.00 | Exact |
| Fork | Continuous-binned | \(\{x_0\}\) | \(\{x_0\}\) | 1.00 | Exact |
| Collider | Binary | \(\{x_0,x_1\}\) | \(\{x_0,x_1\}\) | 1.00 | Exact |
| Collider | Categorical-3 | \(\{x_0,x_1\}\) | \(\{x_0\}\) | 0.67 | Parent subset |
| Collider | Continuous-binned | \(\{x_0,x_1\}\) | \(\{x_0\}\) | 0.67 | Parent subset |

The fork motif was recovered exactly in all three encodings. However, this apparent success is not by itself strong evidence of causal parent recovery because in the fork fixture the true parent of \(x_2\) is \(x_0\). A learner biased towards the first variable would therefore also appear correct. This implementation artefact motivates a later experiment swapping variable columns to account for this. The chain cells also exposed this concern: when the true parent was \(x_1\), the categorical and continuous cells recovered \(x_0\), which is an ancestor but not the direct parent. The binary chain cell recovered both \(x_0\) and \(x_1\), giving full recall but including a redundant ancestor. The collider motif was recovered exactly in the binary setting but only partially in the categorical and continuous settings, where the learned rules cited \(x_0\) but not \(x_1\).

This run exposed two design problems. First, the handcrafted table, as set up, may conflate true parent recovery with a possible preference for \(x_0\). Second, these tables do not guarantee that the intended parent rule is the only strong explanation of the examples. To address these limitations we conducted a stricter minimal baseline.

## QL2: complete truth-table baseline

QL2 was intended to address these two weaknesses in QL1. QL2 therefore replaced the QL1 tables with complete, noiseless truth tables. I forgot to actually implement the swapping of \((x_0,x_1)\) so we have duplicate data unnecessarily. This will be done in the immediate future and seek to address the first stated weakness of QL1.

QL2 used six cells: three motifs crossed with two data modes, binary and categorical-3. The target was \(x_2\) throughout. The binary cells enumerated all assignments of \((x_0,x_1)\in\{0,1\}^2\), repeated twice, giving \(2^2\times 2=8\) rows. For the categorical-3 cells, the table was intended as a complete factorial over the two explanatory variables \((x_0,x_1)\in\{0,1,2\}^2\). Thus all nine value combinations appeared, and each was repeated once, giving \(18\) rows. The target \(x_2\) was then computed deterministically from these categorical values. In the categorical chain, \(x_2=x_1\), so the positive class \(x_2=2\) occurs exactly when \(x_1=2\), independently of \(x_0\). The intended learned rule is therefore value-specific, \(x_2(A)\leftarrow \texttt{x1\_val\_2(A)}\), which contributes the base variable \(x_1\) to the recovered parent set. In the categorical fork, \(x_2=x_0\), so the intended rule is \(x_2(A)\leftarrow \texttt{x0\_val\_2(A)}\). In the categorical collider, \(x_2=\max(x_0,x_1)\). Since positives are defined by \(x_2=2\), a row is positive whenever either \(x_0=2\) or \(x_1=2\). At the level of value predicates, the natural parent-aligned representation is therefore disjunctive, for example by rules using \(\texttt{x0\_val\_2(A)}\) and \(\texttt{x1\_val\_2(A)}\). Both variables are true parents because changing either \(x_0\) or \(x_1\) can change whether \(x_2\) reaches category \(2\).

*Table: QL2 complete truth-table baseline. \(F_1\) measures variable-level overlap between recovered base variables and the true parent set.*

| Cell | Mode | True parents | Recovered | Precision | Recall | \(F_1\) | Outcome |
|---|---|---|---|---|---|---|---|
| Chain | Binary | \(\{x_1\}\) | \(\{x_1\}\) | 1.00 | 1.00 | 1.00 | Solved |
| Fork | Binary | \(\{x_0\}\) | \(\{x_0\}\) | 1.00 | 1.00 | 1.00 | Solved |
| Collider | Binary | \(\{x_0,x_1\}\) | \(\emptyset\) | n/a | 0.00 | 0.00 | No solution |
| Chain | Categorical-3 | \(\{x_1\}\) | \(\{x_0\}\) | 0.00 | 0.00 | 0.00 | Solved |
| Fork | Categorical-3 | \(\{x_0\}\) | \(\{x_0\}\) | 1.00 | 1.00 | 1.00 | Solved |
| Collider | Categorical-3 | \(\{x_0,x_1\}\) | \(\{x_0\}\) | 1.00 | 0.50 | 0.67 | Solved |

The binary chain and binary fork cells recovered the true parent exactly. The learned target rules were:
\[
x_2(A) \leftarrow x_1(A)
\]
for the chain, and
\[
x_2(A) \leftarrow x_0(A)
\]
for the fork. In the binary chain, \(x_0\) is no longer a defensible proxy for \(x_2\), and the learner recovered \(x_1\). Thus QL2 provides evidence against a simple explanation in which the learner always prefers \(x_0\).

The binary collider returned no solution. This is a negative result for the configured learner, but it is not evidence that no parent-aligned rule exists. In the generated truth table, the conjunctive rule
\[
x_2(A) \leftarrow x_0(A),x_1(A)
\]
covers exactly the positive rows and rejects the negative rows. The failure therefore indicates that the current representation and non-deterministic folding configuration did not find the available two-parent rule. This is most relevant for collider-like targets, where the intended mechanism requires a multi-literal rule body rather than a single parent predicate.

The categorical fork recovered the correct parent:
\[
x_2(A) \leftarrow \texttt{x0\_val\_2}(A).
\]

The categorical collider recovered only \(x_0\), giving precision \(1.00\), recall \(0.50\), and \(F_1=0.67\). This is a parent-subset result: the recovered variable is a true parent, but the second true parent \(x_1\) was missed. The categorical chain incorrectly recovered the ancestor \(x_0\) instead of the direct parent \(x_1\) of \(x_2\).

QL2 gives a more reliable baseline than QL1. It shows that some QL1 failures were caused by weak dataset design: the binary recovered a parent superset in QL1 but exactly recovered the set in QL2 once the complete truth table was used. It also shows that ideal noiseless data are not sufficient for robust parent-set recovery. The mean \(F_1\) over the six QL2 cells was approximately \(0.61\). Binary chain and fork recovery were exact, but the binary collider failed, the categorical chain recovered a non-parent, and the categorical collider recovered only one of two parents. The main conclusion is therefore that the current target-wise ABA Learning pipeline can recover parent sets in simple complete cases, but its behaviour remains sensitive to data representation and to whether the target requires a single-parent or multi-parent rule.

## QL3: scaled noisy follow-up

QL2 used complete noiseless truth tables and therefore tested parent-set recovery under deliberately ideal conditions. QL3 was introduced to move one step closer to a realistic data setting while remaining small enough for the current implementation to run. It used a simple stochastic data-generating process with \(n=20\) rows per cell. These synthetic datasets were not sampled from the generic ArgCausalDisco simulator; they were purpose-built for testing parent-set recovery under controlled three-variable mechanisms.

QL3 used five structural configurations crossed with three data modes, giving fifteen cells. The five structural configurations were:
\[
x_0\to x_1\to x_2,\qquad
x_1\to x_0\to x_2,
\]
\[
x_0\to x_1,\;x_0\to x_2,\qquad
x_1\to x_0,\;x_1\to x_2,
\]
and
\[
x_0\to x_2\leftarrow x_1.
\]
Thus the chain and fork motifs were each instantiated twice, once with \(x_0\) as the direct parent of \(x_2\) and once with \(x_1\) as the direct parent of \(x_2\). This was included to test whether the learner follows the true parent position or instead tends to favour \(x_0\), addressing the \(x_0\)-position ambiguity exposed by QL1 while also testing robustness to noisy finite samples.

For binary variables, let \(\mathrm{flip}_{\rho}(z)\) denote a noisy copy of \(z\in\{0,1\}\), equal to \(1-z\) with probability \(\rho\) and equal to \(z\) otherwise. For categorical variables, let \(\mathrm{catnoise}_{\rho}(z)\) denote a noisy copy of \(z\in\{0,1,2\}\), equal to \(z\) with probability \(1-\rho\) and otherwise replaced by one of the other two categories with equal probability. For continuous variables, each \(\varepsilon\) denotes an independent standard normal draw. The exact sampled tables are fixed by deterministic random seeds, one for each experimental cell.

For the chain and fork descriptions below, \(u\) denotes the true direct parent of \(x_2\), and \(v\) denotes the other observed non-target variable. In a chain, \(v\) is the upstream root and \(u\) is generated from \(v\), giving \(v \to u \to x_2\). In a fork, \(u\) is the common cause and \(v\) is the other child, giving \(u\to v\) and \(u\to x_2\). The assignment of \(u\) and \(v\) to \(x_0\) or \(x_1\) depends on the parent-position variant.

*Table: QL3 data-generating mechanisms by motif and data mode. Here \(u\) denotes the true direct parent of \(x_2\) in the single-parent chain and fork cells, while \(v\) denotes the other non-target variable. All Gaussian noise variables are independent standard normal draws.*

| Motif | Data mode | Data-generating mechanism |
|---|---|---|
| Chain | Binary | \(v\sim\mathrm{Bernoulli}(0.5)\), \(u=\mathrm{flip}_{0.2}(v)\), \(x_2=\mathrm{flip}_{0.1}(u)\). |
| Chain | Categorical-3 | \(v\sim\mathrm{Uniform}\{0,1,2\}\), \(u=\mathrm{catnoise}_{0.2}(v)\), \(x_2=\mathrm{catnoise}_{0.1}(u)\). |
| Chain | Continuous | \(v\sim\mathcal{N}(0,1)\), \(u=v+0.5\varepsilon_u\), \(x_2=u+0.3\varepsilon_t\). |
| Fork | Binary | \(u\sim\mathrm{Bernoulli}(0.5)\), \(v=\mathrm{flip}_{0.2}(u)\), \(x_2=\mathrm{flip}_{0.1}(u)\). |
| Fork | Categorical-3 | \(u\sim\mathrm{Uniform}\{0,1,2\}\), \(v=\mathrm{catnoise}_{0.2}(u)\), \(x_2=\mathrm{catnoise}_{0.1}(u)\). |
| Fork | Continuous | \(u\sim\mathcal{N}(0,1)\), \(v=u+0.6\varepsilon_v\), \(x_2=u+0.3\varepsilon_t\). |
| Collider | Binary | \(x_0,x_1\sim\mathrm{Bernoulli}(0.5)\) i.i.d., \(b=x_0\lor x_1\), \(x_2=\mathrm{flip}_{0.1}(b)\). |
| Collider | Categorical-3 | \(x_0,x_1\sim\mathrm{Uniform}\{0,1,2\}\) i.i.d., \(b=\max(x_0,x_1)\), \(x_2=\mathrm{catnoise}_{0.1}(b)\). |
| Collider | Continuous | \(x_0,x_1\sim\mathcal{N}(0,1)\) i.i.d., \(x_2=x_0+x_1+0.3\varepsilon_t\). |

The positive class was defined from the generated target value. Binary cells used \(x_2=1\), categorical-3 cells used \(x_2=2\), and continuous cells used \(x_2\geq 0\). Before ABA Learning, continuous non-target variables were discretised into three uniform bins, so the learner saw predicates such as \(\texttt{x0\_bin0(A)}\), \(\texttt{x0\_bin1(A)}\), and \(\texttt{x0\_bin2(A)}\), rather than raw real values.

After data generation, the table-to-ABA conversion was the same as before. The target was always \(x_2\), and the target column was excluded from the background knowledge. Binary variables were encoded using positive-case predicates such as \(x_0(A)\), categorical variables using value predicates such as \(\texttt{x0\_val\_2(A)}\), and continuous variables using three uniform-bin predicates such as \(\texttt{x0\_bin2(A)}\). The learner used non-deterministic folding with a folding budget of 15 and a Prolog learning timeout of 300 seconds.

All fifteen cells terminated without timeout. The outcome distribution was one solved cell, twelve completed no-solution cells, and two early error cells. No cell achieved exact parent-set recovery, and the maximum variable-level \(F_1\) score was \(0.67\). Table: QL3 scaled noisy follow-up summarises the QL3 outcomes at the level of recovered base variables.

*Table: QL3 scaled noisy follow-up at \(n=20\). \(F_1\) measures variable-level overlap between recovered base variables and the true parent set.*

| Cell | Mode | True parents | Recovered | \(F_1\) | Jaccard | Recall | Outcome |
|---|---|---|---|---|---|---|---|
| Chain, \(x_1\)-parent | Binary | \(\{x_1\}\) | \(\{x_0,x_1\}\) | 0.67 | 0.50 | 1.00 | Solved |
| Chain, \(x_1\)-parent | Cat3 | \(\{x_1\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Chain, \(x_1\)-parent | Cont3 | \(\{x_1\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Chain, \(x_0\)-parent | Binary | \(\{x_0\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Chain, \(x_0\)-parent | Cat3 | \(\{x_0\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Chain, \(x_0\)-parent | Cont3 | \(\{x_0\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Fork, \(x_0\)-parent | Binary | \(\{x_0\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | Error |
| Fork, \(x_0\)-parent | Cat3 | \(\{x_0\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Fork, \(x_0\)-parent | Cont3 | \(\{x_0\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Fork, \(x_1\)-parent | Binary | \(\{x_1\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Fork, \(x_1\)-parent | Cat3 | \(\{x_1\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Fork, \(x_1\)-parent | Cont3 | \(\{x_1\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Collider | Binary | \(\{x_0,x_1\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | Error |
| Collider | Cat3 | \(\{x_0,x_1\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |
| Collider | Cont3 | \(\{x_0,x_1\}\) | \(\emptyset\) | 0.00 | 0.00 | 0.00 | No solution |

The only solved cell was the binary chain with \(x_1\) as the true parent. Its learned target rules were:
\[
x_2(A) \leftarrow \alpha_1(A), x_0(A),
\qquad
x_2(A) \leftarrow x_1(A).
\]
Thus the recovered base-variable set was \(\{x_0,x_1\}\), while the true parent set was \(\{x_1\}\). This gives full recall but imperfect precision and \(F_1\): \(\mathrm{Precision}=0.50\), \(\mathrm{Recall}=1.00\), and \(F_1=0.67\). The cell is therefore a parent-superset result rather than exact recovery. The true parent \(x_1\) appears, but so does the ancestor \(x_0\). This result should therefore be treated as partial recovery rather than success.

QL3 shows that the scaled noisy setting can be made computationally feasible at \(n=20\). Despite the failure of ABA Learning to find solutions in 80\% of these cases, this by no means invalidates the potential of ABA Learning to recover causal structure from noisy data. Much like QL1, QL3 was setup as a way to quickly investigate what would happen for arbitrarily chosen hyper-parameters. However, immediate future work should systematically investigate how varying the noise parameters affects how and whether ABA Learning can recover parents.

## Interim interpretation after QL1, QL2 and QL3

The qualitative investigation gives a bounded but useful picture of the current `aba_asp/causal` implementation. QL1 established that the pipeline can run end-to-end on controlled three-node motifs and produce inspectable learned target rules, but it also showed that recovery is sensitive to motif and data representation. Fork cells were recovered exactly, although this was partly confounded because the true parent was \(x_0\). Chain cells exposed a more serious issue: when the direct parent was \(x_1\), the learned rules often cited \(x_0\), an ancestor or proxy rather than the direct parent. QL2 replaced the initial run with complete noiseless truth tables. This corrected some behaviour, such as binary chain recovery, but did not make recovery reliable: the mean \(F_1\) score was \(0.61\), categorical chain still recovered \(x_0\), and collider recovery remained problematic. QL3 then moved to a modest noisy setting with \(n=20\) and parent-position controls. It completed without timeout, but it did not produce any exact recoveries. The only solved cell was a binary chain case whose learned rules recovered \(\{x_0,x_1\}\) when the true parent set was \(\{x_1\}\), giving full recall but only \(0.5\) precision and \(F_1=0.67\).

The results support a cautious conclusion. The current target-wise ABA Learning pipeline can recover parent sets in selected idealised cases, especially simple binary and fork cases. However, recovery is not robust across motifs, encodings or modest noisy scaling. When the recovered variables match the known parents, this is useful evidence that the representation and learner can express the intended local mechanism in that controlled case. The qualitative investigation identifies both a promising minimal behaviour and a clear boundary of the current implementation.

The main limitations are as follows. First, the investigation is target-wise: it evaluates learned rules for \(x_2\), not whole-graph recovery. Second, it does not implement full Russo-style Causal ABA: there are no \(\mathsf{arr}\), \(\mathsf{noe}\) or \(\mathsf{indep}\) assumptions, no d-separation encoding, and no stable-extension-as-DAG construction. Third, the datasets are synthetic and deliberately small; QL2 is a best-case logical baseline, while QL3 is still only a small \(n=20\) noisy study. Fourth, categorical and continuous modes change the predicate vocabulary seen by ABA Learning, so failures may reflect representation choices as well as learning behaviour. Fifth, continuous variables are discretised before learning, so these experiments do not test learning from raw continuous values. Sixth, QL3 shows that noisy scaled settings can still produce no-solution or error outcomes even when they complete computationally. Seventh, our method for introducing stochasticity was run with arbitrarily chosen hyper-parameters --- a further systematic exploration of noise conditions under which ABA Learning succeeds is necessary. The project plan seeks to set out a plausible methodology by which we can address these issues.
