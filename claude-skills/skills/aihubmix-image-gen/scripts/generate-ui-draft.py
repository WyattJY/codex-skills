#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def read_prompt(args: argparse.Namespace) -> str:
    parts: list[str] = []
    if args.prompt_file:
        parts.append(Path(args.prompt_file).read_text(encoding="utf-8"))
    if args.prompt:
        parts.append(args.prompt)
    prompt = "\n\n".join(p.strip() for p in parts if p.strip())
    if not prompt:
        raise SystemExit("Provide --prompt or --prompt-file.")
    return prompt


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or dry-run a UI draft image through CPA/OpenAI-compatible image API.")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--prompt-file", default="")
    parser.add_argument("--out-dir", default="tmp/ui-drafts")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--dry-run", action="store_true", help="Write prompt/request files without calling the API.")
    parser.add_argument("--env-file", action="append", default=[], help="Optional .env file; values are loaded without printing secrets.")
    args = parser.parse_args()

    configured_env = os.environ.get("CLAUDE_UI_IMAGE_ENV") or os.environ.get("CODEX_UI_IMAGE_ENV", "")
    env_files = [Path(configured_env)] if configured_env else []
    env_files += [Path(p) for p in args.env_file]
    for env_file in env_files:
        load_env_file(env_file)

    prompt = read_prompt(args)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    prompt_path = out_dir / f"ui-draft-{stamp}.prompt.md"
    prompt_path.write_text(prompt + "\n", encoding="utf-8")

    base_url = (
        os.environ.get("CLAUDE_UI_IMAGE_BASE_URL") or os.environ.get("CODEX_UI_IMAGE_BASE_URL")
        or os.environ.get("CPA_IMAGE_BASE_URL")
        or os.environ.get("AIHUBMIX_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or "https://cpa.lobewyatt.icu/v1"
    )
    model = os.environ.get("CLAUDE_UI_IMAGE_MODEL") or os.environ.get("CODEX_UI_IMAGE_MODEL") or os.environ.get("CPA_IMAGE_MODEL") or os.environ.get("AIHUBMIX_IMAGE_MODEL") or os.environ.get("OPENAI_IMAGE_MODEL") or "gpt-image-2"
    api_key = (
        os.environ.get("CLAUDE_UI_IMAGE_API_KEY") or os.environ.get("CODEX_UI_IMAGE_API_KEY")
        or os.environ.get("CPA_IMAGE_API_KEY")
        or os.environ.get("AIHUBMIX_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "size": args.size,
        "n": 1,
    }
    write_json(out_dir / f"ui-draft-{stamp}.request.redacted.json", {**payload, "api_key": "<redacted>"})

    if args.dry_run or not api_key:
        print(f"Saved prompt: {prompt_path}")
        print("Dry run only." if args.dry_run else "No API key found; request not sent.")
        return

    endpoint = base_url.rstrip("/") + "/images/generations"
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Image API failed: HTTP {exc.code}; body saved nowhere; {body[:500]}")

    write_json(out_dir / f"ui-draft-{stamp}.response.json", result)
    data = result.get("data") or []
    if data and data[0].get("b64_json"):
        img_path = out_dir / f"ui-draft-{stamp}.png"
        img_path.write_bytes(base64.b64decode(data[0]["b64_json"]))
        print(f"Saved image: {img_path}")
    elif data and data[0].get("url"):
        print(f"Image URL: {data[0]['url']}")
    else:
        print(f"Saved response: {out_dir / f'ui-draft-{stamp}.response.json'}")


if __name__ == "__main__":
    main()
