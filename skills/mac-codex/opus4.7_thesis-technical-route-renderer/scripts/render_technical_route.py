#!/usr/bin/env python3
"""
render_technical_route.py — render a thesis-style "技术路线图" (technical route
diagram) from a declarative JSON spec.

Outputs:
  * a high-DPI PNG suitable for direct insertion into a .docx
  * a matching .drawio source (XML) for future editing in app.diagrams.net

Usage:
    python render_technical_route.py --spec path/to/spec.json
    python render_technical_route.py --spec spec.json --png out.png --drawio out.drawio

Style: paper-friendly black / white / grey, rounded blocks, orthogonal
3-segment routing for Y / T junctions, dashed centre-line connectors between
sections, output blocks highlighted with a darker grey fill.

Dependencies (auto-detected if a CJK font is present):
    pip install matplotlib pillow
or use the included install helper:
    bash scripts/install_deps.sh

See `references/style.md` for design tokens; see `scripts/example_spec.json`
for a complete, ready-to-run example based on Wyatt's master-thesis Fig. 1-1.
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import os
import platform
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MplPath


# ---------------------------------------------------------------------------
# style tokens (overridable via spec["style"])
# ---------------------------------------------------------------------------
DEFAULT_STYLE = {
    "ink":          "#1F1F1F",
    "ink_soft":     "#555555",
    "stroke":       "#4A4A4A",
    "header":       "#2C2C2C",
    "header_text":  "#FFFFFF",
    "frame":        "#BBBBBB",
    "frame_bg":     "#FAFAFA",
    "block_bg":     "#FFFFFF",
    "output_bg":    "#E5E5E5",
    "output_stroke": "#3A3A3A",
    "arrow":        "#1F1F1F",
    "dashed_arrow": "#555555",
    "section_font_size": 24,
    "block_title_size": 19,
    "block_sub_size":   15,
    "arrow_lw":         1.7,
    "arrow_head":       11,
    "arrow_pad":        6,
    "block_radius":     12,
    "section_radius":   14,
    "header_height":    60,
}


# ---------------------------------------------------------------------------
# Font selection — find a font that supports CJK on Mac / Windows / Linux
# ---------------------------------------------------------------------------
CJK_CANDIDATES = {
    "Darwin": [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ],
    "Windows": [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ],
    "Linux": [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
    ],
}
CJK_FAMILY_PREF = [
    "Hiragino Sans GB", "STHeiti", "PingFang SC",
    "Microsoft YaHei", "SimHei", "SimSun",
    "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Micro Hei",
    "Arial Unicode MS", "DejaVu Sans",
]


def setup_fonts() -> None:
    sysname = platform.system()
    for path in CJK_CANDIDATES.get(sysname, []):
        if os.path.exists(path):
            try:
                font_manager.fontManager.addfont(path)
            except Exception:
                pass
    plt.rcParams["font.family"] = CJK_FAMILY_PREF
    plt.rcParams["axes.unicode_minus"] = False


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------
def rrect(ax, x, y, w, h, *, fill, edge, lw=1.4, r=10, zorder=2):
    r = min(r, w / 2, h / 2)
    verts = [(x + r, y), (x + w - r, y), (x + w, y), (x + w, y + r),
             (x + w, y + h - r), (x + w, y + h), (x + w - r, y + h),
             (x + r, y + h), (x, y + h), (x, y + h - r),
             (x, y + r), (x, y), (x + r, y)]
    codes = [MplPath.MOVETO, MplPath.LINETO,
             MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO,
             MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO,
             MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO,
             MplPath.CURVE3, MplPath.CURVE3]
    ax.add_patch(PathPatch(MplPath(verts, codes),
                           facecolor=fill, edgecolor=edge,
                           linewidth=lw, zorder=zorder))


def text(ax, cx, cy, s, *, size, color, weight="bold",
         ha="center", va="center", zorder=4):
    ax.text(cx, cy, s, fontsize=size, color=color, weight=weight,
            ha=ha, va=va, zorder=zorder, linespacing=1.4)


def arrow_head(ax, x1, y1, x2, y2, *, color, head=11):
    dx, dy = x2 - x1, y2 - y1
    L = max((dx * dx + dy * dy) ** 0.5, 1e-6)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    bx, by = x2 - ux * head, y2 - uy * head
    tri = plt.Polygon([(x2, y2),
                       (bx + px * head * 0.5, by + py * head * 0.5),
                       (bx - px * head * 0.5, by - py * head * 0.5)],
                      closed=True, facecolor=color, edgecolor=color, zorder=6)
    ax.add_patch(tri)


def orth_path(ax, points, *, color, dashed=False, lw=1.7, head=11, pad=6,
              record=None):
    """Polyline with arrow head at the last segment.

    The final segment is shortened by ``pad`` so the arrow head doesn't intrude
    into the destination box. The (unmodified) points are appended to
    ``record`` so they can be emitted to drawio later.
    """
    if record is not None:
        record.append({"points": [tuple(p) for p in points], "dashed": dashed})

    if len(points) >= 2:
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        dx, dy = x2 - x1, y2 - y1
        L = max((dx * dx + dy * dy) ** 0.5, 1e-6)
        ux, uy = dx / L, dy / L
        new_end = (x2 - ux * pad, y2 - uy * pad)
        draw_pts = list(points[:-1]) + [new_end]
    else:
        draw_pts = list(points)

    style = (0, (6, 4)) if dashed else "-"
    for i in range(len(draw_pts) - 1):
        ax.plot([draw_pts[i][0], draw_pts[i + 1][0]],
                [draw_pts[i][1], draw_pts[i + 1][1]],
                linestyle=style, color=color, linewidth=lw, zorder=5,
                solid_capstyle="round")
    arrow_head(ax, draw_pts[-2][0], draw_pts[-2][1],
               draw_pts[-1][0], draw_pts[-1][1],
               color=color, head=head)


# ---------------------------------------------------------------------------
# Spec helpers
# ---------------------------------------------------------------------------
def anchor_x(box, ratio):
    return box["x"] + box["w"] * ratio


def anchor_y_top(box):
    return box["y"]


def anchor_y_bot(box):
    return box["y"] + box["h"]


def build_arrow_points(arrow_spec, box_index):
    src = box_index[arrow_spec["from"]]
    dst = box_index[arrow_spec["to"]]
    a_from = arrow_spec.get("from_anchor", 0.5)
    a_to   = arrow_spec.get("to_anchor", 0.5)
    style  = arrow_spec.get("type", "auto")  # straight | step | side | custom

    if style == "custom":
        return [tuple(p) for p in arrow_spec["points"]]

    if style == "side":
        # horizontal connector at the source's vertical midpoint (or specified y)
        side = arrow_spec.get("side", "right")     # 'right' or 'left'
        mid_y = arrow_spec.get("mid_y",
                               src["y"] + src["h"] / 2)
        if side == "right":
            x0 = src["x"] + src["w"]
            x1 = dst["x"]
        else:
            x0 = src["x"]
            x1 = dst["x"] + dst["w"]
        return [(x0, mid_y), (x1, mid_y)]

    sx = anchor_x(src, a_from)
    sy = anchor_y_bot(src)
    dx = anchor_x(dst, a_to)
    dy = anchor_y_top(dst)

    if style == "straight" or (style == "auto" and abs(sx - dx) < 1e-3):
        return [(sx, sy), (dx, dy)]

    # step (Y / T routing): vertical → horizontal → vertical
    mid_y = arrow_spec.get("mid_y", (sy + dy) / 2)
    return [(sx, sy), (sx, mid_y), (dx, mid_y), (dx, dy)]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def render(spec: dict, png_path: str | None, drawio_path: str | None) -> None:
    style = dict(DEFAULT_STYLE)
    style.update(spec.get("style", {}))
    setup_fonts()

    canvas = spec.get("canvas", {})
    W = canvas.get("width", 1300)
    DPI = canvas.get("dpi", 200)
    auto_height = canvas.get("auto_height", True)
    H_explicit = canvas.get("height")

    sections = spec["sections"]
    arrows_in = spec.get("arrows", [])
    between = spec.get("between_sections", [])
    extras = spec.get("extras", [])  # free-form text labels

    # Compute height
    if auto_height:
        max_y = 0
        for sec in sections:
            max_y = max(max_y, sec["y"] + sec["height"])
            for blk in sec.get("blocks", []):
                max_y = max(max_y, blk["y"] + blk["h"])
        H = int(max_y + canvas.get("bottom_padding", 20))
    else:
        H = H_explicit or 1800

    fig = plt.figure(figsize=(W / 100, H / 100), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.set_axis_off()

    arrows_record = []
    box_index = {}

    # ----- sections + their blocks
    section_records = []
    for sec in sections:
        sx = sec.get("x", spec.get("canvas", {}).get("left_margin", 30))
        sw = sec.get("w", W - 2 * sx)
        sy = sec["y"]
        sh = sec["height"]
        title = sec.get("title", "")

        rrect(ax, sx, sy, sw, sh,
              fill=style["frame_bg"], edge=style["frame"],
              lw=1.0, r=style["section_radius"], zorder=1)
        # header bar (with covered bottom so it sits flush)
        hh = style["header_height"]
        rrect(ax, sx, sy, sw, hh,
              fill=style["header"], edge=style["header"], lw=0,
              r=style["section_radius"], zorder=3)
        ax.add_patch(Rectangle((sx, sy + hh / 2), sw, hh / 2,
                               facecolor=style["header"], edgecolor="none",
                               zorder=3))
        text(ax, sx + sw / 2, sy + hh / 2, title,
             size=style["section_font_size"], color=style["header_text"])
        section_records.append({"id": sec.get("id", f"sec_{len(section_records)+1}"),
                                "x": sx, "y": sy, "w": sw, "h": sh,
                                "title": title})

        for blk in sec.get("blocks", []):
            box_index[blk["id"]] = blk
            highlight = bool(blk.get("highlight"))
            fill = style["output_bg"] if highlight else style["block_bg"]
            edge = style["output_stroke"] if highlight else style["stroke"]
            rrect(ax, blk["x"], blk["y"], blk["w"], blk["h"],
                  fill=fill, edge=edge, lw=1.6,
                  r=style["block_radius"], zorder=4)
            cx = blk["x"] + blk["w"] / 2
            cy = blk["y"] + blk["h"] / 2
            sub = blk.get("sub")
            if sub:
                text(ax, cx, cy - 13, blk["title"],
                     size=style["block_title_size"], color=style["ink"])
                text(ax, cx, cy + 16, sub,
                     size=style["block_sub_size"], color=style["ink_soft"],
                     weight="normal")
            else:
                text(ax, cx, cy, blk["title"],
                     size=style["block_title_size"], color=style["ink"])

    # ----- in-section / cross-section arrows declared in arrows[]
    for a in arrows_in:
        pts = build_arrow_points(a, box_index)
        color = (style["dashed_arrow"] if a.get("dashed")
                 else style["arrow"])
        orth_path(ax, pts,
                  color=color,
                  dashed=bool(a.get("dashed", False)),
                  lw=a.get("lw", style["arrow_lw"]),
                  head=style["arrow_head"],
                  pad=a.get("pad", style["arrow_pad"]),
                  record=arrows_record)

    # ----- automatic dashed gap arrows between sequential sections
    for gap in between:
        sec_from = next(s for s in section_records if s["id"] == gap["from_section"])
        sec_to   = next(s for s in section_records if s["id"] == gap["to_section"])
        cx = sec_from["x"] + sec_from["w"] / 2
        y_top = sec_from["y"] + sec_from["h"] + 5
        y_bot = sec_to["y"] - 5
        orth_path(ax, [(cx, y_top), (cx, y_bot)],
                  color=style["dashed_arrow"], dashed=True, lw=2.0,
                  head=12, pad=10, record=arrows_record)

    # ----- free-form text labels
    for ex in extras:
        if ex.get("type") == "label":
            text(ax, ex["x"], ex["y"], ex["text"],
                 size=ex.get("size", 24),
                 color=ex.get("color", style["ink"]),
                 weight=ex.get("weight", "bold"))

    # ----- write PNG
    if png_path:
        Path(png_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(png_path, dpi=DPI, bbox_inches=None, pad_inches=0,
                    facecolor="white")
        print(f"[ok] PNG    {png_path}")
    plt.close(fig)

    # ----- write .drawio
    if drawio_path:
        Path(drawio_path).parent.mkdir(parents=True, exist_ok=True)
        Path(drawio_path).write_text(
            build_drawio_xml(W, H, section_records, box_index,
                             arrows_record, extras, style),
            encoding="utf-8")
        print(f"[ok] DRAWIO {drawio_path}")


# ---------------------------------------------------------------------------
# Drawio XML emission
# ---------------------------------------------------------------------------
def esc(s: str | None) -> str:
    return html_mod.escape(s or "", quote=True)


def block_html(title: str, sub: str | None) -> str:
    if sub:
        return (f"&lt;b&gt;{esc(title)}&lt;/b&gt;"
                f"&lt;br&gt;&lt;font style=&quot;font-size:13px&quot; "
                f"color=&quot;#555555&quot;&gt;{esc(sub)}&lt;/font&gt;")
    return f"&lt;b&gt;{esc(title)}&lt;/b&gt;"


def build_drawio_xml(W, H, section_records, box_index, arrows_record,
                     extras, style) -> str:
    cells: list[str] = []

    # sections
    for s in section_records:
        frame_style = (f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;"
                       f"fillColor={style['frame_bg']};"
                       f"strokeColor={style['frame']};strokeWidth=1.0;")
        head_style = (f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;"
                      f"fillColor={style['header']};"
                      f"strokeColor={style['header']};"
                      f"align=center;verticalAlign=middle;fontSize=18;"
                      f"fontStyle=1;fontColor={style['header_text']};")
        cells.append(
            f'        <mxCell id="bg_{s["id"]}" value="" style="{frame_style}" '
            f'vertex="1" parent="1">\n'
            f'          <mxGeometry x="{s["x"]}" y="{s["y"]}" '
            f'width="{s["w"]}" height="{s["h"]}" as="geometry" />\n'
            f'        </mxCell>'
        )
        cells.append(
            f'        <mxCell id="h_{s["id"]}" value="{esc(s["title"])}" '
            f'style="{head_style}" vertex="1" parent="1">\n'
            f'          <mxGeometry x="{s["x"]}" y="{s["y"]}" '
            f'width="{s["w"]}" height="{style["header_height"]}" as="geometry" />\n'
            f'        </mxCell>'
        )

    # blocks
    for blk in box_index.values():
        highlight = bool(blk.get("highlight"))
        fill = style["output_bg"] if highlight else style["block_bg"]
        stroke = style["output_stroke"] if highlight else style["stroke"]
        s_style = (f"rounded=1;arcSize=10;whiteSpace=wrap;html=1;"
                   f"fillColor={fill};strokeColor={stroke};strokeWidth=1.5;"
                   f"align=center;verticalAlign=middle;fontSize=15;fontStyle=1;")
        val = block_html(blk["title"], blk.get("sub"))
        cells.append(
            f'        <mxCell id="{blk["id"]}" value="{val}" '
            f'style="{s_style}" vertex="1" parent="1">\n'
            f'          <mxGeometry x="{blk["x"]}" y="{blk["y"]}" '
            f'width="{blk["w"]}" height="{blk["h"]}" as="geometry" />\n'
            f'        </mxCell>'
        )

    # text labels
    for i, ex in enumerate(extras):
        if ex.get("type") != "label":
            continue
        lw = ex.get("box_w", 100)
        lh = ex.get("box_h", 50)
        lx = ex["x"] - lw / 2
        ly = ex["y"] - lh / 2
        size = ex.get("size", 24)
        color = ex.get("color", style["ink"])
        s_style = (f"text;html=1;strokeColor=none;fillColor=none;"
                   f"align=center;verticalAlign=middle;fontSize={size};"
                   f"fontStyle=1;fontColor={color};")
        cells.append(
            f'        <mxCell id="label_{i}" value="&lt;b&gt;{esc(ex["text"])}&lt;/b&gt;" '
            f'style="{s_style}" vertex="1" parent="1">\n'
            f'          <mxGeometry x="{lx}" y="{ly}" width="{lw}" '
            f'height="{lh}" as="geometry" />\n'
            f'        </mxCell>'
        )

    # edges
    for i, edge in enumerate(arrows_record):
        pts = edge["points"]
        dashed = edge["dashed"]
        e_style = ("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
                   "jettySize=auto;html=1;"
                   f"strokeColor={style['arrow']};strokeWidth=1.6;"
                   "endArrow=block;endFill=1;endSize=8;")
        if dashed:
            e_style = (e_style.replace(
                f"strokeColor={style['arrow']}",
                f"strokeColor={style['dashed_arrow']}") +
                "dashed=1;dashPattern=6 4;")
        sx, sy = pts[0]
        ex_, ey_ = pts[-1]
        wp = "\n".join([f'              <mxPoint x="{p[0]}" y="{p[1]}" />'
                        for p in pts[1:-1]])
        array = (f'            <Array as="points">\n{wp}\n'
                 f'            </Array>\n' if wp else "")
        cells.append(
            f'        <mxCell id="e_{i}" style="{e_style}" '
            f'edge="1" parent="1">\n'
            f'          <mxGeometry relative="1" as="geometry">\n'
            f'            <mxPoint x="{sx}" y="{sy}" as="sourcePoint" />\n'
            f'            <mxPoint x="{ex_}" y="{ey_}" as="targetPoint" />\n'
            f'{array}'
            f'          </mxGeometry>\n'
            f'        </mxCell>'
        )

    return (
        '<mxfile host="app.diagrams.net" agent="thesis-technical-route-renderer" '
        'version="29.6.6">\n'
        '  <diagram name="技术路线图" id="tech-route">\n'
        f'    <mxGraphModel dx="1854" dy="1180" grid="1" gridSize="10" '
        f'guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" '
        f'pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">\n'
        '      <root>\n'
        '        <mxCell id="0" />\n'
        '        <mxCell id="1" parent="0" />\n'
        + "\n".join(cells) + "\n"
        '      </root>\n'
        '    </mxGraphModel>\n'
        '  </diagram>\n'
        '</mxfile>\n'
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Render a thesis-style technical-route diagram from a JSON spec.")
    p.add_argument("--spec", required=True,
                   help="Path to the JSON spec file.")
    p.add_argument("--png", default=None,
                   help="Output PNG path. Defaults to <spec_basename>.png next "
                        "to the spec file.")
    p.add_argument("--drawio", default=None,
                   help="Output .drawio path. Defaults to <spec_basename>.drawio "
                        "next to the spec file.")
    p.add_argument("--no-drawio", action="store_true",
                   help="Skip emitting the .drawio file.")
    args = p.parse_args(argv)

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"error: spec file not found: {spec_path}", file=sys.stderr)
        return 2
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    base = spec_path.with_suffix("")
    png_path = args.png or str(base) + ".png"
    drawio_path = None if args.no_drawio else (args.drawio or str(base) + ".drawio")

    render(spec, png_path, drawio_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
