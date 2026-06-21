#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_course_note_quality.py")


def load_module():
    spec = importlib.util.spec_from_file_location("check_course_note_quality", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckCourseNoteQualityTests(unittest.TestCase):
    def run_checker(
        self, md_path: Path, extra_args: list[str] | None = None
    ) -> tuple[int, str]:
        module = load_module()
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = module.main([str(md_path), *(extra_args or [])])
        return code, stdout.getvalue()

    def test_good_note_with_required_callouts_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "note.md"
            asset = Path(tmp) / "assets" / "fig.jpg"
            asset.parent.mkdir()
            asset.write_bytes(b"fake")
            note.write_text(
                "\n".join(
                    [
                        "# Lesson",
                        "> [!info] 资料来源",
                        "> audio and transcript links",
                        "> [!important] 本节核心",
                        "> central claim",
                        "> [!important] 关键机制",
                        "> mechanism summary",
                        "> [!warning] 实现陷阱",
                        "> boundary condition",
                        "## 先给结论",
                        "为什么本节要解决一个真实问题。",
                        "## 课程承接",
                        "这节课连接前后课程。",
                        "## 学习地图",
                        "| 阶段 | 问题 | 证据 |",
                        "| --- | --- | --- |",
                        "| A | 为什么 | 截图 |",
                        "## 一 主要内容",
                        "### 动机",
                        "这里解释为什么引入概念。",
                        "### 核心观点",
                        "这里说明核心机制。",
                        "![图](<assets/fig.jpg>)",
                        "这张图证明了课程里的关键机制，解释了图中结构解决什么问题。",
                        "```python",
                        "x = 1",
                        "```",
                        "源码位置：[demo.py:1](<vscode://file/tmp/demo.py:1>)",
                        "### 本章小结",
                        "本章小结说明机制和证据。",
                        "## 六 大模型算法工程师易错点",
                        "### 本章小结",
                        "工程师易错点总结。",
                        "## 七 复盘动作与自测题",
                        "### 自测题",
                        "1. 为什么？",
                        "### 复盘动作",
                        "1. 打开源码验证。",
                    ]
                ),
                encoding="utf-8",
            )

            code, output = self.run_checker(note)

        self.assertEqual(code, 0, output)
        self.assertIn("callout_important=2", output)
        self.assertIn("callout_warning=1", output)

    def test_polished_plain_note_without_callouts_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "note.md"
            note.write_text(
                "# Lesson\n\n## 先给结论\n\n这里有核心概念。\n\n## 工程师易错点\n\n这里有易错点。\n",
                encoding="utf-8",
            )

            code, output = self.run_checker(note)

        self.assertEqual(code, 1, output)
        self.assertIn("missing required > [!info]", output)
        self.assertIn("important callouts too few", output)
        self.assertIn("warning callouts too few", output)

    def test_callout_only_note_fails_deep_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "note.md"
            note.write_text(
                "\n".join(
                    [
                        "# Lesson",
                        "> [!info] 资料来源",
                        "> source",
                        "> [!important] A",
                        "> a",
                        "> [!important] B",
                        "> b",
                        "> [!warning] C",
                        "> c",
                        "## 先给结论",
                        "这里看起来有总结，但没有课程承接、学习地图、图片证据或源码锚点。",
                    ]
                ),
                encoding="utf-8",
            )

            code, output = self.run_checker(note)

        self.assertEqual(code, 1, output)
        self.assertIn("missing required heading: 课程承接", output)
        self.assertIn("missing required heading: 学习地图", output)
        self.assertIn("local image links too few", output)
        self.assertIn("source anchors too few", output)

    def test_code_block_without_adjacent_source_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            asset = Path(tmp) / "assets" / "fig.jpg"
            asset.parent.mkdir()
            asset.write_bytes(b"fake")
            note = Path(tmp) / "note.md"
            note.write_text(
                "\n".join(
                    [
                        "# Lesson",
                        "> [!info] 资料来源",
                        "> source",
                        "> [!important] A",
                        "> a",
                        "> [!important] B",
                        "> b",
                        "> [!warning] C",
                        "> c",
                        "## 先给结论",
                        "为什么要学习。",
                        "## 课程承接",
                        "承接。",
                        "## 学习地图",
                        "| 阶段 | 问题 | 证据 |",
                        "| --- | --- | --- |",
                        "| A | 为什么 | 截图 |",
                        "![图](<assets/fig.jpg>)",
                        "这张图解释了关键机制和证据。",
                        "```python",
                        "x = 1",
                        "```",
                        "这里没有紧邻源码位置。",
                        "## 六 大模型算法工程师易错点",
                        "### 本章小结",
                        "总结。",
                        "## 七 复盘动作与自测题",
                        "### 自测题",
                        "1. 为什么？",
                        "### 复盘动作",
                        "1. 验证。",
                    ]
                ),
                encoding="utf-8",
            )

            code, output = self.run_checker(note)

        self.assertEqual(code, 1, output)
        self.assertIn("code block without adjacent source anchor", output)

    def test_toc_target_missing_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            asset = Path(tmp) / "assets" / "fig.jpg"
            asset.parent.mkdir()
            asset.write_bytes(b"fake")
            note = Path(tmp) / "note.md"
            note.write_text(
                "\n".join(
                    [
                        "# Lesson",
                        "> [!info] 资料来源",
                        "> source",
                        "> [!important] A",
                        "> a",
                        "> [!important] B",
                        "> b",
                        "> [!warning] C",
                        "> c",
                        "- [[#不存在|bad]]",
                        "## 先给结论",
                        "为什么要学习。",
                        "## 课程承接",
                        "承接。",
                        "## 学习地图",
                        "| 阶段 | 问题 | 证据 |",
                        "| --- | --- | --- |",
                        "| A | 为什么 | 截图 |",
                        "![图](<assets/fig.jpg>)",
                        "这张图解释了关键机制和证据。",
                        "```python",
                        "x = 1",
                        "```",
                        "源码位置：[demo.py:1](<vscode://file/tmp/demo.py:1>)",
                        "## 六 大模型算法工程师易错点",
                        "### 本章小结",
                        "总结。",
                        "## 七 复盘动作与自测题",
                        "### 自测题",
                        "1. 为什么？",
                        "### 复盘动作",
                        "1. 验证。",
                    ]
                ),
                encoding="utf-8",
            )

            code, output = self.run_checker(note)

        self.assertEqual(code, 1, output)
        self.assertIn("TOC target missing: 不存在", output)

    def test_embedded_transcript_heading_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "note.md"
            note.write_text(
                "# Lesson\n\n> [!info] 资料来源\n> source\n\n> [!important] A\n> a\n\n> [!important] B\n> b\n\n> [!warning] C\n> c\n\n## 短分段逐字稿\n",
                encoding="utf-8",
            )

            code, output = self.run_checker(note)

        self.assertEqual(code, 1, output)
        self.assertIn("transcript sections appear", output)

    def test_unused_lesson_asset_image_fails_when_asset_dir_is_given(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            asset_dir = Path(tmp) / "assets"
            asset_dir.mkdir()
            (asset_dir / "used.jpg").write_bytes(b"fake")
            (asset_dir / "missing.jpg").write_bytes(b"fake")
            note = Path(tmp) / "note.md"
            note.write_text(
                "\n".join(
                    [
                        "# Lesson",
                        "> [!info] 资料来源",
                        "> source",
                        "> [!important] A",
                        "> a",
                        "> [!important] B",
                        "> b",
                        "> [!warning] C",
                        "> c",
                        "## 先给结论",
                        "为什么要学习。",
                        "## 课程承接",
                        "承接。",
                        "## 学习地图",
                        "| 阶段 | 问题 | 证据 |",
                        "| --- | --- | --- |",
                        "| A | 为什么 | 截图 |",
                        "![图](<assets/used.jpg>)",
                        "这张图解释了关键机制和证据。",
                        "```python",
                        "x = 1",
                        "```",
                        "源码位置：[demo.py:1](<vscode://file/tmp/demo.py:1>)",
                        "## 六 大模型算法工程师易错点",
                        "### 本章小结",
                        "总结。",
                        "## 七 复盘动作与自测题",
                        "### 自测题",
                        "1. 为什么？",
                        "### 复盘动作",
                        "1. 验证。",
                    ]
                ),
                encoding="utf-8",
            )

            code, output = self.run_checker(note, ["--asset-dir", str(asset_dir)])

        self.assertEqual(code, 1, output)
        self.assertIn("unused asset images", output)
        self.assertIn("missing.jpg", output)

    def test_all_lesson_asset_images_used_passes_when_asset_dir_is_given(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            asset_dir = Path(tmp) / "assets"
            asset_dir.mkdir()
            (asset_dir / "fig1.jpg").write_bytes(b"fake")
            (asset_dir / "fig2.png").write_bytes(b"fake")
            (asset_dir / "._fig2.png").write_bytes(b"appledouble")
            note = Path(tmp) / "note.md"
            note.write_text(
                "\n".join(
                    [
                        "# Lesson",
                        "> [!info] 资料来源",
                        "> source",
                        "> [!important] A",
                        "> a",
                        "> [!important] B",
                        "> b",
                        "> [!warning] C",
                        "> c",
                        "## 先给结论",
                        "为什么要学习。",
                        "## 课程承接",
                        "承接。",
                        "## 学习地图",
                        "| 阶段 | 问题 | 证据 |",
                        "| --- | --- | --- |",
                        "| A | 为什么 | 截图 |",
                        "![图一](<assets/fig1.jpg>)",
                        "这张图解释了第一段关键机制和证据，说明为什么截图必须贴在对应论述旁边。",
                        "![图二](<assets/fig2.png>)",
                        "这张图解释了第二段关键机制和证据，继续证明所有截图都应进入教学链路。",
                        "```python",
                        "x = 1",
                        "```",
                        "源码位置：[demo.py:1](<vscode://file/tmp/demo.py:1>)",
                        "## 六 大模型算法工程师易错点",
                        "### 本章小结",
                        "总结。",
                        "## 七 复盘动作与自测题",
                        "### 自测题",
                        "1. 为什么？",
                        "### 复盘动作",
                        "1. 验证。",
                    ]
                ),
                encoding="utf-8",
            )

            code, output = self.run_checker(note, ["--asset-dir", str(asset_dir)])

        self.assertEqual(code, 0, output)
        self.assertIn("asset_images_total=2", output)
        self.assertIn("unused_asset_images=0", output)


if __name__ == "__main__":
    unittest.main()
