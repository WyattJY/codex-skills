#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
import time
from pathlib import Path


def extract_section(text: str, title_fragment: str) -> str:
    pattern = re.compile(rf"^##\s+.*{re.escape(title_fragment)}.*?\n(.*?)(?=^##\s+|\Z)", re.M | re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def case_id_from_text(text: str, path: Path) -> str:
    match = re.search(r"^case_id:\s*(\S+)", text, re.M)
    return match.group(1) if match else path.stem


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a final rewritten prompt from a case markdown file.")
    parser.add_argument("case_file")
    parser.add_argument("--memory-root", default="/Volumes/T7 Shield/hermes/home/memory")
    parser.add_argument("--out", default="")
    parser.add_argument("--update-db", action="store_true")
    args = parser.parse_args()

    case_path = Path(args.case_file)
    text = case_path.read_text(encoding="utf-8", errors="ignore")
    case_id = case_id_from_text(text, case_path)
    raw = extract_section(text, "最初需求")
    path_taken = extract_section(text, "实际走的路径")
    delivery = extract_section(text, "最终交付")
    bug = extract_section(text, "代表性 bug")

    prompt = f"""请作为 Hermes orchestrator 处理以下任务，并严格执行 WyattJY 本机工作流：

1. 先运行 case-router，最多加载 0-3 个相关历史 case，并说明复用/不复用原因。
2. 保留用户原始目标，不要把任务改写成泛泛建议。
3. 如属于产品/代码/研究/训练任务，按 G0-G9 gate 输出可落盘产物。
4. 交付物必须包含绝对路径、验证命令、已知风险和下一步。
5. 不写入或展示 `.env`、API key、WEIXIN_TOKEN、cookie、session、公司原始数据。

原始需求：
{raw or "UNKNOWN_NEEDS_WYATT"}

已验证有效路径：
{path_taken or "UNKNOWN_NEEDS_WYATT"}

最终交付参考：
{delivery or "UNKNOWN_NEEDS_WYATT"}

应避免/重点复查的 bug：
{bug or "UNKNOWN_NEEDS_WYATT"}
"""
    out = Path(args.out) if args.out else case_path.with_suffix(".final-prompt.md")
    out.write_text(prompt, encoding="utf-8")
    if args.update_db:
        db = Path(args.memory_root) / "cases" / "embeddings.sqlite"
        conn = sqlite3.connect(str(db))
        project_id = "project-" + re.sub(r"^case-\d+-", "", case_id)
        conn.execute("CREATE TABLE IF NOT EXISTS final_prompts (id TEXT PRIMARY KEY,project_id TEXT,prompt_text TEXT,use_case TEXT,version TEXT)")
        conn.execute("INSERT OR REPLACE INTO final_prompts VALUES (?,?,?,?,?)", (f"prompt-{case_id}", project_id, prompt, "case-final", time.strftime("%Y%m%d")))
        conn.commit()
        conn.close()
    print(out)


if __name__ == "__main__":
    main()

