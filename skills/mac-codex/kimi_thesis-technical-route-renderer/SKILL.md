---
name: kimi_thesis-technical-route-renderer
description: Render thesis-style 技术路线图 (technical route diagrams) from a declarative JSON spec to high-DPI PNG plus a matching .drawio source. Paper-friendly black/white/grey style, rounded blocks, orthogonal 3-segment routing for Y/T junctions, dashed centre-line connectors between sections. Use when the user asks to (re)make 论文图1-1 / 技术路线图 / 流程图 / architecture diagram for a thesis, and wants both a publication-ready PNG and an editable .drawio. Tuned for Chinese theses; auto-detects CJK fonts on macOS / Windows / Linux.
---

# Thesis Technical Route Renderer

Render a thesis 技术路线图 from one JSON spec into:

- a paper-ready **PNG** (high DPI, CJK-safe), and
- a matching **`.drawio`** source for future edits in [app.diagrams.net](https://app.diagrams.net).

The renderer enforces a paper-friendly style: grey section headers, rounded
white blocks, output blocks tinted darker, orthogonal 3-segment routing for
every Y / T junction, dashed centre-line connectors between major sections.

## Quick start

```bash
# 1) install deps once (matplotlib + pillow). Uses uv if available, else pip.
bash scripts/install_deps.sh

# 2) render the bundled example (Wyatt's master-thesis Fig. 1-1)
python scripts/render_technical_route.py --spec scripts/example_spec.json
# outputs: scripts/example_spec.png + scripts/example_spec.drawio

# 3) for a new figure: copy example_spec.json, edit titles + coordinates, rerun
python scripts/render_technical_route.py --spec my_fig.json --png fig.png --drawio fig.drawio
```

## When to use this skill

Trigger on user phrases like:

- "重做我的图 1-1 / 技术路线图 / 流程图"
- "把这个图字号调大 / 美化一下"
- "再画一份和图 1-1 一样风格的图"
- "thesis technical route diagram", "research roadmap figure", "architecture overview"

Do **not** trigger for:

- general flowcharts that are not paper figures (use plain drawio templates)
- Mermaid diagrams in Markdown (use Mermaid directly)

## Spec format

A spec is one JSON file. Top-level keys: `canvas`, `sections`, `arrows`,
`between_sections`, `extras`, and an optional `style` override.

### canvas

```jsonc
"canvas": {
  "width": 1300,           // page width in px (drawio coords)
  "left_margin": 30,       // section frames start here
  "dpi": 200,              // PNG output DPI
  "auto_height": true,     // compute page height from the lowest section
  "bottom_padding": 20
}
```

### sections

Each section is a labeled grey-headed band. Place blocks inside by setting
their `x` / `y` in absolute page coords.

```jsonc
{
  "id": "s1",
  "y": 20,
  "height": 580,
  "title": "构建黄瓜全生育期视觉表型感知模型",
  "blocks": [
    {"id": "s1_1", "x": 80,  "y": 110, "w": 565, "h": 85,
     "title": "温室黄瓜图像数据采集",
     "sub": "覆盖多生育阶段与典型遮挡场景"},
    {"id": "s1_4", "x": 230, "y": 385, "w": 840, "h": 70,
     "title": "输出：器官级实例分割结果（Mask）",
     "highlight": true}
  ]
}
```

`highlight: true` → darker grey fill, used for **output / conclusion** blocks.

### arrows

Each arrow refers to source / target block IDs. Five `type` values:

| type       | use case                              | extra fields                |
| ---------- | ------------------------------------- | --------------------------- |
| `straight` | source directly above target          | —                           |
| `step`     | two-source → one-target (Y / T)       | `from_anchor`, `to_anchor`, `mid_y` |
| `side`     | horizontal connector between siblings | `side` (`right`/`left`), `mid_y` |
| `auto`     | straight if columns align, else step  | optional `mid_y`            |
| `custom`   | hand-routed polyline                  | `points: [[x,y], …]`        |

For every step / Y / T junction, **always set `mid_y`** so the horizontal
midpoint lands cleanly between the two boxes. Aim for each vertical stub to be
≥ 20 px tall — otherwise the path looks like only two segments, not three.

`dashed: true` makes the arrow dashed (use sparingly, e.g. side / feedback /
override arrows).

### between_sections

Adds the dashed centre-line arrow between two sections automatically.

```jsonc
"between_sections": [
  {"from_section": "s1", "to_section": "s2"},
  {"from_section": "s2", "to_section": "s3"}
]
```

### extras

Free-form labels (e.g. "VS" between two comparison boxes).

```jsonc
"extras": [
  {"type": "label", "text": "VS", "x": 660, "y": 1942, "size": 30}
]
```

### style overrides

```jsonc
"style": {
  "section_font_size": 26,
  "block_title_size": 20,
  "block_sub_size":   16
}
```

Everything in `DEFAULT_STYLE` (top of `render_technical_route.py`) can be
overridden.

## Authoring workflow

When a user asks for a new technical-route figure:

1. **Outline first**: collect 3-4 sections (one per major task), each with
   3-5 blocks. Decide which blocks are outputs (`highlight: true`).
2. **Sketch layout on a grid** before assigning numeric coordinates.
   - Recommended block heights:  75 px (single-line), 80-90 px (two-line).
   - Recommended row gaps: ≥ 50 px so every step path has visible 20 px stubs.
   - Section spacing (between sections): ≥ 35 px so the dashed centre arrow is visible.
3. **Write the JSON spec**. Use absolute coordinates relative to the page.
4. **Render**. Iterate on coordinates and `mid_y` until no arrow crosses
   block text and every step path shows three visible segments.
5. **Show the PNG to the user first; do not overwrite the user's .docx
   figure until they approve.**

## Style invariants (do not break)

- Only **orthogonal** arrows (no diagonal lines except in `extras`).
- Arrow heads stop ~ 6 px short of the destination box edge.
- Section header is filled `#2C2C2C` with white text; section frame is
  light grey on `#FAFAFA`.
- Output blocks: fill `#E5E5E5`, stroke `#3A3A3A` — never a different colour.
- Subtext (small grey line below title) uses `#555555` at 15 pt.

If the user asks for colour, prefer **tinting the section frame** (`frame_bg`)
rather than colouring blocks; thesis figures should remain print-safe.

## Files

```
thesis-technical-route-renderer/
├── SKILL.md
├── scripts/
│   ├── render_technical_route.py   # main renderer (PNG + .drawio)
│   ├── example_spec.json           # canonical exemplar (Fig 1-1)
│   └── install_deps.sh             # one-shot dep installer (uv or pip)
└── references/
    └── style.md                    # design tokens, coordinate cheatsheet
```

## Cross-tool notes

- **Claude Code** invokes this skill via the Skill tool.
- **Codex** (CLI) picks it up under `~/.codex/skills/`.
- The renderer is plain Python; nothing about it depends on either tool.
- Works on macOS (Hiragino Sans GB), Windows (Microsoft YaHei), and Linux
  (Noto Sans CJK / WenQuanYi). Font auto-detection is in `setup_fonts()`.
