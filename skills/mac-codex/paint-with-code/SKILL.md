---
name: paint-with-code
description: Use when creating or revising editable code-generated paintings, watercolor illustrations, expressive poster art, or layered visual sketches where the user wants source-level control instead of prompt-only image generation. Do not use for photorealism, pixel-exact brand layouts, or precision technical diagrams.
---

# Paint With Code

Create the image as an editable JavaScript artifact. The normal deliverable is source code plus a verified PNG, not a prompt-only bitmap.

## Choose This Medium

Use `p5.brush` when brush texture, visible construction, reproducibility, and later source edits matter. Prefer image generation for a fast photorealistic result, and prefer SVG/Draw.io for exact diagrams or typography-heavy layouts.

## Workflow

1. Translate the request into an intent sheet: subject, composition, palette, texture, editable parameters, and prohibited additions. Do not silently invent major subjects or symbols.
2. Copy the complete `assets/starter/` directory, including its vendored MIT-licensed `p5.brush` build, into the requested output directory. Keep palette, geometry, layer functions, and seed near the top of `sketch.js`.
3. Read [references/p5-brush-api.md](references/p5-brush-api.md) before changing brush calls. Start from its small verified API surface; expand it only after checking the installed or pinned library documentation.
4. Render in a WebGL2-capable browser. Wait for `canvas[data-paint-ready="true"]`, then inspect the canvas and capture the PNG.
5. Verify that the canvas is nonblank, correctly framed, free of accidental overlap, and visually legible at the requested dimensions. Use a screenshot and a canvas-pixel check when browser tooling supports them.
6. Iterate by editing named parameters or layer functions. Preserve approved composition unless the user requests a redesign.

## Deliverables

Keep the editable source beside the rendered result:

- `index.html` and `sketch.js`
- the final PNG at the requested dimensions
- local image assets actually used by the sketch

Do not claim visual completion from a successful page load alone. Report any WebGL2, font, asset, or browser limitation that prevented a real render check.

## Taste Alignment

For repeated work in one style, retain approved examples and compare new candidates pairwise against them. Ask which candidate is closer to the intended taste instead of assigning abstract 0-10 aesthetic scores. Do not start GEPA, reward-model, or GRPO training unless the user explicitly requests model optimization and provides a suitable evaluation set and compute budget.

## Common Mistakes

- Feeding the model a long API manual, which encourages invented methods.
- Producing only a PNG and discarding the editable artifact.
- Using unseeded randomness, making revisions impossible to compare.
- Replacing a requested local edit with a complete regeneration.
- Treating compile success as evidence that the artwork is visually correct.
