#!/usr/bin/env python3
"""Check synthesized Obsidian course-note quality signals.

This complements check_markdown_assets.py. It catches notes that look polished
but forgot the required Obsidian teaching callouts or deep teaching structure.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


CALLOUT_RE = re.compile(r"^>\s*\[!([A-Za-z]+)\](?:\s+(.+))?$", re.MULTILINE)
MECHANICAL_RE = re.compile(r"(音频依据：|涂鸦识别：|老师在\s*\d{1,2}:\d{2})")
TRANSCRIPT_HEADING_RE = re.compile(
    r"^(##\s+辅助摘要|##\s+短分段逐字稿|###\s+\[\d{2}:\d{2}:\d{2})",
    re.MULTILINE,
)
HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$", re.MULTILINE)
TOC_RE = re.compile(r"\[\[#([^|\]]+)(?:\|[^\]]*)?\]\]")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\((?:<([^>]+)>|([^)]+))\)")
SOURCE_ANCHOR_RE = re.compile(r"(源码位置：|脚本：|vscode://file)")
PEDAGOGICAL_RE = re.compile(r"(为什么|机制|证据|证明|解决|关键|shape|源码位置：|本章小结)")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}

DEFAULT_REQUIRED_HEADINGS = [
    "先给结论",
    "课程承接",
    "学习地图",
    "复盘动作",
    "自测题",
]

CAPTION_HINT_RE = re.compile(
    r"(这张图|图中|图里|补充图|截图|白板|板书|曲线|结构|展示|说明|解释|证明|对比|对应)"
)


def count_callouts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for match in CALLOUT_RE.finditer(text):
        key = match.group(1).lower()
        counts[key] = counts.get(key, 0) + 1
    return counts


def heading_names(text: str) -> set[str]:
    return {match.group(2).strip() for match in HEADING_RE.finditer(text)}


def local_image_links(text: str) -> list[str]:
    links: list[str] = []
    for match in IMAGE_RE.finditer(text):
        target = (match.group(1) or match.group(2) or "").strip()
        if not target:
            continue
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target):
            continue
        links.append(target)
    return links


def image_link_names(text: str) -> set[str]:
    names: set[str] = set()
    for link in local_image_links(text):
        clean = unquote(link).split("#", 1)[0].split("?", 1)[0]
        name = Path(clean).name
        if name:
            names.add(name)
    return names


def asset_image_names(asset_dirs: list[Path]) -> list[str]:
    names: set[str] = set()
    for raw_dir in asset_dirs:
        asset_dir = raw_dir.expanduser().resolve()
        if not asset_dir.exists():
            continue
        for path in asset_dir.rglob("*"):
            if not path.is_file():
                continue
            if path.name.startswith("._"):
                continue
            if path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            names.add(path.name)
    return sorted(names)


def check_toc_targets(text: str) -> list[str]:
    headings = heading_names(text)
    missing: list[str] = []
    for target in TOC_RE.findall(text):
        target = target.strip()
        if target and target not in headings:
            missing.append(target)
    return missing


def nonempty_following_lines(lines: list[str], start: int, limit: int = 4) -> list[str]:
    found: list[str] = []
    for line in lines[start : start + 12]:
        stripped = line.strip()
        if not stripped:
            continue
        found.append(stripped)
        if len(found) >= limit:
            break
    return found


def check_image_captions(text: str) -> list[str]:
    failures: list[str] = []
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if not IMAGE_RE.search(line):
            continue
        following = nonempty_following_lines(lines, idx + 1, limit=2)
        if not following:
            failures.append(f"image at line {idx + 1} has no explanatory caption")
            continue
        caption = following[0]
        if caption.startswith(("!", "#", ">", "|")) or len(caption) < 18:
            failures.append(f"image at line {idx + 1} lacks nearby prose explanation")
            continue
        if not CAPTION_HINT_RE.search(caption):
            failures.append(f"image at line {idx + 1} caption does not explain teaching value")
    return failures


def check_code_source_adjacency(text: str) -> list[str]:
    failures: list[str] = []
    lines = text.splitlines()
    in_code = False
    start_line = 0
    fence_header = ""
    for idx, line in enumerate(lines):
        if not line.startswith("```"):
            continue
        if not in_code:
            in_code = True
            start_line = idx + 1
            fence_header = line.strip().lower()
            continue
        in_code = False
        if fence_header in {"```mermaid", "```dot"}:
            continue
        following = "\n".join(nonempty_following_lines(lines, idx + 1, limit=4))
        if not SOURCE_ANCHOR_RE.search(following):
            failures.append(
                f"code block without adjacent source anchor: lines {start_line}-{idx + 1}"
            )
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("note", type=Path)
    parser.add_argument("--min-important", type=int, default=2)
    parser.add_argument("--min-warning", type=int, default=1)
    parser.add_argument("--min-total-callouts", type=int, default=4)
    parser.add_argument("--min-local-images", type=int, default=1)
    parser.add_argument("--min-source-anchors", type=int, default=1)
    parser.add_argument("--min-chapter-summaries", type=int, default=1)
    parser.add_argument("--min-pedagogical-markers", type=int, default=6)
    parser.add_argument(
        "--require-heading",
        action="append",
        default=[],
        help="Additional heading text that must exist exactly.",
    )
    parser.add_argument("--no-require-info", action="store_true")
    parser.add_argument(
        "--no-deep-structure",
        action="store_true",
        help="Skip RoPE-grade teaching-structure checks for legitimate short notes.",
    )
    parser.add_argument(
        "--asset-dir",
        action="append",
        default=[],
        type=Path,
        help="Lesson asset directory whose non-hidden image files must all be referenced.",
    )
    args = parser.parse_args(argv)

    note = args.note.expanduser().resolve()
    if not note.exists():
        print(f"missing markdown: {note}", file=sys.stderr)
        return 2

    text = note.read_text(encoding="utf-8")
    counts = count_callouts(text)
    total = sum(counts.values())
    failures: list[str] = []

    if not args.no_require_info and counts.get("info", 0) < 1:
        failures.append("missing required > [!info] source/provenance callout")
    if counts.get("important", 0) < args.min_important:
        failures.append(
            f"important callouts too few: {counts.get('important', 0)} < {args.min_important}"
        )
    if counts.get("warning", 0) < args.min_warning:
        failures.append(
            f"warning callouts too few: {counts.get('warning', 0)} < {args.min_warning}"
        )
    if total < args.min_total_callouts:
        failures.append(f"total callouts too few: {total} < {args.min_total_callouts}")
    if MECHANICAL_RE.search(text):
        failures.append("mechanical labels or timestamp narration remain in main note")
    if TRANSCRIPT_HEADING_RE.search(text):
        failures.append("transcript sections appear to be embedded in the main note")

    if not args.no_deep_structure:
        headings = heading_names(text)
        for required in [*DEFAULT_REQUIRED_HEADINGS, *args.require_heading]:
            if not any(required in heading for heading in headings):
                failures.append(f"missing required heading: {required}")

        images = local_image_links(text)
        if len(images) < args.min_local_images:
            failures.append(
                f"local image links too few: {len(images)} < {args.min_local_images}"
            )
        failures.extend(check_image_captions(text))

        asset_images = asset_image_names(args.asset_dir)
        linked_image_names = image_link_names(text)
        unused_assets = [
            image_name for image_name in asset_images if image_name not in linked_image_names
        ]
        if unused_assets:
            failures.append("unused asset images: " + ", ".join(unused_assets))

        source_anchors = len(SOURCE_ANCHOR_RE.findall(text))
        if source_anchors < args.min_source_anchors:
            failures.append(
                f"source anchors too few: {source_anchors} < {args.min_source_anchors}"
            )

        chapter_summaries = text.count("### 本章小结")
        if chapter_summaries < args.min_chapter_summaries:
            failures.append(
                f"chapter summaries too few: {chapter_summaries} < {args.min_chapter_summaries}"
            )

        pedagogical_markers = len(PEDAGOGICAL_RE.findall(text))
        if pedagogical_markers < args.min_pedagogical_markers:
            failures.append(
                "pedagogical markers too few: "
                f"{pedagogical_markers} < {args.min_pedagogical_markers}"
            )

        for missing in check_toc_targets(text):
            failures.append(f"TOC target missing: {missing}")

        failures.extend(check_code_source_adjacency(text))

    print(f"markdown={note}")
    print(f"callouts_total={total}")
    for key in sorted(counts):
        print(f"callout_{key}={counts[key]}")
    if not args.no_deep_structure:
        print(f"local_image_links={len(local_image_links(text))}")
        if args.asset_dir:
            asset_images = asset_image_names(args.asset_dir)
            unused_assets = [
                image_name
                for image_name in asset_images
                if image_name not in image_link_names(text)
            ]
            print(f"asset_images_total={len(asset_images)}")
            print(f"asset_images_used={len(asset_images) - len(unused_assets)}")
            print(f"unused_asset_images={len(unused_assets)}")
        print(f"source_anchors={len(SOURCE_ANCHOR_RE.findall(text))}")
        print(f"chapter_summaries={text.count('### 本章小结')}")
        print(f"pedagogical_markers={len(PEDAGOGICAL_RE.findall(text))}")
    print(f"failures={len(failures)}")
    for failure in failures:
        print(f"FAIL {failure}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
