import importlib.util
from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "download_arxiv_papers.py"
SPEC = importlib.util.spec_from_file_location("download_arxiv_papers", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SanitizeFilenameTests(unittest.TestCase):
    def test_sanitize_filename_removes_spaces_and_limits_length(self) -> None:
        raw = (
            "MLLM Is a Strong Reranker: Advancing Multimodal Retrieval-augmented Generation "
            "via Knowledge-enhanced Reranking and Noise-injected Training"
        )

        sanitized = MODULE.sanitize_filename(raw)

        self.assertNotIn(" ", sanitized)
        self.assertLessEqual(len(sanitized), 80)


if __name__ == "__main__":
    unittest.main()
