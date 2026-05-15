# Expert Survey Blueprint

Use this blueprint when writing the **final** report after all per-paper `Analysis_Detail.md` files already exist.

## Report Intent

The final report should read like:
- a mature review article,
- an expert consulting memo,
- or a thesis-grade literature survey section.

It should **not** read like:
- a paper-by-paper digest,
- a simple merge of per-paper notes,
- or a chronology of “paper A says / paper B says / paper C says”.

## Opening Pattern

The report should open by making the following explicit:
- research object
- covered literature scope
- report goal
- output positioning
- center thesis / central judgment

Useful opening labels include:
- 研究对象
- 覆盖文献
- 报告目标
- 输出形态
- 本报告的中心判断

These labels can be adapted to the user's domain and writing style.

## Recommended Chapter Logic

Default chapter flow:

1. Background and problem definition
2. Technical routes / method taxonomy
3. Key progress by route
4. Cross-paper comparison
5. Unresolved bottlenecks
6. Future directions

Within each chapter, use this internal order:

1. define the local problem
2. explain why earlier approaches were insufficient
3. group representative papers into one technical route
4. extract what these papers collectively improved
5. identify what remains unsolved

## Evidence Usage

Each paper should contribute one or more of:
- a representative mechanism
- a benchmark result
- a failure mode
- a turning point in the research line
- a useful architecture figure

Do not give every paper equal narrative weight by default.
Assign weight based on:
- representativeness
- novelty
- empirical influence
- explanatory usefulness for the chapter argument

## Anti-Patterns

Avoid the following unless the user explicitly wants them:

- one subsection per paper
- paper title as section title
- repetitive formula:
  - “X paper proposes…”
  - “Y paper introduces…”
  - “Z paper improves…”
- equal paragraph length for every paper
- descriptive listing without judgment

## Required Comparative Moves

A good expert survey must repeatedly perform comparative reasoning such as:
- why this route emerged
- what it improved over the previous route
- what tradeoff it introduced
- which settings it works best in
- why it is still insufficient

Useful sentence moves:
- “与上一阶段相比……”
- “这类方法的共同收益在于……”
- “它们真正解决的是……，而不是……”
- “性能提升的代价是……”
- “这些工作虽然提高了……，但在……上仍然受限”

## Figure Strategy

Insert figures with a purpose.

Prefer figures that do one of these:
- explain a canonical architecture
- show a benchmark/task setup the reader must understand
- visualize the method family split
- support a turning point in the chapter argument

Do not insert figures only because a paper has them.

## Final Self-Check

If you remove the paper titles from the report and the argument still stands, the synthesis is working.

If removing paper titles makes the report collapse into disconnected paragraphs, the report is still too paper-centric.
