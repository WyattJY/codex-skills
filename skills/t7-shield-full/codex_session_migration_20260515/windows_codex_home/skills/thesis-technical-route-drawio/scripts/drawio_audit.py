#!/usr/bin/env python3
"""
Audit a Draw.io (.drawio) file for thesis-style "technical route" diagrams.

Checks:
- Vertex/edge inventory
- Edges missing orthogonal styling / arrow sizing
- Edges with manual routing points (often indicates extra bends)
- Connected-shape gaps that are too small (arrowhead can hide the line)
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    w: float
    h: float
    value: str

    @property
    def x2(self) -> float:
        return self.x + self.w

    @property
    def y2(self) -> float:
        return self.y + self.h


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a Draw.io (.drawio) file for common technical-route figure issues."
    )
    parser.add_argument("path", type=Path, help="Path to a .drawio file")
    parser.add_argument(
        "--gap-threshold",
        type=float,
        default=30.0,
        help="Warn when a connected shapes' horizontal/vertical gap is below this threshold (px).",
    )
    parser.add_argument(
        "--show-all-edges",
        action="store_true",
        help="Print every edge (otherwise only warnings).",
    )
    return parser.parse_args()


def get_geometry(cell: ET.Element) -> tuple[float, float, float, float] | None:
    geo = cell.find("mxGeometry")
    if geo is None:
        return None
    x = float(geo.get("x") or 0)
    y = float(geo.get("y") or 0)
    w = float(geo.get("width") or 0)
    h = float(geo.get("height") or 0)
    return x, y, w, h


def rect_gap(a: Rect, b: Rect) -> tuple[float, float]:
    gap_x = 0.0
    if a.x2 < b.x:
        gap_x = b.x - a.x2
    elif b.x2 < a.x:
        gap_x = a.x - b.x2

    gap_y = 0.0
    if a.y2 < b.y:
        gap_y = b.y - a.y2
    elif b.y2 < a.y:
        gap_y = a.y - b.y2

    return gap_x, gap_y


def normalize_value(value: str) -> str:
    return (
        (value or "")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "/")
        .replace("<br>", "/")
        .strip()
    )


def main() -> int:
    args = parse_args()
    if not args.path.exists():
        print(f"[error] File not found: {args.path}", file=sys.stderr)
        return 2

    root = ET.fromstring(args.path.read_text(encoding="utf-8"))
    cells = root.findall(".//mxCell")
    by_id: dict[str, ET.Element] = {c.get("id"): c for c in cells if c.get("id")}

    vertices: dict[str, Rect] = {}
    edges: list[ET.Element] = []
    for c in cells:
        if c.get("vertex") == "1":
            geo = get_geometry(c)
            if geo is None:
                continue
            x, y, w, h = geo
            vertices[c.get("id")] = Rect(x=x, y=y, w=w, h=h, value=normalize_value(c.get("value") or ""))
        elif c.get("edge") == "1":
            edges.append(c)

    print(f"[info] vertices={len(vertices)} edges={len(edges)}")

    warnings: list[str] = []

    for e in edges:
        edge_id = e.get("id") or "<?>"
        src = e.get("source")
        tgt = e.get("target")
        style = e.get("style") or ""
        geo = e.find("mxGeometry")

        has_points = geo is not None and geo.find("Array") is not None

        if "edgeStyle=orthogonalEdgeStyle" not in style:
            warnings.append(f"[warn] {edge_id}: non-orthogonal edgeStyle")
        if "endArrow=classic" in style and "endSize=" not in style:
            warnings.append(f"[warn] {edge_id}: missing endSize (arrowhead can hide line)")
        if "rounded=1" in style or "curved=1" in style:
            warnings.append(f"[warn] {edge_id}: rounded/curved edge (prefer straight orthogonal)")

        if has_points:
            warnings.append(f"[warn] {edge_id}: has manual routing points (may introduce extra bends)")

        if src and tgt and src in vertices and tgt in vertices:
            gap_x, gap_y = rect_gap(vertices[src], vertices[tgt])
            if (gap_x and gap_x < args.gap_threshold) or (gap_y and gap_y < args.gap_threshold):
                warnings.append(
                    f"[warn] {edge_id}: small gap (x={gap_x:.0f}, y={gap_y:.0f}) "
                    f"{src}('{vertices[src].value}') -> {tgt}('{vertices[tgt].value}')"
                )

        if args.show_all_edges:
            print(
                f"[edge] {edge_id}: {src or '<srcPoint>'} -> {tgt or '<tgtPoint>'}"
                f"{' [points]' if has_points else ''}"
            )

    if warnings:
        print("\n".join(warnings))
        print(f"[info] warnings={len(warnings)}")
        return 1

    print("[info] no warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

