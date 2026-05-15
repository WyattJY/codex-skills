# Using `nwafuthesis` (LaTeX) for NWAFU Master Theses

## Bibliography engine

The template uses `biblatex` with `backend=biber` and `style=gb7714-2015ay` (author–year).
See: `nwafuthesis-master/nwafuthesis.cls`.

## Minimal setup

1. Add your `.bib`:
   - `\\addbibresource[location=local]{bib/your.bib}`
2. Cite in text:
   - Narrative: `\\textcite{key}`
   - Parenthetical: `\\cite{key}` / `\\parencite{key}`
   - With pages: `\\parencite[20-22]{key}`
3. Print references:
   - `\\printbibliography[heading=bibintoc]`

## Compile sequence

```
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

## Notes

- Do not manually edit the rendered bibliography; fix the `.bib` data instead.
- The template defaults `doi=false`, `isbn=false`; keep consistent with NWAFU examples unless your advisor requires otherwise.
