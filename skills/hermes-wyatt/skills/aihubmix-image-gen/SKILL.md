---
name: aihubmix-image-gen
description: Use when UI Designer needs to generate a product UI draft image from a product spec, design tokens, or layout prompt via the configured AIHubMix image model.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# AIHubMix Image Generation

## Inputs
- `ui_brief.md`, `requirements.md`, or a short product/UI prompt.
- Target platform: web, dashboard, mobile, app, landing, or admin console.
- Constraints: brand, audience, states, density, and forbidden styles.

## Environment
Read credentials only from environment or `.env`:
- `HERMES_UI_IMAGE_API_KEY`, `HERMES_UI_IMAGE_BASE_URL`, `HERMES_UI_IMAGE_MODEL`
- `AIHUBMIX_API_KEY` or compatible `OPENAI_API_KEY`
- `AIHUBMIX_BASE_URL`
- `AIHUBMIX_IMAGE_MODEL`

## Workflow
1. Convert the product spec into one concrete visual prompt.
2. Generate or dry-run one draft image at a time.
3. Save outputs under `tmp/ui-drafts/` or a project-local `ui-drafts/`.
4. Ask Wyatt to approve direction before block-level design.
5. After approval, write `DESIGN_TOKENS.md` and `COMPONENT_SPEC.md`.

## Hard rules
- Never print API keys, tokens, `.env`, cookies, or account files.
- Do not hard-code model names; use `HERMES_UI_IMAGE_MODEL` or `AIHUBMIX_IMAGE_MODEL`.
- Image drafts are for UI direction only; final frontend implementation must still follow the G0-G9 gate.
- Do not generate UI that requests or displays company raw data.
