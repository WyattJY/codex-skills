---
name: expert-survey-report
description: Use when the user wants an expert literature survey from a paper set, with the final report organized by themes, problem chains, and evidence-backed synthesis rather than paper-by-paper summaries, while still requiring per-paper Analysis_Detail.md as source material.
---

# Expert Survey Report

Use this skill when the user wants a high-end survey report that reads like an expert review article or consulting-grade research report, not a stack of paper cards.

This skill does **not** replace:
- `G:\Wyatt\HK_intership\.agent\skills\research-workflow`
- `G:\Wyatt\HK_intership\.agent\skills\research-analysis-subagent`

Instead, it **builds on top of them**:
1. keep the per-paper workflow;
2. then change the **final report-writing logic**.

Canonical source-of-truth for runtime/scripts remains:
- `G:\Wyatt\HK_intership\.agent\skills\research-workflow`
- `G:\Wyatt\HK_intership\.agent\skills\research-analysis-subagent`

Supporting guidance for the final synthesis lives at:
- `G:\Wyatt\HK_intership\.agent\skills\expert-survey-report\assets\expert_survey_blueprint.md`

## When To Use

Use this skill when the user says things like:
- “不要逐篇总结，要专家级综述”
- “按主题归类，不要文献卡片感”
- “先讲研究对象、主线、问题，再讲各篇论文”
- “给我一个 consulting / review article 风格的报告”
- “最终 Word 要像成熟综述，不像 merge 出来的论文拼接”

Do **not** use this skill when:
- the user explicitly wants a paper-by-paper dossier;
- the user only wants one paper analyzed;
- the user only wants download / PDF-to-Markdown / raw merge.

## Core Rule

The pipeline still requires:
- paper download
- `paper.md`
- `paper_artifacts`
- one `Analysis_Detail.md` per paper

But the final report must **not** be written as:
- one subsection per paper
- one paper followed by one summary paragraph
- a direct concatenation of `Analysis_Detail.md`

The final report must be written as:
- a **theme-organized expert survey**
- driven by **problem chains**
- with papers used as **evidence**, not as the report skeleton

## Workflow

### 1. Run the standard paper pipeline first

Use the existing workflow to complete:
1. `paper_list.txt`
2. paper download
3. `paper.md` + `paper_artifacts`
4. one `Analysis_Detail.md` per paper

Do not skip the per-paper analysis stage.

### 2. Build a synthesis matrix before writing the final report

Before drafting the final report, extract from the paper set:
- problem addressed
- method family / technical route
- representative gains or benchmark improvements
- setting / scenario / benchmark scope
- limitations / unresolved issues
- figures worth reusing in the final report

This matrix is a planning aid. It does not need to be delivered unless the user asks.

### 3. Decide the report's main line

Before writing the final report, explicitly determine:
- research object
- coverage boundary
- report goal
- target reader
- center thesis / central judgment

The report must open by making these explicit.

### 4. Organize the final report by problem chain, not by paper order

Default structure:
1. research object / coverage / report goal / center thesis
2. why this research direction emerged
3. major technical categories or evolution stages
4. for each category:
   - what problem it addresses
   - what progress it made
   - what representative methods prove that progress
   - what limitations remain
5. cross-category comparison and trend judgment
6. open problems and future directions

If the topic needs basic background sections, include them.
Examples:
- bi-encoder vs cross-encoder
- benchmark setting differences
- retriever vs reranker division of labor
- memory / planning / tool-use distinctions

When explaining such basics, prefer real figures from papers, official docs, or high-quality technical references.

### 5. Writing constraints for the final report

The final report must satisfy all of the following:

- Do not write it as a sequence of paper summaries.
- Each chapter must revolve around a research question, technical route, or bottleneck.
- Each chapter should answer:
  - what problem is being solved?
  - what progress has been made?
  - what evidence supports that claim?
  - what still remains unsolved?
- Mention papers as supporting evidence inside the argument, not as isolated cards.
- The prose should feel like a coherent expert narrative with forward momentum.
- The report should contain explicit comparative judgments, not just neutral description.
- Important figures should be inserted where they help explain the argument.
- All claims about improvements or benchmark gains must stay traceable to the source material.

## Final Report Style Contract

Use the following style contract for the final synthesis:

- Start with a “what this report is about” block, not with paper summaries.
- State the center thesis early.
- Use section titles based on **problems, mechanisms, or stages**, not paper names.
- Prefer synthesis sentences such as:
  - “这一阶段的核心变化在于……”
  - “这类工作共同解决的是……”
  - “与上一阶段相比，关键进步体现在……”
  - “尽管取得了这些提升，但仍存在以下结构性问题……”
- Avoid repetitive paper-intro templates such as:
  - “本文提出……”
  - “该论文主要研究……”
  unless used sparingly as local evidence.

The reader should feel they are reading:
- an expert review,
- a strong survey chapter,
- or a consulting-grade research memo,

not a stitched archive of individual notes.

## Deliverables

Default deliverables:
- per-paper `Analysis_Detail.md` files inside each paper directory
- one final survey markdown
- one exported Word document

Optional:
- PDF export if the user asks

## Verification

Before claiming the survey is done, verify:
- every paper directory has `Analysis_Detail.md`
- the final report is theme-organized rather than paper-ordered
- chapter titles are topic/problem titles, not paper titles
- the opening states research object / goal / central judgment
- figures render correctly in the final document
- formulas and tables survive the export path

If the final report still reads like a pile of literature cards, the skill has not been followed.
