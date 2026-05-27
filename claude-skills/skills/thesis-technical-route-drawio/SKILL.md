---
name: thesis-technical-route-drawio
description: "Create and refine thesis technical route diagrams (技术路线图) in Draw.io (.drawio) with paper-style black/white visuals, dashed section frames, rectangular blocks, and orthogonal connectors. Use when asked to generate or polish a drawio technical路线图/flowchart/architecture figure (especially when mimicking a reference image) and you must ensure connectors are straight/orthogonal and never cross text."
---


## Claude Code Migration Notes

This skill was migrated from the local Codex skill registry for Claude Code. Use it as a Claude Code `SKILL.md` skill. Some source text may name Codex-only tools or channels; in Claude Code, use the closest available Claude Code tool, shell command, MCP/plugin integration, or local helper script. Keep secrets in Keychain, environment variables, or authenticated CLIs only.

# Thesis Technical Route Drawio

## Quick Start

1. List the required **sections**, **blocks** (modules/outputs), and **connections** (arrows) from the user’s thesis outline/requirements.
2. Build/update a `.drawio` figure with:
   - Outer dashed frame + dashed section frames
   - Rectangular blocks (black stroke, white fill)
   - Orthogonal connectors only (no diagonal/curved lines)
3. Iterate until **no connector crosses any block text** and arrow lines are clearly visible.

## Workflow

### 1) Extract diagram content

- Convert narrative requirements into: `Section -> Blocks -> Edges`.
- For data-construction parts, explicitly include dataset derivations (e.g., image pair → VL inference → QA pairs → prompt iteration).

### 2) Lay out the page first (before drawing arrows)

- Use a grid; align blocks in rows/columns; keep whitespace for routing.
- Recommended minimum spacing:
  - Horizontal gap between connected blocks: `>= 40px`
  - Vertical gap between stacked blocks: `>= 25px`
- Put long cross-section links on the **outside margin** (route along the frame), and consider dashed lines for “auxiliary/feedback” relations.

### 3) Draw connectors (orthogonal only)

- Prefer `edgeStyle=orthogonalEdgeStyle` with clear entry/exit sides (`exitX/exitY`, `entryX/entryY`).
- If an arrowhead hides the line, increase spacing or ensure `endSize` is set.
- Avoid manual waypoints; only add points when routing must go around blocks.

### 4) Validate and polish

Run the bundled audit script to catch common issues:

`python scripts/drawio_audit.py path/to/figure.drawio --gap-threshold 30`

Fix warnings by adjusting spacing, ports, or (as a last resort) adding a routed “outside-frame” path.

## Style Reference

Use `references/drawio-style.md` as the canonical style snippets for boxes, titles, frames, and edges.
