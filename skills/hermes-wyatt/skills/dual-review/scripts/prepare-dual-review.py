#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import time
from pathlib import Path

SECRET_RE = re.compile(r"(?i)(api[_-]?key|token|secret|password|cookie|session)\s*[:=]\s*\S+")


def run(cmd: list[str], cwd: Path) -> str:
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return out.strip()


def redact(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if SECRET_RE.search(line):
            lines.append(SECRET_RE.sub(r"\1=<redacted>", line))
        else:
            lines.append(line)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a safe dual-review packet from a git workspace.")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--spec", action="append", default=[])
    parser.add_argument("--test-output", default="")
    parser.add_argument("--out-dir", default=".hermes-review")
    parser.add_argument("--title", default="Dual Review Packet")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    out_dir = repo / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = out_dir / f"review-packet-{stamp}.md"

    status = redact(run(["git", "status", "--short"], repo))
    diff = redact(run(["git", "diff", "--stat"], repo) + "\n\n" + run(["git", "diff", "--"], repo))
    specs = []
    for spec in args.spec:
        p = Path(spec)
        if not p.is_absolute():
            p = repo / p
        if p.exists():
            specs.append(f"## Spec: {p}\n\n" + redact(p.read_text(encoding="utf-8", errors="ignore")[:20000]))
    test_text = ""
    if args.test_output:
        p = Path(args.test_output)
        if not p.is_absolute():
            p = repo / p
        if p.exists():
            test_text = redact(p.read_text(encoding="utf-8", errors="ignore")[:20000])
    spec_text = "\n\n".join(specs) if specs else "## Specs\n\n(not provided)"

    body = f"""# {args.title}

Generated: {stamp}
Repo: `{repo}`

## Review Instructions
- Review independently as Claude Code and Codex would.
- Prioritize blocker, major, minor, style.
- Every blocker/major finding needs evidence and a reproduction or test command.
- Do not include secrets or raw company data.

## Git Status
```text
{status or "(clean or not a git repo)"}
```

## Test Output
```text
{test_text or "(not provided)"}
```

{spec_text}

## Diff
```diff
{diff or "(no diff)"}
```

## Merged Findings Template
| Severity | File/Line | Finding | Evidence | Required Fix/Test |
|---|---|---|---|---|
"""
    out.write_text(body, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
