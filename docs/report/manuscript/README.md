# Manuscript sources

LaTeX chapters for the interim/final report live here. Each chapter has a paired **Markdown
mirror** (same basename, `.md` extension) for ChatGPT Project context.

## File pairing

| `.tex` (authoritative, for compilation) | `.md` (mirror, for ChatGPT) |
|---|---|
| `introduction.tex` | `introduction.md` |
| `literature-review.tex` | `literature-review.md` |
| `background.tex` | `background.md` |
| `experimentation.tex` | `experimentation.md` |
| `project_plan.tex` | `project_plan.md` |

**Rule:** edit the `.tex` for submission; regenerate or hand-sync the `.md` when the chapter
changes materially. The `.md` files are not compiled.

## Current status

| Chapter | `.tex` | `.md` |
|---|---|---|
| Introduction | *pending — copy in* | placeholder |
| Literature review | *pending — copy in* | synced from prior mirror |
| Background | *pending — copy in* | synced from prior mirror |
| Experimentation | present (`experimentation.tex`) | *pending sync from .tex* |
| Project plan | *pending — copy in* | placeholder |

Earlier theory drafts remain in `docs/theory/background.tex` and
`docs/theory/literature_review.tex` (canonical theory context per `AGENTS.md`). Report
chapters here may diverge from those files once you copy in your authored versions.

## Building

`main.tex` is a minimal driver that `\input`s all five chapters. Adjust the preamble (document
class, packages, bibliography) to match your Imperial template before compiling.

```
docs/report/manuscript/
  main.tex
  introduction.tex
  literature-review.tex
  background.tex
  experimentation.tex
  project_plan.tex
  figures/          # report-only figures
```

Bibliography: point `\bibliography{...}` at your `.bib` (e.g. `docs/papers/secondary/sample.bib`
or a manuscript-local `references.bib`).

## Regenerating Markdown mirrors

When a `.tex` chapter changes, update the matching `.md` so ChatGPT Project files stay current.
Preserve wording; convert `\section{}` → `##`, `\cite{key}` → `[cite: key]`, keep inline math
as `\( ... \)`. Ask Cursor to regenerate a mirror from the `.tex` when needed.
