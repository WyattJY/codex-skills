#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import struct
import time
from collections import Counter, defaultdict
from pathlib import Path


def image_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()[:64]
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            return struct.unpack(">II", data[16:24])
        if data[:2] == b"\xff\xd8":
            with path.open("rb") as f:
                f.read(2)
                while True:
                    marker = f.read(2)
                    if len(marker) < 2:
                        return None
                    while marker[0] != 0xFF:
                        marker = marker[1:] + f.read(1)
                    code = marker[1]
                    size = struct.unpack(">H", f.read(2))[0]
                    if code in {0xC0, 0xC2}:
                        f.read(1)
                        h, w = struct.unpack(">HH", f.read(4))
                        return w, h
                    f.seek(size - 2, 1)
    except Exception:
        return None
    return None


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    values = sorted(values)
    idx = min(len(values) - 1, max(0, round((len(values) - 1) * pct)))
    return values[idx]


def safe_label(value: str, show: bool) -> str:
    if show:
        return value[:80]
    return "sha1:" + hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()[:10]


def profile_csv(path: Path, show_labels: bool, max_rows: int) -> dict:
    rows = 0
    missing = Counter()
    lengths: dict[str, list[int]] = defaultdict(list)
    label_counts = Counter()
    with path.open(newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        label_col = next((c for c in columns if c.lower() in {"label", "class", "category", "target"}), "")
        for row in reader:
            rows += 1
            if rows > max_rows:
                break
            for col in columns:
                val = row.get(col, "")
                if val == "":
                    missing[col] += 1
                lengths[col].append(len(val or ""))
            if label_col:
                label_counts[safe_label(row.get(label_col, ""), show_labels)] += 1
    return {
        "type": "csv",
        "path": str(path),
        "rows_sampled": rows,
        "columns": columns,
        "missing": dict(missing.most_common(20)),
        "length_p50": {k: percentile(v, 0.50) for k, v in lengths.items()},
        "length_p95": {k: percentile(v, 0.95) for k, v in lengths.items()},
        "labels_top": dict(label_counts.most_common(20)),
    }


def profile_jsonl(path: Path, show_labels: bool, max_rows: int) -> dict:
    rows = 0
    keys = Counter()
    text_lengths = []
    label_counts = Counter()
    with path.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            if rows >= max_rows:
                break
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows += 1
            if isinstance(obj, dict):
                keys.update(obj.keys())
                for key in ("text", "content", "query", "answer", "caption"):
                    if key in obj and isinstance(obj[key], str):
                        text_lengths.append(len(obj[key]))
                for key in ("label", "class", "category", "target"):
                    if key in obj:
                        label_counts[safe_label(str(obj[key]), show_labels)] += 1
    return {
        "type": "jsonl",
        "path": str(path),
        "rows_sampled": rows,
        "keys_top": dict(keys.most_common(50)),
        "text_length_p50": percentile(text_lengths, 0.50),
        "text_length_p95": percentile(text_lengths, 0.95),
        "labels_top": dict(label_counts.most_common(20)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate-only dataset profiler.")
    parser.add_argument("path")
    parser.add_argument("--out", default="")
    parser.add_argument("--max-rows", type=int, default=10000)
    parser.add_argument("--show-label-values", action="store_true")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file() and not p.name.startswith("._")]
    by_ext = Counter(p.suffix.lower() or "<none>" for p in files)
    profiles = []
    image_dims = []
    for p in files[:5000]:
        suffix = p.suffix.lower()
        if suffix == ".csv":
            profiles.append(profile_csv(p, args.show_label_values, args.max_rows))
        elif suffix in {".jsonl", ".ndjson"}:
            profiles.append(profile_jsonl(p, args.show_label_values, args.max_rows))
        elif suffix in {".png", ".jpg", ".jpeg"}:
            size = image_size(p)
            if size:
                image_dims.append(size)

    widths = [w for w, _h in image_dims]
    heights = [h for _w, h in image_dims]
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    out_path = Path(args.out) if args.out else root / "DATA_CARD.md"
    md = [
        "# DATA_CARD",
        "",
        f"- generated_at: {now}",
        f"- dataset_path: `{root}`",
        f"- files_count: {len(files)}",
        "",
        "## File Types",
        "",
        "| extension | count |",
        "|---|---:|",
        *[f"| {ext} | {count} |" for ext, count in by_ext.most_common()],
        "",
        "## Image Dimensions",
        "",
        f"- images_profiled: {len(image_dims)}",
        f"- width_p50/p95: {percentile(widths, 0.50)} / {percentile(widths, 0.95)}",
        f"- height_p50/p95: {percentile(heights, 0.50)} / {percentile(heights, 0.95)}",
        "",
        "## Structured Files",
        "```json",
        json.dumps(profiles[:20], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Safety Notes",
        "- This card contains aggregate metadata only.",
        "- Raw rows, raw samples, raw images, credentials, cookies, and tokens were not exported.",
        "- Label values are hashed unless `--show-label-values` is explicitly used.",
    ]
    out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()

