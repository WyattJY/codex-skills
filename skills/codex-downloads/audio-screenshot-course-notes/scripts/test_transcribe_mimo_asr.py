#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("transcribe_mimo_asr.py")


def load_module():
    spec = importlib.util.spec_from_file_location("transcribe_mimo_asr", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MimoAsrScriptTests(unittest.TestCase):
    def test_payload_uses_mimo_chat_audio_shape(self) -> None:
        module = load_module()

        payload = module.build_payload(
            data_url="data:audio/mpeg;base64,QUJD",
            model="mimo-v2.5-asr",
            language="zh",
        )

        self.assertEqual(payload["model"], "mimo-v2.5-asr")
        self.assertEqual(payload["asr_options"], {"language": "zh"})
        content = payload["messages"][0]["content"][0]
        self.assertEqual(content["type"], "input_audio")
        self.assertEqual(content["input_audio"]["data"], "data:audio/mpeg;base64,QUJD")

    def test_extracts_transcript_from_chat_completion_response(self) -> None:
        module = load_module()

        text = module.extract_transcript_text(
            {
                "choices": [
                    {
                        "message": {
                            "content": "这一段在讲多模态 reranker 的 badcase 分析。"
                        }
                    }
                ],
                "usage": {"seconds": 4},
            }
        )

        self.assertEqual(text, "这一段在讲多模态 reranker 的 badcase 分析。")

    def test_extracts_transcript_removes_mimo_language_tags(self) -> None:
        module = load_module()

        text = module.extract_transcript_text(
            {
                "choices": [
                    {
                        "message": {
                            "content": "think>\n<chinese> Hello. This is a Mimo ASR key test."
                        }
                    }
                ]
            }
        )

        self.assertEqual(text, "Hello. This is a Mimo ASR key test.")

    def test_postprocess_normalizes_common_course_terms(self) -> None:
        module = load_module()

        text = module.postprocess_transcript_text(
            "这一段讲 RPE、LP、LPE 和西塔在位置编码里的作用。"
        )

        self.assertEqual(text, "这一段讲 RoPE、RoPE、RoPE 和theta在位置编码里的作用。")

    def test_postprocess_marks_system_prompt_sounds(self) -> None:
        module = load_module()

        text = module.postprocess_transcript_text("验证码 7462，请填写验证码。")

        self.assertTrue(text.startswith("（非课程提示音："))
        self.assertIn("验证码", text)

    def test_summary_selects_teaching_signal_sentences(self) -> None:
        module = load_module()

        summary = module.summarize_chunk_text(
            "这里先回顾上一节。核心问题是 RoPE 如何把相对位置信息注入 QK 内积。"
            "后面会结合代码说明 theta 的构造。"
        )

        self.assertIn("RoPE", summary)
        self.assertIn("theta", summary)

    def test_silence_range_builder_keeps_short_note_chunks(self) -> None:
        module = load_module()

        ranges = module.build_silence_aligned_ranges(
            duration_seconds=72,
            silences=[(22, 23), (47, 48)],
            target_seconds=25,
            min_seconds=10,
            max_seconds=30,
        )

        self.assertEqual(len(ranges), 3)
        for start, end in ranges:
            self.assertGreaterEqual(end - start, 10)
            self.assertLessEqual(end - start, 30)

    def test_silence_range_builder_uses_target_when_silence_point_is_outside_window(self) -> None:
        module = load_module()

        ranges = module.build_silence_aligned_ranges(
            duration_seconds=65,
            silences=[(0, 65)],
            target_seconds=25,
            min_seconds=10,
            max_seconds=30,
        )

        self.assertEqual(ranges, [(0.0, 25.0), (25.0, 50.0), (50.0, 65)])
        for start, end in ranges:
            self.assertLessEqual(end - start, 30)

    def test_prepare_audio_chunks_segments_supported_audio_when_duration_exceeds_max(self) -> None:
        module = load_module()

        original_data_url = module.data_url_for_audio
        original_find_ffmpeg = module.find_ffmpeg
        original_duration = module.get_audio_duration_seconds
        original_segment = module.segment_audio_with_ffmpeg
        calls: dict[str, bool] = {}

        try:
            module.data_url_for_audio = lambda path: "data:audio/mpeg;base64,QUJD"
            module.find_ffmpeg = lambda: "/usr/bin/ffmpeg"
            module.get_audio_duration_seconds = lambda path, ffmpeg_path=None: 65.0

            def fake_segment(*args, **kwargs):
                calls["segmented"] = True
                return [
                    module.AudioChunk(Path("/tmp/chunk_000.mp3"), 0.0, 25.0),
                    module.AudioChunk(Path("/tmp/chunk_001.mp3"), 25.0, 50.0),
                    module.AudioChunk(Path("/tmp/chunk_002.mp3"), 50.0, 65.0),
                ]

            module.segment_audio_with_ffmpeg = fake_segment

            chunks = module.prepare_audio_chunks(
                Path("/tmp/long-small.mp3"),
                Path("/tmp/work"),
                segment_seconds=25,
                min_segment_seconds=10,
                max_segment_seconds=30,
                segment_mode="silence",
                silence_noise_db="-35dB",
                min_silence_seconds=0.45,
            )
        finally:
            module.data_url_for_audio = original_data_url
            module.find_ffmpeg = original_find_ffmpeg
            module.get_audio_duration_seconds = original_duration
            module.segment_audio_with_ffmpeg = original_segment

        self.assertTrue(calls.get("segmented"))
        self.assertEqual(len(chunks), 3)

    def test_markdown_metadata_does_not_include_api_key(self) -> None:
        module = load_module()

        markdown = module.render_transcript_markdown(
            source_audio=Path("/tmp/lesson.mp3"),
            model="mimo-v2.5-asr",
            base_url="https://token-plan-cn.xiaomimimo.com/v1",
            language="zh",
            chunks=[
                module.TranscriptChunk(
                    index=0,
                    start_seconds=0,
                    end_seconds=24.5,
                    source_path=Path("/tmp/chunk_000.mp3"),
                    text="课程从 residual connection 开始。",
                    summary="课程从 residual connection 开始。",
                    usage={"seconds": 3},
                )
            ],
        )

        self.assertIn("ASR 模型：mimo-v2.5-asr", markdown)
        self.assertIn("[00:00:00 --> 00:00:24]", markdown)
        self.assertIn("辅助摘要", markdown)
        self.assertIn("摘要：课程从 residual connection 开始。", markdown)
        self.assertNotIn("tp-", markdown)
        self.assertNotIn("api-key", markdown.lower())


if __name__ == "__main__":
    unittest.main()
