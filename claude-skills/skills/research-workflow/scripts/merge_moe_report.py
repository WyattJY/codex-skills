from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


TITLE_BLACKLIST = {
    "abstract",
    "introduction",
    "method",
    "methods",
    "related work",
    "related works",
    "overview",
    "preliminaries",
}

NOTICE_PREFIXES = (
    "this cvpr paper is the open access version",
    "except for this watermark",
)


@dataclass(frozen=True)
class PaperRecord:
    folder: Path
    title: str
    authors: str
    norm_title: str
    compact_title: str
    norm_folder: str
    compact_folder: str


def clean_inline_text(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^\s*#+\s*", "", value)
    value = value.strip("* ").strip()
    return value


def normalize_text(value: str) -> str:
    value = clean_inline_text(value)
    value = re.sub(r"^\[\d{4}\]\s*", "", value)
    value = value.casefold()
    value = value.replace("&", " and ")
    value = value.replace("_", " ")
    value = value.replace("-", " ")
    value = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def compact_text(value: str) -> str:
    return re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "", normalize_text(value))


def is_image_or_empty(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("![") or stripped.startswith("<img")


def is_title_candidate(text: str) -> bool:
    lowered = text.casefold()
    if lowered in TITLE_BLACKLIST:
        return False
    if any(lowered.startswith(prefix) for prefix in NOTICE_PREFIXES):
        return False
    if lowered.startswith("figure ") or lowered.startswith("table "):
        return False
    if len(text) > 220:
        return False
    return bool(re.search(r"[A-Za-z\u4e00-\u9fff]{3,}", text))


def extract_title_and_authors(paper_dir: Path) -> tuple[str, str]:
    paper_md_path = paper_dir / "paper.md"
    fallback_title = paper_dir.name
    fallback_authors = "Unknown Authors"

    if not paper_md_path.is_file():
        return fallback_title, fallback_authors

    try:
        raw_lines = paper_md_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return fallback_title, fallback_authors

    title = fallback_title
    authors = fallback_authors
    title_index: int | None = None

    for idx, raw in enumerate(raw_lines[:120]):
        if is_image_or_empty(raw):
            continue

        stripped = raw.strip()
        cleaned = clean_inline_text(stripped)

        if stripped.startswith("#") and is_title_candidate(cleaned):
            title = cleaned
            title_index = idx
            break

    if title_index is None:
        for idx, raw in enumerate(raw_lines[:20]):
            if is_image_or_empty(raw):
                continue
            cleaned = clean_inline_text(raw.strip())
            if is_title_candidate(cleaned):
                title = cleaned
                title_index = idx
                break

    if title_index is not None:
        for raw in raw_lines[title_index + 1 : title_index + 8]:
            if is_image_or_empty(raw):
                continue
            cleaned = clean_inline_text(raw.strip())
            lowered = cleaned.casefold()
            if lowered in TITLE_BLACKLIST or lowered.startswith("figure "):
                continue
            if len(cleaned) > 300:
                continue
            authors = cleaned
            break

    return title, authors


def build_paper_records(base_dir: Path) -> list[PaperRecord]:
    records: list[PaperRecord] = []
    for folder in sorted((p for p in base_dir.iterdir() if p.is_dir()), key=lambda p: p.name.lower()):
        title, authors = extract_title_and_authors(folder)
        records.append(
            PaperRecord(
                folder=folder,
                title=title,
                authors=authors,
                norm_title=normalize_text(title),
                compact_title=compact_text(title),
                norm_folder=normalize_text(folder.name),
                compact_folder=compact_text(folder.name),
            )
        )
    return records


def process_markdown_content(content: str, folder_path_for_markdown: str) -> str:
    content = re.sub(r"<script.*?>.*?</script>", "", content, flags=re.DOTALL | re.IGNORECASE)

    def demote_header(match: re.Match[str]) -> str:
        return "#" * (len(match.group(1)) + 2) + match.group(2)

    content = re.sub(r"^(#+)(.*)$", demote_header, content, flags=re.MULTILINE)
    rel_folder_path = folder_path_for_markdown.replace("\\", "/")

    def fix_img_path(match: re.Match[str]) -> str:
        prefix, img_path, suffix = match.group(1), match.group(2), match.group(3)
        if not img_path.startswith(("http", "downloads/", "/", "G:/", "G:\\")):
            return f"{prefix}{rel_folder_path}/{img_path}{suffix}"
        return match.group(0)

    content = re.sub(r"(!\[.*?\]\()(.+?)(\))", fix_img_path, content)
    content = re.sub(r'(<img.*?src=")(.+?)(")', fix_img_path, content)
    return content.strip()


def is_chapter_heading(line: str) -> str | None:
    match = re.match(r"^\s*##\s*第\s*(\d+)\s*章", line)
    if match:
        return match.group(1)
    match = re.match(r"^\s*##\s*chapter\s*(\d+)", line, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def is_placeholder(line: str) -> bool:
    placeholders = (
        "[基于本篇论文的内容待后续详细生成]",
        "[鍩轰簬鏈瘒璁烘枃鐨勫唴瀹瑰緟鍚庣画璇︾粏鐢熸垚]",
        "[閸╄桨绨張顒傜槖鐠佺儤鏋冮惃鍕敶鐎圭懓绶熼崥搴ｇ敾鐠囷妇绮忛悽鐔稿灇]",
    )
    return any(token in line for token in placeholders)


def extract_outline_title(line: str) -> str:
    match = re.match(r"^\s*[-*]\s*\*\*(.*?)\*\*\s*$", line)
    if match:
        value = match.group(1).strip()
    else:
        value = re.sub(r"^\s*[-*]\s*", "", line).strip()
    value = re.sub(r"^\[\d{4}\]\s*", "", value)
    return value.strip()


def title_match_score(target_title: str, record: PaperRecord) -> float:
    target_norm = normalize_text(target_title)
    target_compact = compact_text(target_title)
    if not target_norm:
        return 0.0

    if target_compact and (
        target_compact == record.compact_title
        or target_compact == record.compact_folder
    ):
        return 10.0

    if target_compact and record.compact_title and (
        target_compact in record.compact_title or record.compact_title in target_compact
    ):
        return 9.0

    if target_compact and record.compact_folder and (
        target_compact in record.compact_folder or record.compact_folder in target_compact
    ):
        return 8.0

    ratio = SequenceMatcher(None, target_norm, record.norm_title).ratio()
    folder_ratio = SequenceMatcher(None, target_norm, record.norm_folder).ratio()
    tokens_a = {token for token in target_norm.split() if len(token) >= 3}
    tokens_b = {token for token in record.norm_title.split() if len(token) >= 3}
    overlap = len(tokens_a & tokens_b)
    return max(ratio, folder_ratio) + overlap


def find_paper_record_from_line(line: str, records: list[PaperRecord]) -> PaperRecord | None:
    target_title = extract_outline_title(line)
    if not target_title:
        return None

    best_record: PaperRecord | None = None
    best_score = 0.0
    for record in records:
        score = title_match_score(target_title, record)
        if score > best_score:
            best_score = score
            best_record = record

    if best_record is None:
        return None

    if best_score >= 8.0:
        return best_record

    target_norm = normalize_text(target_title)
    similarity = SequenceMatcher(None, target_norm, best_record.norm_title).ratio()
    if similarity >= 0.7:
        return best_record

    return None


def merge_report(
    outline_path: Path,
    output_path: Path,
    base_dir: Path,
    analysis_filename: str = "Analysis_Detail.md",
    only_chapter_2: bool = True,
) -> tuple[int, int]:
    if not outline_path.is_file():
        raise SystemExit(f"Outline not found: {outline_path}")
    if not base_dir.is_dir():
        raise SystemExit(f"Base dir not found: {base_dir}")

    records = build_paper_records(base_dir)
    lines = outline_path.read_text(encoding="utf-8").splitlines(keepends=True)
    merged_lines: list[str] = []
    processed_folders: set[Path] = set()
    ordered_references: list[tuple[str, str]] = []

    in_merge_scope = False

    for line in lines:
        chapter_num = is_chapter_heading(line)
        if chapter_num is not None:
            in_merge_scope = (chapter_num == "2") if only_chapter_2 else True
            merged_lines.append(line)
            continue

        if only_chapter_2 and not in_merge_scope:
            merged_lines.append(line)
            continue

        if is_placeholder(line):
            continue

        if in_merge_scope and line.lstrip().startswith(("-", "*")):
            title_text = extract_outline_title(line)
            merged_lines.append(f"#### {title_text}\n")

            record = find_paper_record_from_line(line, records)
            if record and record.folder not in processed_folders:
                detail_file = record.folder / analysis_filename
                if detail_file.is_file():
                    detail_content = detail_file.read_text(encoding="utf-8", errors="ignore")
                    processed_content = process_markdown_content(
                        detail_content,
                        str(record.folder.as_posix()),
                    )
                    merged_lines.append("\n")
                    merged_lines.append(processed_content)
                    merged_lines.append("\n\n-----\n\n")
                    ordered_references.append((record.title, record.authors))
                    processed_folders.add(record.folder)
            continue

        merged_lines.append(line)

    if ordered_references:
        merged_lines.append("\n## 参考文献\n\n")
        seen: set[tuple[str, str]] = set()
        idx = 1
        for title, authors in ordered_references:
            key = (title, authors)
            if key in seen:
                continue
            seen.add(key)
            merged_lines.append(f"{idx}. {title} - {authors}\n")
            idx += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(merged_lines), encoding="utf-8")
    return len(processed_folders), len(ordered_references)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default="downloads/MoE")
    parser.add_argument("--outline", default=None)
    parser.add_argument("--output", default="MoE_report_complete.md")
    parser.add_argument("--analysis-filename", default="Analysis_Detail.md")
    parser.add_argument("--all-chapters", action="store_true", default=False)
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser().resolve()
    outline_path = (
        Path(args.outline).expanduser().resolve()
        if args.outline
        else (base_dir / "outline.md").resolve()
    )
    output_path = Path(args.output).expanduser().resolve()

    processed_count, ref_count = merge_report(
        outline_path=outline_path,
        output_path=output_path,
        base_dir=base_dir,
        analysis_filename=args.analysis_filename,
        only_chapter_2=(not args.all_chapters),
    )
    print(
        f"Merged {processed_count} papers. References collected: {ref_count}. "
        f"Output: {output_path}"
    )


if __name__ == "__main__":
    main()
