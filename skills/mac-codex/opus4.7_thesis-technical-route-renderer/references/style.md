# Design Tokens — thesis-technical-route-renderer

The renderer's visual language is intentionally conservative so figures pass
review without rework. Treat these tokens as defaults; override only with
purpose.

## Palette

| token            | hex        | usage                                            |
| ---------------- | ---------- | ------------------------------------------------ |
| `ink`            | `#1F1F1F`  | block titles, arrow lines, primary text          |
| `ink_soft`       | `#555555`  | block subtext (below the title)                  |
| `stroke`         | `#4A4A4A`  | regular block outline                            |
| `header`         | `#2C2C2C`  | section header bar fill                          |
| `header_text`    | `#FFFFFF`  | section header text                              |
| `frame`          | `#BBBBBB`  | section frame stroke                             |
| `frame_bg`       | `#FAFAFA`  | section frame fill                               |
| `block_bg`       | `#FFFFFF`  | regular block fill                               |
| `output_bg`      | `#E5E5E5`  | **output / conclusion** block fill               |
| `output_stroke`  | `#3A3A3A`  | output block outline                             |
| `arrow`          | `#1F1F1F`  | solid arrows                                     |
| `dashed_arrow`   | `#555555`  | dashed (feedback / side / override / gap) arrows |

No colour outside this palette by default. If the user wants accent colour,
tint only the **section frame fill** (`frame_bg`); never colour individual
blocks — thesis figures need to remain print-safe at grayscale.

## Typography

| element           | size | weight |
| ----------------- | ---- | ------ |
| section title     | 24   | bold   |
| block title       | 19   | bold   |
| block subtext     | 15   | normal |
| free-form label   | 24-30 | bold  |

CJK is rendered via Hiragino Sans GB (macOS), Microsoft YaHei (Windows), or
Noto Sans CJK SC / WenQuanYi Micro Hei (Linux), in that auto-detection order.

## Geometry cheatsheet

| element                      | value                                      |
| ---------------------------- | ------------------------------------------ |
| page width                   | 1200 – 1400 px (1300 default)              |
| left/right margin            | 30 px                                      |
| section header height        | 60 px                                      |
| section frame corner radius  | 14 px                                      |
| block corner radius          | 12 px                                      |
| block min height (1-line)    | 70 px                                      |
| block min height (2-line)    | 85 px                                      |
| row gap (for step routing)   | ≥ 50 px (gives 20-25 px stubs both ends)   |
| section gap                  | ≥ 35 px (room for dashed centre arrow)     |
| arrow line width             | 1.6 – 1.7                                  |
| arrow head size              | 11                                         |
| arrow pad (head-to-box gap)  | 6 px                                       |

## Arrow routing rules

1. **Only orthogonal lines.** Diagonals are reserved for `extras` (text VS,
   etc.) — never for arrows.
2. **Every Y / T junction is a 3-segment path** (vertical → horizontal →
   vertical). If the final vertical stub would be < 18 px, push the
   destination row down until the stub is ≥ 20 px.
3. **Arrow heads do not enter the box.** The renderer auto-pads the final
   segment by `arrow_pad` (default 6 px); leave that intact.
4. **Dashed arrows are an exception, not a default.** Use them only for:
   - feedback / override links (e.g. 异常检测 → 灌溉建议输出)
   - inter-section gap arrows (auto-emitted by `between_sections`)
5. **Mid-y placement**: for two-source → one-target step joins, put the
   horizontal track at the midpoint between source-bottom and target-top, or
   one row's worth above the target — never on the target's top edge.

## Output / highlight rule

A block is "highlighted" iff it represents one of:

- the explicit **output** of a section (e.g. "输出：…")
- the **final conclusion** of the whole figure (e.g. 节水与稳产增质效果分析 → 生产应用优化建议)

Do **not** highlight intermediate processing blocks even if they "feel
important" — the highlight is a structural signal, not a visual emphasis.

## Anti-patterns (the renderer will let you make these, please don't)

- ❌ Block fills in any colour other than white or `output_bg`.
- ❌ Curved or diagonal connectors.
- ❌ Arrow heads landing on top of block text.
- ❌ Two-segment "L-shape" routing where a step join is expected.
- ❌ Numbered badges / icons in section headers (kept out for print clarity).
- ❌ Subtext at the same size as the block title — keep the 19/15 ratio.
