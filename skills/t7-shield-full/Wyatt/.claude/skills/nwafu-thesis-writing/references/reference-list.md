# NWAFU Thesis Reference List (GB/T 7714-2015, Author–Year)

## Recommendation

Do not hand-format references. Use:
- LaTeX: `biblatex` + `biber` (nwafuthesis already configures `style=gb7714-2015ay`)
- Word: Zotero (choose GB/T 7714-2015 author–year output if available) or export BibTeX → convert

## Common entry patterns (as seen in NWAFU thesis PDFs)

### 中文期刊论文 [J]

`作者1,作者2,作者3.年份.题名[J].刊名,卷(期):起止页码.`

Example:
`常明,王西琴,贾宝珍.2019.中国粮食作物灌溉用水效率时空特征及驱动因素——以稻谷、小麦、玉米为例[J].资源科学,41(11):2032-2042.`

### 英文期刊论文 [J]

`Author A, Author B, Year. Title[J]. Journal, volume(issue): pages.`

Example:
`Ainsworth EA, Leakey ADB, Ort DR, Long SP, 2008. FACE-ing the facts: ...[J]. New Phytol, 179(1): 5-9.`

### 学位论文 [D]

`作者.年份.题名[D].授予单位.`

Example:
`刘照.2024.基于机理模型与深度学习方法的农作物长势参数与产量反演研究[D].中国科学院大学(中国科学院东北地理与农业生态研究所).`

## LaTeX `.bib` field checklist (for correct automatic output)

- Journal: `author`, `year`, `title`, `journaltitle`, `volume`, `number`, `pages`
- Thesis: `author`, `year`, `title`, `institution`, `location` (optional), `type` (if used)

If an entry renders wrong, fix the `.bib` fields instead of patching the output text.
