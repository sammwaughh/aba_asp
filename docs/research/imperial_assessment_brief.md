# Imperial MSc Assessment Brief

Operational distillation of the Imperial MSc project assessment and report-writing guidance,
tailored to the Causal ABA Learning project. Source documents: `assess.pdf`, `interim.pdf`,
`report-writing-and-assessment.pdf`, `writing.pdf`. This is a working brief, not a substitute
for the official wiki; check the originals for edge cases.

Note: `project-description.pdf` (Fabrizio's original project specification) is **not** merged
here. It remains a separate primary context document.

## Pass requirements

MSc individual project pass mark is **50%**. To pass you must:

1. submit an **interim report** judged acceptable;
2. submit a **final report** judged acceptable;
3. complete a **project presentation** judged acceptable.

The interim report is **not marked for credit** but is required to pass.

## Marking criteria (final report)

- **Framing of research problem — 20%**
- **Execution and technical quality — 40%**
- **Evaluation and reflection — 20%**
- **Communication of ideas — 20%**

### Communication as an upper bound

The Communication mark also **caps the overall project mark** (overall ≤ Communication %).
A strong project written up poorly is limited by its communication score. Two hard limits:

- **exceeding the page limit caps Communication in the 40–49% band**, which caps the whole
  project;
- unacceptable GenAI use / serious academic-integrity breaches can force a 0–39% band
  regardless of quality (and may trigger misconduct investigation).

## What the top bands imply (practically)

- **70–84%** — sharp, well-motivated framing with a clear gap; precise, ambitious-yet-
  realistic research questions; methodology with strong, critically justified design;
  high-quality, reproducible technical work; thorough, well-controlled evaluation that
  interrogates trade-offs and threats to validity; polished, concise writing.
- **85%+** — publication-standard across the board: original framing that could underpin a
  publishable study; exemplary methodology and evaluation that anticipates objections;
  mature self-critical reflection including what does **not** generalise; outstanding,
  accessible-yet-rigorous communication.

Implication: high marks require genuine evaluation and honest limitation analysis, not just a
working artefact.

## Final report expectations

- **Standalone**: must be fully understandable without the code, slides, or a demo. Markers
  (especially the second marker/moderators) rely on it.
- **Length**: max **60 A4 content pages** (chapters only; excludes title, contents,
  references, appendices). Recommended 2.5 cm margins, ≥11 pt. Shorter and well-edited beats
  padded — "in many cases a 40-page report is better than a 60-page report".
- **UK English** (not US English).
- **Vancouver referencing**; complete, consistent citations.
- **Serious, separate evaluation** with critical appraisal of limitations; agree the
  evaluation method with the supervisor early.
- **No source-code listings** in the report (code lives in the repo); appendices are
  peripheral and not guaranteed to be marked.
- Typical structure: abstract (≤1 page, no citations), introduction, literature/related work,
  body chapters (design/implementation/experiments — experimental projects may use one
  chapter per experiment), evaluation, conclusions/future work, references, declarations,
  appendices. A declarations section (incl. GenAI) is required.

## Interim report expectations

- Two main parts: a **Background/Literature** section and a **Progress + Plan** section
  (accomplishments to date, obstacles and how they are handled, plan/timeline for remaining
  work; define what success looks like; flag ethics approval if required).
- **Vancouver referencing**.
- **10–20 content pages** (do not exceed 20). Same formatting as the final report.
- No abstract or acknowledgements needed.
- Reusable: background material can become the final report's background chapters. Reviewed
  by the second marker (arrange a feedback meeting after submission).

## GenAI disclosure and management

- Disclose GenAI use transparently in the declarations; keep the student as the clear author.
- Acceptable use is limited and human-reviewed (idea generation, proofreading, coding
  assistance). Higher communication bands require **critical reflection** on GenAI use —
  noting limitations, checks performed, and how suggestions were adapted.
- Undeclared or over-reliant GenAI use risks the 0–39% band and misconduct referral.

## Implications for the Causal ABA Learning project

- **Not just implementation.** A straightforward implementation, however clean, will not
  score highly. The project must show originality and a thorough evaluation. The natural
  source of originality is the **integration of ABA Learning and Causal ABA** (the gap
  identified in `docs/theory/literature_review.tex`).
- **Framing (20%).** Lead with the precise gap: Causal ABA represents causal-discovery
  evidence in ABA; ABA Learning transforms ABA frameworks from examples; their interaction is
  largely unstudied. State crisp, modest research questions.
- **Execution (40%).** Emphasise reproducibility (the verified environment, exact commands,
  seeds, and DGPs already documented in `execution_guide.md` / `environment_setup.md`) and
  clear methodology for each experiment (QL-001 onward).
- **Evaluation (20%).** Plan evaluation **now**, with the supervisor. Be explicit about what
  results would and would not show — in particular, distinguish **empirical parent-set
  recovery via ABA Learning** from **Russo-style Causal ABA discovery** (see
  `research_state.md`). Honest negative/partial results are creditable.
- **Communication (20%, the cap).** Maintain UK English and Vancouver throughout from the
  start; keep within page limits; no code listings; write as you go.
- **Background reuse.** The interim background/literature can seed the final report; invest in
  `background.tex` / `literature_review.tex` quality early.

## Implications for the Samuel–ChatGPT–Cursor workflow

- **Samuel** owns all submissions, decisions, and the GenAI declaration; he is the author of
  record. He must be able to explain and defend every claim and result.
- **ChatGPT** (research/theory/writing agent) helps draft report text, frame the problem,
  align theory and results, and review plans — but its output must be critically reviewed and
  adapted by Samuel, and its assistance disclosed. ChatGPT should help write the GenAI
  reflection honestly rather than obscure it.
- **Cursor** (implementation agent) produces the reproducible artefacts, tests, and run logs
  that the Execution and Evaluation sections depend on; its commits/run artefacts should be
  traceable for the report (link experiments to commit hashes / artefact paths via
  `experiment_register.md`).
- **Division aids integrity**: keep a clear record of who/what produced each artefact and each
  passage, so GenAI disclosure is accurate and authorship remains with Samuel.

## Related docs

- `docs/research/chatgpt_project_brief.md` — ChatGPT role and team model.
- `docs/research/research_state.md` — current state, conceptual risks.
- `docs/research/experiment_register.md` — experiment tracking (link to commits/artefacts).
- `project-description.pdf` — Fabrizio's original specification (separate primary context).
