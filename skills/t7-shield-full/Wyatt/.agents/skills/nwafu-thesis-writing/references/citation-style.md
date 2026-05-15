# NWAFU Thesis Citations (Author–Year / 著者-出版年)

## Core rule

Use author–year citations throughout the thesis (著者-出版年制). Prefer auto-generated citations (LaTeX `biblatex`/`biber`) whenever possible.

## In-text citation forms

### 1) Author as narrative subject

- 中文：张三（2022）指出…… / 张三等（2022）认为……
- 英文：Smith (2020) reported … / Li et al. (2024) found …

LaTeX (`nwafuthesis`):
- Narrative: `\\textcite{key}`
- Year only (after an explicit author name): `\\yearcite{key}` or `\\citeyear{key}`

### 2) Author not mentioned (parenthetical)

- 中文：……（齐学斌等 2022）
- 英文：… (FAO Report, 2021) / (Coyago-Cruz et al. 2019; Giuliani et al. 2011)

LaTeX:
- Parenthetical: `\\cite{key}` or `\\parencite{key}`

## Author count rules

- 2 authors: 中文用“和”，英文用“and”
- ≥3 authors: 中文用“等”，英文用“et al.”

Template defaults (`nwafuthesis-master/nwafuthesis.cls`):
- `maxcitenames=2`, `mincitenames=1` (3+ authors truncate to 1 + “等/et al.”)
- `maxbibnames=99` (bibliography lists all authors)

## Multiple citations at one location

- Different first-authors: separate with semicolons `;`
- Same first-author, different years: separate years with commas `,`
- Same first-author, same year: add suffix `a/b/c` (e.g., 2023a, 2023b)

LaTeX:
- Multi-cite: `\\cite{key1,key2,key3}` (comma-separated keys; output uses semicolons by style rules)
- Page numbers: `\\parencite[20-22]{key}` → (Author Year: 20–22)

## Consistency checklist

- Keep punctuation consistent within the whole thesis (don’t mix multiple conventions).
- If using LaTeX, rely on `biblatex` output and avoid hand-typing citations.
