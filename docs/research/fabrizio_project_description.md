# Fabrizio Project Description

## Source and status

This file is a Markdown rendering of **Fabrizio Russo's** original project description,
derived from `project-description.pdf`. The PDF remains the authoritative original source;
this transcription is for convenient Cursor and ChatGPT project context. The "Original
project description" section below transcribes the specification faithfully; the later
sections are **our** working interpretation and are clearly separated from Fabrizio's text.

## Original project description

### Description

Assumption-Based Argumentation (ABA) provides a powerful formalism for representing and
reasoning with structured arguments, while recent work on ABA learning (ABALearn) has shown
how argumentation frameworks can be learned automatically from data using logic-programming
techniques [1–3]. In parallel, causal discovery aims to infer cause–effect relationships from
data and is increasingly used in high-stakes domains such as healthcare and finance [4]. More
recently, Causal Assumption-Based Argumentation (Causal ABA) has been proposed as a
principled and contestable approach to causal discovery, representing causal relationships as
argumentative structures grounded in statistical evidence [5].

This project investigates the synergy between causal discovery and ABA learning by exploring
how each paradigm can be applied to strengthen the other. On the one hand, ABA learning
techniques can be used to learn causal structures, treating causal discovery as a
rule-learning problem over argumentative representations. On the other hand, causal graphs and
causal constraints can be used to guide and structure rule learning in ABALearn. By combining
these perspectives, the project aims to develop learning approaches that are more
interpretable, structured, and contestable than either paradigm in isolation.

### Project Goals

This project will focus on two complementary objectives that reflect the two directions of
interaction between causal reasoning and ABA learning:

**1. Apply ABA Learning to Causal Discovery**

a) Represent causal graphs as sets of argumentative rules and assumptions within the ABA
   formalism.
b) Use ABA learning techniques to induce causal relationships from data, viewing causal
   discovery as a structured rule-learning problem.
c) Analyse how different ABA learning strategies affect the quality and stability of the
   learned causal structures.

**2. Use Causal Structure to Guide ABA Learning**

a) Incorporate causal assumptions and graphical constraints (e.g. causal ordering, absence of
   cycles) into the ABALearn process.
b) Investigate whether causal guidance improves the interpretability, robustness, or
   efficiency of learned ABA frameworks.
c) Study how causal information can reduce ambiguity or search complexity in ABA learning
   approaches.

### References

[1] De Angelis, E., Proietti, M., and Toni, F. *ABA Learning via ASP.* In Proceedings ICLP
2023 (EPTCS), 385, 2023. https://doi.org/10.4204/EPTCS.385.1

[2] De Angelis, E., Proietti, M., and Toni, F. *Greedy ABA Learning for Case-Based
Reasoning.* In Proceedings of the 24th International Conference on Autonomous Agents and
Multiagent Systems (AAMAS), 2025, pp. 556–564.
https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p556.pdf

[3] De Angelis, E., Proietti, M., and Toni, F. *Learning to Contest Argumentative Claims.*
Rules and Reasoning (RuleML+RR), 2025, pp. 237–255.
https://doi.org/10.1007/978-3-032-08887-1_15

[4] Glymour, C., Zhang, K., and Spirtes, P. *Review of Causal Discovery Methods Based on
Graphical Models.* Frontiers in Genetics, 2019. https://doi.org/10.3389/fgene.2019.00524

[5] Russo, F., Rapberger, A., and Toni, F. *Argumentative Causal Discovery.* Proceedings of
the 21st International Conference on Principles of Knowledge Representation and Reasoning (KR),
2024. https://doi.org/10.24963/kr.2024/88

## Working interpretation

This is **our** current reading of Fabrizio's specification, not part of the original text:

- The project sits at the **intersection of ABA Learning and Causal ABA**.
- **Direction 1** (Apply ABA Learning to Causal Discovery) asks whether ABA Learning can
  learn causal or causal-adjacent structure from data.
- **Direction 2** (Use Causal Structure to Guide ABA Learning) asks whether causal
  constraints (e.g. causal ordering, acyclicity) can guide or bias ABA Learning.
- The current `aba_asp/causal` implementation should **not** be assumed to be full
  Russo-style Causal ABA unless it implements the relevant `arr`/`noe`/`indep` assumptions,
  d-separation reasoning, and the stable-extension-as-DAG machinery (see
  `docs/research/repo_map.md`).
- The first likely novel experiment, **QL-001**, should therefore be framed **modestly** —
  validating the existing ABA Learning bridge (parent-set recovery) before claiming a full
  Causal ABA contribution (see `docs/research/research_state.md` and
  `docs/research/experiment_register.md`).

## Implications for project planning

- Each experiment should support **one or both** of Fabrizio's two directions, and record
  which.
- Report writing must clearly distinguish **ABA Learning**, **Causal ABA**, and the **current
  implementation**; do not conflate empirical parent-set recovery with full causal-
  argumentative discovery.
- **Cursor** owns implementation; **ChatGPT** helps check whether proposed experiments stay
  aligned with this specification and the two stated directions.
- Future work should log, per experiment, which of the two project directions it supports
  (track alongside `docs/research/experiment_register.md`).

## Related docs

- `project-description.pdf` — original source (authoritative).
- `docs/research/research_state.md` — current state and conceptual risks.
- `docs/research/experiment_register.md` — experiment tracking.
- `docs/research/repo_map.md` — implemented vs theory-only.
