---
name: ui-trends-watcher
description: Use when Wyatt asks to extract reusable UI direction, design tokens, app/dashboard patterns, or implementation checklists from local products, screenshots, or approved UI examples.
---


# UI Trends Watcher
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Workflow

1. Read recent product cases, UI preferences, and approved screenshots only when available and relevant.
2. When Wyatt asks to learn from a local app UI, inspect implementation and evidence: docs, routes, page components, CSS/theme tokens, screenshots, and demo assets.
3. Summarize 3-5 reusable UI directions for dashboards, admin consoles, model pages, and reports.
4. Convert directions into `DESIGN_TOKENS.md`, component specs, or an implementation checklist.
5. Prefer the target project's `docs/` directory on `H:/T7` when Wyatt points at a T7 project.
6. For app/product work, hand off to `$aihubmix-image-gen` or `$wyatt-product-team` only after target audience and density are clear.

## Local Product Review Pattern

- Inventory the real UI source of truth: theme files, page components, constants, route structure, delivery screenshots, and existing plans.
- Review by task flow: onboarding, dashboard, core workflow, analytics, settings/admin.
- Extract implementation decisions: hierarchy, density, whitespace, color semantics, component reuse, empty/loading/error states, and demo-data support.
- Final output should be a team-facing experience note plus implementation checklist.

## Hard Rules

- Do not make generic mood boards without implementation guidance.
- Do not overwrite Wyatt's preference for practical, polished, data-rich deliverables.
- Avoid one-note palettes, decorative-only UI, and marketing pages when the requested artifact is an app, tool, or dashboard.
- Do not store private screenshots or company raw UI data.
