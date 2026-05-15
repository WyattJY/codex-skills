import argparse
import re
import urllib.parse
from pathlib import Path


def convert_markdown_image_paths_to_relative(markdown: str, base_dir: Path) -> str:
    base_dir_str = str(base_dir.as_posix().rstrip("/")) + "/"

    def make_relative_markdown(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        full_path = match.group(2)

        decoded_path = urllib.parse.unquote(full_path)
        decoded_posix = decoded_path.replace("\\", "/")

        if decoded_posix.startswith(base_dir_str):
            rel_path = decoded_posix[len(base_dir_str):]
            encoded_rel_path = urllib.parse.quote(rel_path)
            return f"![{alt_text}]({encoded_rel_path})"

        return match.group(0)

    def make_relative_html(match: re.Match[str]) -> str:
        prefix = match.group(1)
        full_path = match.group(2)
        suffix = match.group(3)

        decoded_path = urllib.parse.unquote(full_path)
        decoded_posix = decoded_path.replace("\\", "/")

        if decoded_posix.startswith(base_dir_str):
            rel_path = decoded_posix[len(base_dir_str):]
            encoded_rel_path = urllib.parse.quote(rel_path)
            return f"{prefix}{encoded_rel_path}{suffix}"

        return match.group(0)

    markdown_pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    html_pattern = re.compile(r'(<img[^>]*?src=")(.+?)(")')

    out = markdown_pattern.sub(make_relative_markdown, markdown)
    out = html_pattern.sub(make_relative_html, out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Markdown file to rewrite in-place")
    parser.add_argument(
        "--base-dir",
        default="downloads",
        help="Absolute or project-relative base dir prefix to strip from image paths",
    )
    args = parser.parse_args()

    md_path = Path(args.file).expanduser().resolve()
    base_dir = Path(args.base_dir).expanduser().resolve()

    if not md_path.is_file():
        raise SystemExit(f"Markdown file not found: {md_path}")
    if not base_dir.is_dir():
        raise SystemExit(f"Base dir not found: {base_dir}")

    content = md_path.read_text(encoding="utf-8")
    new_content = convert_markdown_image_paths_to_relative(content, base_dir)
    md_path.write_text(new_content, encoding="utf-8")
    print(f"Converted absolute image paths to relative in {md_path}")


if __name__ == "__main__":
    main()
