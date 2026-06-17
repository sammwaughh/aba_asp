# Manuscript sources

LaTeX chapters for the interim/final report live here. Each chapter has a paired **Markdown
mirror** (same basename, `.md` extension) for ChatGPT Project context.

## File pairing

| `.tex` (authoritative, for compilation) | `.md` (mirror, for ChatGPT) |
|---|---|
| `introduction.tex` | `introduction.md` |
| `literature_review.tex` | `literature_review.md` |
| `background.tex` | `background.md` |
| `experimentation.tex` | `experimentation.md` |
| `project_plan.tex` | `project_plan.md` |

**Rule:** edit the `.tex` for submission; regenerate or hand-sync the `.md` when the chapter
changes materially. The `.md` files are not compiled.

## Current status

| Chapter | `.tex` | `.md` |
|---|---|---|
| Introduction | present (`introduction.tex`) | present (`introduction.md`) |
| Literature review | present (`literature_review.tex`) | present (`literature_review.md`) |
| Background | present (`background.tex`) | present (`background.md`) |
| Experimentation | present (`experimentation.tex`) | present (`experimentation.md`) |
| Project plan | present (`project_plan.tex`) | present (`project_plan.md`) |

Earlier theory drafts remain in `docs/theory/background.tex` and
`docs/theory/literature_review.tex` (canonical theory context per `AGENTS.md`). Report
chapters here may diverge from those files once you copy in your authored versions.

## Building

The actual chapter sources in this folder are **flat** — one `.tex` per chapter plus paired
`.md` mirrors and a `figures/` directory:

```
docs/report/manuscript/
  main.tex          # external Overleaf driver (see note below)
  introduction.tex
  literature_review.tex
  background.tex
  experimentation.tex
  project_plan.tex
  figures/          # report-only figures
```

**Note on `main.tex`.** `main.tex` is the driver used in Samuel's external Overleaf/Imperial
project, where the chapters sit in per-chapter subdirectories. It therefore `\input`s paths like
`introduction/introduction.tex`, `title/title.tex`, `appendix/appendix.tex`, and
`\bibliography{bibs/sample}` that do **not** exist in this flat folder. It is kept here verbatim
as a reference copy of the Overleaf driver and is **not** intended to compile against this
directory; the flat `.tex` files above are the authoritative chapter sources that get copied
into that Overleaf project. Do not treat `main.tex` as the repo build target.

## Regenerating Markdown mirrors

When a `.tex` chapter changes, update the matching `.md` so ChatGPT Project files stay current.
Preserve wording; convert `\section{}` → `##`, `\cite{key}` → `[cite: key]`, keep inline math
as `\( ... \)`. Ask Cursor to regenerate a mirror from the `.tex` when needed.
