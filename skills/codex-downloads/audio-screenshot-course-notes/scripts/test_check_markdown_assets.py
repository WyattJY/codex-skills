#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_markdown_assets.py")


def load_module():
    spec = importlib.util.spec_from_file_location("check_markdown_assets", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckMarkdownAssetsTests(unittest.TestCase):
    def run_checker(self, md_path: Path) -> tuple[int, str]:
        module = load_module()
        old_argv = sys.argv
        stdout = io.StringIO()
        try:
            sys.argv = [str(MODULE_PATH), str(md_path)]
            with contextlib.redirect_stdout(stdout):
                code = module.main()
        finally:
            sys.argv = old_argv
        return code, stdout.getvalue()

    def test_markdown_image_path_with_parentheses_is_not_truncated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "assets").mkdir()
            (root / "assets" / "diagram (final).png").write_bytes(b"")
            note = root / "note.md"
            note.write_text("![figure](assets/diagram (final).png)\n", encoding="utf-8")

            code, output = self.run_checker(note)

        self.assertEqual(code, 0, output)
        self.assertIn("local_image_links=1", output)
        self.assertIn("missing=0", output)

    def test_obsidian_image_embed_missing_asset_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "note.md"
            note.write_text("![[assets/missing wiki.png]]\n", encoding="utf-8")

            code, output = self.run_checker(note)

        self.assertEqual(code, 1, output)
        self.assertIn("local_image_links=1", output)
        self.assertIn("missing=1", output)
        self.assertIn("missing wiki.png", output)

    def test_obsidian_image_embed_alias_existing_asset_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "assets").mkdir()
            (root / "assets" / "slide.png").write_bytes(b"")
            note = root / "note.md"
            note.write_text("![[assets/slide.png|课堂截图]]\n", encoding="utf-8")

            code, output = self.run_checker(note)

        self.assertEqual(code, 0, output)
        self.assertIn("local_image_links=1", output)
        self.assertIn("missing=0", output)


if __name__ == "__main__":
    unittest.main()
