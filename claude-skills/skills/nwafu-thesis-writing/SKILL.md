---
name: nwafu-thesis-writing
description: Write Northwest A&F University (西北农林科技大学, NWAFU) master’s thesis content with the correct author–year (著者-出版年) in-text citations and GB/T 7714-2015 author–year (gb7714-2015ay) bibliography style. Use when drafting or revising thesis sections/chapters (摘要/文献综述/方法/系统设计等), converting a paper (e.g., manuscript.docx) into thesis writing, or checking/fixing citation + reference list formatting for the nwafuthesis LaTeX template or Word/Markdown drafts (e.g., “Li et al., 2024” style).
---


# NWAFU Master Thesis Writing & Citations
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Quick Start

1. Pick an output mode:
   - LaTeX (`nwafuthesis` template) for final typesetting
   - Word/Markdown for drafting
2. Use author–year citations everywhere (著者-出版年制):
   - Narrative: `作者（年份）…` / `Author (Year) …`
   - Parenthetical: `（作者等 年份）` / `(Author et al., Year)`
   - Load `references/citation-style.md` when unsure.
3. Keep the reference list consistent with GB/T 7714-2015 author–year:
   - Prefer generating from `.bib` (LaTeX) or Zotero export (Word) instead of hand-formatting.
   - Load `references/reference-list.md` and `references/nwafuthesis-latex.md`.

## Workflow (Draft Thesis Content)

1. Collect sources (paper + system docs + experiment notes) and extract “claims → evidence → citations”.
2. Outline the target section (3–5 subheadings) and decide which citations support each subheading.
3. Draft in Chinese academic voice:
   - Use “本文/本研究/本章” instead of “我”.
   - Prefer short topic sentences + evidence + summary at paragraph ends.
4. Insert citations while writing (avoid “finish first, cite later”).
5. Add a short “本章小结” that summarizes contributions, limitations, and what the next chapter builds on.

## Repo Pointers (Optional)

- Citation rules + LaTeX commands: `nwafuthesis-master/contents/chap03.tex`
- LaTeX citation engine config: `nwafuthesis-master/nwafuthesis.cls` (`biblatex` `style=gb7714-2015ay`)
- Example thesis formatting: `master-paper/参考文献/硕士论文参考/2022050389 白嘉鸣 融合生长与环境要素的樱桃番茄动态灌水模型构建.pdf`
- Your main writing sources:
  - `master-paper/11.28_revise/manuscript.docx` / `master-paper/11.28_revise/manuscript_zh.md`
  - `cucumber-irrigation-linux/PROJECT_DOCUMENTATION.md`

## Validation Checklist

- Use author–year citations consistently (中/英 punctuation consistent within the document).
- Separate different first-authors with semicolons; use `a/b/c` suffix for same-year same-author.
- Ensure every figure/table/equation is cited in text and has a caption.
- Ensure every in-text citation has a matching reference list entry (and vice versa).
