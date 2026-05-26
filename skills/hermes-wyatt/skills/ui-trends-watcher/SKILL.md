---
name: ui-trends-watcher
description: Use to maintain Wyatt's UI style watchlist and translate current UI references into reusable dashboard/app design notes.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# UI Trends Watcher

## Workflow
1. Read recent product cases, Wyatt UI preferences, and approved screenshots if available.
2. When Wyatt asks to “learn from” a local product/app UI, inspect both implementation and evidence: README/product docs, routes/constants, page components, CSS/theme tokens, and screenshots or demo assets. Do not rely on screenshots alone.
3. Summarize 3-5 reusable UI directions for dashboards, admin consoles, model pages, and reports.
4. Convert trends into `DESIGN_TOKENS.md` starter notes, not vague style adjectives. Include concrete token candidates, layout templates, component patterns, and checklists.
5. Write the deliverable where the product/team can reuse it (prefer the project `docs/` directory on T7 when the user points at a T7 project) and link useful directions to product cases or memory findings.
6. For app/product work, hand off to `aihubmix-image-gen` or product-builder only after the target audience and density are clear.

## Local product UI review pattern
- Start with `case-router` for non-trivial product/design work; load at most 0-3 relevant cases and explicitly state whether they are directly reusable or only adjacent.
- Inventory the target repo enough to identify the real UI source of truth: global theme, feature CSS, route/page components, constants, delivery screenshots, and existing plans.
- Review pages by task flow, not by file order: login/onboarding, dashboard, core model/workflow pages, analytics, settings/admin.
- For each page, extract reusable design decisions: information hierarchy, density, whitespace, color semantics, component reuse, empty/loading/error states, and demo-data support.
- Final output should be a team-facing experience note plus an implementation checklist; avoid a one-off task narrative.
- See `references/agri-model-platform-ui-review.md` for a concrete example of reviewing a local agricultural model platform for UI cleanliness and polish.

## Hard rules
- Do not make generic mood boards without implementation guidance.
- Do not overwrite Wyatt's established preference for practical, polished, data-rich deliverables.
- Avoid one-note palettes, decorative-only UI, and marketing pages when the requested artifact is an app/tool/dashboard.
- Do not store private screenshots or company raw UI data.

