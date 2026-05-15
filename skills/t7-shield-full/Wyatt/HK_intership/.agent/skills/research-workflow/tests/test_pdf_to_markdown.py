import importlib.util
from pathlib import Path
import sys
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "pdf_to_markdown.py"
sys.path.insert(0, str(SCRIPT_PATH.parent))
SPEC = importlib.util.spec_from_file_location("pdf_to_markdown", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PdfPipelineModeTests(unittest.TestCase):
    def test_fast_mode_keeps_ocr_and_table_structure_off(self) -> None:
        options = MODULE.build_pipeline_options("fast")

        self.assertFalse(options.do_ocr)
        self.assertFalse(options.do_table_structure)
        self.assertTrue(options.generate_page_images)
        self.assertTrue(options.generate_picture_images)

    def test_enhanced_mode_turns_on_ocr_and_table_structure(self) -> None:
        options = MODULE.build_pipeline_options("enhanced")

        self.assertTrue(options.do_ocr)
        self.assertTrue(options.do_table_structure)
        self.assertTrue(options.generate_page_images)
        self.assertTrue(options.generate_picture_images)

    def test_enhanced_flag_selects_enhanced_mode(self) -> None:
        args = MODULE.parse_args(["--root", "downloads", "--enhanced"])

        self.assertEqual(args.mode, "enhanced")


if __name__ == "__main__":
    unittest.main()
