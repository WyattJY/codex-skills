#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path

EXTS = {'.pdf', '.md', '.txt', '.docx', '.pptx', '.ipynb', '.html'}
EXCLUDES = {'.git', 'node_modules', '.cache', '__pycache__'}


def recent_files(root: Path, limit: int = 20):
    out = []
    if not root.exists():
        return out
    stack = [(root, 0)]
    while stack:
        p, depth = stack.pop()
        if depth > 4 or p.name in EXCLUDES:
            continue
        try:
            for c in p.iterdir():
                if c.is_dir():
                    stack.append((c, depth + 1))
                elif c.suffix.lower() in EXTS:
                    out.append(c)
        except Exception:
            pass
    out.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    return out[:limit]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--memory-root', default=os.environ.get('HERMES_MEMORY_HOME', '/Volumes/T7 Shield/hermes/home/memory'))
    parser.add_argument('--research-root', default=os.environ.get('HERMES_RESEARCH_ROOT', '/Volumes/T7 Shield/02_Research_Papers_Reports/实习'))
    args = parser.parse_args()

    memory = Path(args.memory_root)
    root = Path(args.research_root)
    files = recent_files(root, 10)
    today = datetime.now().strftime('%Y-%m-%d')
    chosen = str(files[0]) if files else 'UNKNOWN'
    refs = '\n'.join('- ' + str(p) for p in files[:5]) if files else '- No local files found; add papers/reports to research root.'

    lines = [
        '# Daily Research Idea - ' + today,
        '',
        '## 标题',
        '多模态训练的一条可验证小实验',
        '',
        '## 500 字 idea',
        f'今天只推进一条和当前 watchlist 绑定的想法：围绕多模态/训练工作，不先追热点，而是从本地 T7 研究资料中选择一个最近文件作为锚点：`{chosen}`。建议把它转成一个最小可验证实验：抽取该资料里的核心方法假设，映射到你当前训练任务中的一个可控模块（数据过滤、hard negative 构造、reranker 目标、视觉语言输入格式、或偏好优化样本构造），只改一个变量，保持其余训练配置不变。这样可以避免“看完论文但没有落地”的信息流过载。',
        '',
        '如果锚点资料与 reranker 相关，则实验可以是：固定 backbone 与训练集，只改变 hard negative 采样策略，观察 nDCG/Recall@K 与 bad case 类型是否改善。如果锚点资料与 Qwen-VL/视频理解相关，则实验可以是：在 50-200 条样本上比较不同图像/视频帧摘要格式对下游判断的影响。如果锚点资料与 DPO/RLHF 相关，则实验可以是：构造极小偏好对，先验证 reward signal 是否区分明显错误与明显正确输出。',
        '',
        '## 可验证实验',
        '选择一个当前项目可控变量，做 A/B 两组，运行在小样本或短 epoch 上；当天只判断方向，不追求最终 SOTA。',
        '',
        '## 所需数据/代码',
        '- 数据：脱敏聚合统计或公司内网中可手动运行的小样本子集。',
        '- 代码：现有训练脚本、配置路径、评估脚本。',
        '- 记录：RUN_CARD + 指标截图/日志摘要。',
        '',
        '## 预期信号',
        '一个关键指标有方向性改善，或 bad case 类型明显减少；同时训练成本不显著增加。',
        '',
        '## 风险与停止条件',
        '若小样本无改善且错误类型不变，停止继续扩大实验；先回到数据画像和 label 分布检查。',
        '',
        '## 参考链接/本地资料',
        refs,
        '',
        '## 反馈按钮',
        '请回复：有用 / 无用 / 深读',
    ]
    text = '\n'.join(lines) + '\n'
    out_dir = memory / 'research' / 'IDEA_LOG'
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f'idea-{today}.md'
    out.write_text(text, encoding='utf-8')
    print(text)
    print('\nSaved: ' + str(out))


if __name__ == '__main__':
    main()
