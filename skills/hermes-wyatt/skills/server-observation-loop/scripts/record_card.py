#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from pathlib import Path


CARD_DIRS = {
    "run": "datasets/RUN_CARDS",
    "data": "datasets/DATA_CARDS",
    "error": "datasets/ERROR_CARDS",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Record RUN_CARD, DATA_CARD, or ERROR_CARD without raw company data.")
    parser.add_argument("kind", choices=sorted(CARD_DIRS))
    parser.add_argument("--memory-root", default="/Volumes/T7 Shield/hermes/home/memory")
    parser.add_argument("--title", required=True)
    parser.add_argument("--goal", default="")
    parser.add_argument("--command", default="")
    parser.add_argument("--observed", default="")
    parser.add_argument("--inference", default="")
    parser.add_argument("--next-command", default="")
    parser.add_argument("--metrics", default="")
    args = parser.parse_args()

    date = time.strftime("%Y-%m-%d")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.memory_root) / CARD_DIRS[args.kind]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{args.kind}-card-{stamp}.md"
    body = f"""# {args.kind.upper()}_CARD - {args.title}

## 基本信息
- 日期：{date}
- 目标：{args.goal or "UNKNOWN_NEEDS_WYATT"}
- 安全边界：只记录脱敏日志、截图摘要、聚合统计或命令；不写公司原始数据。

## 运行命令
```bash
{args.command or "# UNKNOWN_NEEDS_WYATT"}
```

## 核心指标
{args.metrics or "- UNKNOWN_NEEDS_WYATT"}

## 截图/日志摘要
{args.observed or "- UNKNOWN_NEEDS_WYATT"}

## Hermes 分析
- 我看到什么：{args.observed or "UNKNOWN_NEEDS_WYATT"}
- 我推断什么：{args.inference or "UNKNOWN_NEEDS_WYATT"}
- 下一步命令：
```bash
{args.next_command or "# UNKNOWN_NEEDS_WYATT"}
```

## 禁止项检查
- 未记录 API key / token / cookie / session。
- 未记录原始公司数据、原始样本或私有标识。
"""
    out.write_text(body, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()

