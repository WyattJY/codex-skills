#!/usr/bin/env python3
"""OCR an ordered image folder and write audit artifacts for Markdown rebuilding."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def iter_images(image_dir: Path, recursive: bool = False) -> list[Path]:
    pattern = "**/*" if recursive else "*"
    images = [
        p
        for p in image_dir.glob(pattern)
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images, key=lambda p: p.name)


def load_engine() -> tuple[str, Any]:
    try:
        from rapidocr import RapidOCR

        return "rapidocr", RapidOCR()
    except Exception as modern_error:
        try:
            from rapidocr_onnxruntime import RapidOCR

            return "rapidocr_onnxruntime", RapidOCR()
        except Exception as legacy_error:
            raise RuntimeError(
                "No supported OCR engine found. Run with: "
                "uv run --with rapidocr --with onnxruntime --with pillow python "
                "ocr_image_folder.py --image-dir <dir> --out-dir <dir>"
            ) from legacy_error


def normalize_modern_output(output: Any) -> list[dict[str, Any]]:
    boxes = output.boxes.tolist() if getattr(output, "boxes", None) is not None else []
    txts = list(getattr(output, "txts", None) or [])
    scores = list(getattr(output, "scores", None) or [])
    return normalize_items(zip(boxes, txts, scores))


def normalize_legacy_output(output: Any) -> list[dict[str, Any]]:
    result, _elapsed = output
    return normalize_items(result or [])


def normalize_items(items: Iterable[Any]) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    for item in items:
        box, text, score = item
        box = [[float(pt[0]), float(pt[1])] for pt in box]
        xs = [pt[0] for pt in box]
        ys = [pt[1] for pt in box]
        lines.append(
            {
                "text": str(text),
                "score": float(score),
                "box": box,
                "x": min(xs),
                "y": min(ys),
                "w": max(xs) - min(xs),
                "h": max(ys) - min(ys),
            }
        )
    lines.sort(key=lambda row: (round(row["y"] / 10) * 10, row["x"]))
    return lines


def run_ocr(image_dir: Path, out_dir: Path, prefix: str, recursive: bool) -> dict[str, Path]:
    image_dir = image_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    images = iter_images(image_dir, recursive=recursive)
    if not images:
        raise FileNotFoundError(f"No image files found under {image_dir}")

    engine_name, engine = load_engine()
    records: list[dict[str, Any]] = []

    for index, image_path in enumerate(images, 1):
        raw = engine(str(image_path))
        if engine_name == "rapidocr":
            lines = normalize_modern_output(raw)
        else:
            lines = normalize_legacy_output(raw)

        records.append(
            {
                "index": index,
                "filename": image_path.name,
                "path": str(image_path),
                "engine": engine_name,
                "lines": lines,
            }
        )
        print(f"{index:03d}/{len(images):03d} {image_path.name}: {len(lines)} lines")

    json_path = out_dir / f"{prefix}_ocr_results.json"
    dump_path = out_dir / f"{prefix}_ocr_dump.txt"
    scaffold_path = out_dir / f"{prefix}_ocr_scaffold.md"

    json_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    dump_parts: list[str] = []
    for rec in records:
        dump_parts.append(f"\n===== {rec['index']:03d} {rec['filename']} =====")
        dump_parts.extend(line["text"] for line in rec["lines"])
    dump_path.write_text("\n".join(dump_parts), encoding="utf-8")

    scaffold_parts = [
        "# OCR Scaffold",
        "",
        f"- Source image directory: `{image_dir}`",
        f"- Image count: {len(records)}",
        f"- OCR engine: {engine_name}",
        f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "> This is an intermediate scaffold only. Rebuild a continuous technical Markdown document from it.",
        "",
    ]
    for rec in records:
        image_path = Path(rec["path"])
        rel = image_path.name
        try:
            rel = image_path.relative_to(out_dir.parent).as_posix()
        except ValueError:
            pass
        scaffold_parts.extend(
            [
                f"## OCR {rec['index']:03d}. {rec['filename']}",
                "",
                f"![{rec['filename']}]({rel})",
                "",
                "```text",
                *[line["text"] for line in rec["lines"]],
                "```",
                "",
            ]
        )
    scaffold_path.write_text("\n".join(scaffold_parts), encoding="utf-8")

    return {"json": json_path, "dump": dump_path, "scaffold": scaffold_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-dir", required=True, type=Path, help="Image folder to OCR.")
    parser.add_argument("--out-dir", required=True, type=Path, help="Directory for OCR artifacts.")
    parser.add_argument("--prefix", default="image_doc", help="Output filename prefix.")
    parser.add_argument("--recursive", action="store_true", help="Scan image folder recursively.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = run_ocr(args.image_dir, args.out_dir, args.prefix, args.recursive)
    for label, path in outputs.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
