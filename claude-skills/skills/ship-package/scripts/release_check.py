#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import time
from pathlib import Path

SECRET_NAME_RE = re.compile(r"(?i)(\.env$|token|secret|cookie|session|credential|apikey|api_key|password)")
SECRET_VALUE_RE = re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*([^\s#]+)")
EXCLUDE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".next", "dist", "build", ".cache"}


def git_output(repo: Path, cmd: list[str]) -> str:
    try:
        p = subprocess.run(cmd, cwd=str(repo), text=True, capture_output=True, timeout=30)
        return ((p.stdout or "") + (p.stderr or "")).strip()
    except Exception as exc:
        return f"unavailable: {exc}"


def walk_files(root: Path):
    for p in root.rglob("*"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.is_file() and not p.name.startswith("._"):
            yield p


def has_literal_secret(text: str) -> bool:
    for line in text.splitlines():
        match = SECRET_VALUE_RE.search(line)
        if not match:
            continue
        value = match.group(2).strip().strip('"').strip("'")
        lower = value.lower()
        if not value or value in {"***", "<redacted>", "true", "false"}:
            continue
        if lower.startswith(("os.environ", "env.", "process.env", "${", "$", "getenv", "none", "null")):
            continue
        if len(value) >= 12 and re.search(r"[A-Za-z]", value) and re.search(r"[0-9]", value):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="G9 release/package safety checker.")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    suspicious_names = []
    suspicious_values = []
    for p in walk_files(repo):
        rel = p.relative_to(repo)
        if SECRET_NAME_RE.search(p.name):
            suspicious_names.append(str(rel))
        if p.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".js", ".ts", ".tsx", ".env", ""}:
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if has_literal_secret(text):
                suspicious_values.append(str(rel))

    required_docs = ["README.md", ".env.example"]
    present_docs = {doc: (repo / doc).exists() for doc in required_docs}
    docker_present = any((repo / name).exists() for name in ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"])
    git_status = git_output(repo, ["git", "status", "--short"])
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    out = Path(args.out) if args.out else repo / "release_check_report.md"
    body = [
        "# Release Check Report",
        "",
        f"- generated_at: {stamp}",
        f"- repo: `{repo}`",
        "",
        "## Git Status",
        "```text",
        git_status or "(clean or not a git repo)",
        "```",
        "",
        "## Required Docs",
        "",
        "| item | present |",
        "|---|---|",
        *[f"| {doc} | {present_docs[doc]} |" for doc in required_docs],
        f"| Dockerfile/compose | {docker_present} |",
        "",
        "## Secret Hygiene",
        "",
        f"- suspicious_file_names: {len(suspicious_names)}",
        f"- suspicious_secret_values: {len(suspicious_values)}",
        "",
        "### Suspicious File Names",
        *[f"- `{name}`" for name in suspicious_names[:80]],
        "",
        "### Suspicious Value Matches",
        *[f"- `{name}`" for name in suspicious_values[:80]],
        "",
        "## G9 Decision",
        "- PASS only when suspicious values are zero or confirmed false positives.",
        "- Do not ship `.env`, tokens, sessions, cookies, or company raw data.",
        "- Include exact run/test/start/rollback commands in release notes.",
    ]
    out.write_text("\n".join(body) + "\n", encoding="utf-8")
    print(out)
    if suspicious_values:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
