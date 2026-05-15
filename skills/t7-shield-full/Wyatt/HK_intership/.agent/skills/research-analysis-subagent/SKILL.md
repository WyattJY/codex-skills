---
name: "research-analysis-subagent"
description: "Programmatic subagent invoked by research-workflow Step 3. Reads one paper directory and writes Analysis_Detail.md following a strict academic prompt. Invoked once per paper in a fresh session. Do not invoke directly from user requests — use research-workflow instead."
---

# Research Analysis Subagent

## Purpose
- Processes a **single** paper directory per invocation.
- Reads `paper.md` and `paper_artifacts/` within `${paper_dir}`.
- Writes `Analysis_Detail.md` into `${paper_dir}`.

## Parameters
- `${paper_dir}`: absolute path to a single paper directory containing `paper.md` and `paper_artifacts/`

## Usage
Execute these steps in order on **every** invocation — do not skip step 1 even if this skill was previously used in the same session:

1. Read [assets/analysis_prompt.md](assets/analysis_prompt.md) in full. Apply it verbatim as your role and output specification for this paper.
2. Read `${paper_dir}/paper.md` and all images under `${paper_dir}/paper_artifacts/`.
3. Write output to `${paper_dir}/Analysis_Detail.md` following the prompt specification exactly. Reference images using their absolute paths.
4. Confirm the file is written and remind the user to verify formula and image rendering.
