#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from pathlib import Path


def read_optional(path: str) -> str:
    if not path:
        return ""
    p = Path(path)
    return p.read_text(encoding="utf-8", errors="ignore")[:12000] if p.exists() else ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create backend blueprint docs for G6.")
    parser.add_argument("--project", default="Wyatt Product")
    parser.add_argument("--requirements", default="")
    parser.add_argument("--design", default="")
    parser.add_argument("--out-dir", default="backend-blueprint")
    args = parser.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    now = time.strftime("%Y-%m-%d")
    req = read_optional(args.requirements)
    design = read_optional(args.design)

    (out / "API_SPEC.md").write_text(f"""# API_SPEC - {args.project}

Generated: {now}

## Source Context

### Requirements
```text
{req or "TODO: attach requirements.md"}
```

### Design
```text
{design or "TODO: attach design.md"}
```

## Endpoints

| Method | Path | Purpose | Auth | Request | Response | Errors |
|---|---|---|---|---|---|---|
| GET | /health | service health | none | - | status/version | 500 |

## Contracts
- Define stable response envelopes before implementation.
- Keep frontend mock data aligned with this file.
- Every non-2xx response must map to `ERROR_MODEL.md`.
""", encoding="utf-8")

    (out / "DB_SCHEMA.md").write_text(f"""# DB_SCHEMA - {args.project}

Generated: {now}

## Tables

| Table | Purpose | Key Fields | Retention | Notes |
|---|---|---|---|---|
| audit_events | user-visible actions and release-relevant state changes | id, actor, action, target, created_at | project-defined | no secrets |

## Migration Rules
- Add migrations in small reversible steps.
- Never store API keys, tokens, cookies, sessions, or raw company data.
- Add indexes only after access paths are clear.
""", encoding="utf-8")

    (out / "ERROR_MODEL.md").write_text(f"""# ERROR_MODEL - {args.project}

Generated: {now}

## Response Shape
```json
{{
  "error": {{
    "code": "string",
    "message": "safe user-facing message",
    "request_id": "string"
  }}
}}
```

## Error Classes
| Code | HTTP | User Message | Log Detail | Test |
|---|---:|---|---|---|
| VALIDATION_ERROR | 400 | Input is invalid. | field-level safe summary | unit/API test |
| UNAUTHORIZED | 401 | Please sign in. | no token values | auth test |
| FORBIDDEN | 403 | Not allowed. | actor/action only | permission test |
| NOT_FOUND | 404 | Resource not found. | resource type/id hash | API test |
| RATE_LIMITED | 429 | Try again later. | bucket key hash | load/rate test |
| INTERNAL | 500 | Something went wrong. | request id + stack in server logs | failure test |
""", encoding="utf-8")

    print(out)


if __name__ == "__main__":
    main()
