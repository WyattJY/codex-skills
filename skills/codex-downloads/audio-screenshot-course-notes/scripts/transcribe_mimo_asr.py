#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, NamedTuple


DEFAULT_BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1"
DEFAULT_MODEL = "mimo-v2.5-asr"
DEFAULT_WORK_ROOT = Path("/Volumes/T7/codex_cache/course_note_asr/mimo_asr")
DEFAULT_KEYCHAIN_SERVICE = "wyatt-mimo-asr-api-key"
BASE64_LIMIT_BYTES = 10 * 1024 * 1024
DEFAULT_SEGMENT_SECONDS = 25
DEFAULT_MIN_SEGMENT_SECONDS = 10
DEFAULT_MAX_SEGMENT_SECONDS = 30
DEFAULT_SILENCE_NOISE_DB = "-35dB"
DEFAULT_MIN_SILENCE_SECONDS = 0.45
DEFAULT_SUMMARY_CHARS = 180

FFMPEG_CANDIDATES = [
    "/opt/homebrew/bin/ffmpeg",
    "/usr/local/bin/ffmpeg",
    "/Users/jiangyu/Library/Application Support/bilibili/ffmpeg/ffmpeg",
    "/Applications/VideoFusion-macOS.app/Contents/Resources/ffmpeg",
    "/Applications/iShot.app/Contents/Resources/ARM/ffmpeg",
    "/Applications/iShot.app/Contents/Resources/Intel/ffmpeg",
]

TERM_REPLACEMENTS = [
    (re.compile(r"(?<![A-Za-z])(?:RPE|LPE|LP)(?![A-Za-z])", re.IGNORECASE), "RoPE"),
    (re.compile(r"(?:R\s*O\s*P\s*E|若\s*普|肉\s*普|绕\s*普)", re.IGNORECASE), "RoPE"),
    (re.compile(r"(?:西塔|希塔|奇塔|θ塔)", re.IGNORECASE), "theta"),
    (re.compile(r"(?:可锐|Q瑞|Q睿)", re.IGNORECASE), "query"),
    (re.compile(r"(?:K瑞|K睿)", re.IGNORECASE), "key"),
    (re.compile(r"(?:V瑞|V睿)", re.IGNORECASE), "value"),
    (re.compile(r"(?:马斯克|掩码)", re.IGNORECASE), "mask"),
    (re.compile(r"(?:层归一化|层规范化)", re.IGNORECASE), "LayerNorm"),
    (re.compile(r"(?:残差连接|残差链接)", re.IGNORECASE), "Residual Connection"),
]

SYSTEM_SOUND_RE = re.compile(
    r"(验证码|校验码|安全验证|请填写|通知音|系统提示|播放器提示|播放失败|微信收款|支付宝到账|短信验证码)"
)
COURSE_SIGNAL_RE = re.compile(
    r"(模型|训练|数据|代码|公式|矩阵|向量|注意力|Transformer|RoPE|位置编码|embedding|mask|loss|grounding|车位)",
    re.IGNORECASE,
)
SUMMARY_SIGNAL_RE = re.compile(
    r"(核心|关键|注意|问题|原因|机制|公式|代码|训练|数据|样本|mask|RoPE|theta|attention|Transformer|位置编码|矩阵|向量|损失|指标)",
    re.IGNORECASE,
)


class TranscriptChunk(NamedTuple):
    index: int
    start_seconds: float
    end_seconds: float
    source_path: Path
    text: str
    summary: str
    usage: dict[str, Any]


class AudioChunk(NamedTuple):
    path: Path
    start_seconds: float
    end_seconds: float


def format_timestamp(seconds: float) -> str:
    hours, rem = divmod(max(0, int(seconds)), 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def build_payload(*, data_url: str, model: str = DEFAULT_MODEL, language: str = "zh") -> dict[str, Any]:
    return {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": data_url,
                        },
                    }
                ],
            }
        ],
        "asr_options": {
            "language": language,
        },
    }


def extract_transcript_text(response: dict[str, Any]) -> str:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("MiMo ASR response has no choices.")
    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not isinstance(message, dict):
        raise ValueError("MiMo ASR response choice has no message.")
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("MiMo ASR response message has no transcript content.")
    return clean_transcript_text(content)


def clean_transcript_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^(?:</?think>|think>)\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^<(?:chinese|english|zh|en)>\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def normalize_course_terms(text: str) -> str:
    normalized = text
    for pattern, replacement in TERM_REPLACEMENTS:
        normalized = pattern.sub(replacement, normalized)
    return normalized


def is_non_course_system_sound(text: str) -> bool:
    compact = re.sub(r"\s+", "", text)
    if not compact or not SYSTEM_SOUND_RE.search(compact):
        return False
    if COURSE_SIGNAL_RE.search(compact):
        return False
    return len(compact) <= 180


def postprocess_transcript_text(text: str) -> str:
    processed = normalize_course_terms(clean_transcript_text(text))
    if is_non_course_system_sound(processed):
        return f"（非课程提示音：{processed}）"
    return processed


def split_sentences(text: str) -> list[str]:
    pieces = re.split(r"(?<=[。！？!?；;])\s*", text.strip())
    return [piece.strip() for piece in pieces if piece.strip()]


def summarize_chunk_text(text: str, *, max_chars: int = DEFAULT_SUMMARY_CHARS) -> str:
    clean = text.strip()
    if not clean or clean.startswith("（非课程提示音："):
        return ""
    sentences = split_sentences(clean)
    if not sentences:
        return clean[:max_chars].strip()

    selected: list[str] = []
    for sentence in sentences:
        if not selected or SUMMARY_SIGNAL_RE.search(sentence):
            selected.append(sentence)
        if len("".join(selected)) >= max_chars:
            break

    summary = "".join(selected) or sentences[0]
    if len(summary) > max_chars:
        summary = summary[: max_chars - 3].rstrip("，,。；; ") + "..."
    return summary.strip()


def build_overall_summary(chunks: list[TranscriptChunk], *, max_items: int = 12) -> list[str]:
    items: list[str] = []
    for chunk in chunks:
        if not chunk.summary:
            continue
        timestamp = format_timestamp(chunk.start_seconds)
        items.append(f"- `{timestamp}` {chunk.summary}")
        if len(items) >= max_items:
            break
    return items


def guess_audio_mime(path: Path) -> str:
    mime = mimetypes.guess_type(str(path))[0]
    if mime in {"audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3"}:
        return "audio/wav" if mime == "audio/x-wav" else mime
    if path.suffix.lower() == ".wav":
        return "audio/wav"
    if path.suffix.lower() == ".mp3":
        return "audio/mpeg"
    raise ValueError(f"MiMo ASR accepts wav/mp3 data URLs; unsupported file type: {path}")


def data_url_for_audio(path: Path, *, max_base64_bytes: int = BASE64_LIMIT_BYTES) -> str:
    mime = guess_audio_mime(path)
    estimated_base64_bytes = ((path.stat().st_size + 2) // 3) * 4
    if estimated_base64_bytes > max_base64_bytes:
        raise ValueError(
            f"Estimated base64 audio is {estimated_base64_bytes} bytes, above MiMo ASR limit "
            f"{max_base64_bytes}; segment or transcode the audio first."
        )
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    if len(encoded.encode("ascii")) > max_base64_bytes:
        raise ValueError(
            f"Base64 audio is {len(encoded)} bytes, above MiMo ASR limit {max_base64_bytes}; "
            "segment or transcode the audio first."
        )
    return f"data:{mime};base64,{encoded}"


def resolve_api_key(
    *,
    env_var: str = "MIMO_ASR_API_KEY",
    keychain_service: str | None = DEFAULT_KEYCHAIN_SERVICE,
    keychain_account: str | None = None,
) -> str:
    value = os.environ.get(env_var, "").strip()
    if value:
        return value
    if keychain_service:
        cmd = ["security", "find-generic-password", "-w", "-s", keychain_service]
        if keychain_account:
            cmd.extend(["-a", keychain_account])
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    raise RuntimeError(
        f"Missing MiMo ASR credential. Set {env_var} or add a Keychain item named {keychain_service}."
    )


def post_chat_completion(
    *,
    base_url: str,
    api_key: str,
    payload: dict[str, Any],
    timeout: float,
) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_text = exc.read().decode("utf-8", errors="replace")[:600]
        raise RuntimeError(f"MiMo ASR HTTP {exc.code}: {error_text}") from exc


def find_ffmpeg() -> str | None:
    found = shutil.which("ffmpeg")
    if found:
        return found
    for candidate in FFMPEG_CANDIDATES:
        path = Path(candidate)
        if path.exists() and os.access(path, os.X_OK):
            return str(path)
    return None


def find_ffprobe(ffmpeg_path: str | None = None) -> str | None:
    found = shutil.which("ffprobe")
    if found:
        return found
    if ffmpeg_path:
        sibling = Path(ffmpeg_path).with_name("ffprobe")
        if sibling.exists() and os.access(sibling, os.X_OK):
            return str(sibling)
    return None


def require_ffmpeg() -> str:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to segment or transcode long/non-mp3 audio for MiMo ASR.")
    return ffmpeg


def get_audio_duration_seconds(audio_path: Path, ffmpeg_path: str | None = None) -> float | None:
    ffprobe = find_ffprobe(ffmpeg_path)
    if ffprobe:
        result = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(audio_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            try:
                duration = float(result.stdout.strip())
                if duration > 0:
                    return duration
            except ValueError:
                pass

    ffmpeg = ffmpeg_path or find_ffmpeg()
    if not ffmpeg:
        return None
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(audio_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stderr)
    if not match:
        return None
    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = float(match.group(3))
    return hours * 3600 + minutes * 60 + seconds


def detect_silences(
    audio_path: Path,
    *,
    ffmpeg_path: str,
    noise_db: str = DEFAULT_SILENCE_NOISE_DB,
    min_silence_seconds: float = DEFAULT_MIN_SILENCE_SECONDS,
) -> list[tuple[float, float]]:
    result = subprocess.run(
        [
            ffmpeg_path,
            "-hide_banner",
            "-nostats",
            "-i",
            str(audio_path),
            "-af",
            f"silencedetect=noise={noise_db}:d={min_silence_seconds}",
            "-f",
            "null",
            "-",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    silences: list[tuple[float, float]] = []
    current_start: float | None = None
    for line in result.stderr.splitlines():
        start_match = re.search(r"silence_start:\s*([0-9.]+)", line)
        if start_match:
            current_start = float(start_match.group(1))
            continue
        end_match = re.search(r"silence_end:\s*([0-9.]+)", line)
        if end_match and current_start is not None:
            silences.append((current_start, float(end_match.group(1))))
            current_start = None
    return silences


def build_silence_aligned_ranges(
    *,
    duration_seconds: float,
    silences: list[tuple[float, float]],
    target_seconds: int,
    min_seconds: int,
    max_seconds: int,
) -> list[tuple[float, float]]:
    if duration_seconds <= 0:
        return []
    if not silences:
        return []

    ranges: list[tuple[float, float]] = []
    silence_points = sorted((start + end) / 2 for start, end in silences if end > start)
    start = 0.0
    while start < duration_seconds:
        remaining = duration_seconds - start
        if remaining <= max_seconds or (ranges and remaining < min_seconds):
            ranges.append((start, duration_seconds))
            break

        min_cut = start + min_seconds
        target_cut = start + target_seconds
        max_cut = min(start + max_seconds, duration_seconds)
        candidates = [point for point in silence_points if min_cut <= point <= max_cut]
        cut = min(candidates, key=lambda point: abs(point - target_cut)) if candidates else min(target_cut, max_cut)
        if cut <= start + 1:
            cut = min(start + target_seconds, duration_seconds)
        ranges.append((start, cut))
        start = cut

    if len(ranges) >= 2:
        last_start, last_end = ranges[-1]
        if last_end - last_start < min_seconds:
            prev_start, _ = ranges[-2]
            if last_end - prev_start <= max_seconds:
                ranges[-2] = (prev_start, last_end)
                ranges.pop()
    return ranges


def build_fixed_ranges(duration_seconds: float | None, segment_seconds: int) -> list[tuple[float, float]]:
    if not duration_seconds or duration_seconds <= 0:
        return []
    ranges: list[tuple[float, float]] = []
    start = 0.0
    while start < duration_seconds:
        end = min(start + segment_seconds, duration_seconds)
        ranges.append((start, end))
        start = end
    return ranges


def export_audio_ranges(
    *,
    audio_path: Path,
    work_dir: Path,
    ffmpeg_path: str,
    ranges: list[tuple[float, float]],
) -> list[AudioChunk]:
    chunk_dir = work_dir / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    for stale in chunk_dir.glob("chunk_*.mp3"):
        stale.unlink()
    chunks: list[AudioChunk] = []
    for index, (start, end) in enumerate(ranges):
        if end <= start:
            continue
        chunk_path = chunk_dir / f"chunk_{index:03d}.mp3"
        subprocess.run(
            [
                ffmpeg_path,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-ss",
                f"{start:.3f}",
                "-i",
                str(audio_path),
                "-t",
                f"{end - start:.3f}",
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-b:a",
                "64k",
                str(chunk_path),
            ],
            check=True,
        )
        chunks.append(AudioChunk(chunk_path, start, end))
    if not chunks:
        raise RuntimeError("ffmpeg produced no audio chunks.")
    return chunks


def segment_audio_with_ffmpeg(
    audio_path: Path,
    work_dir: Path,
    *,
    segment_seconds: int,
    min_segment_seconds: int,
    max_segment_seconds: int,
    segment_mode: str,
    silence_noise_db: str,
    min_silence_seconds: float,
) -> list[AudioChunk]:
    ffmpeg = require_ffmpeg()
    duration = get_audio_duration_seconds(audio_path, ffmpeg)
    ranges: list[tuple[float, float]] = []
    if segment_mode == "silence" and duration:
        silences = detect_silences(
            audio_path,
            ffmpeg_path=ffmpeg,
            noise_db=silence_noise_db,
            min_silence_seconds=min_silence_seconds,
        )
        ranges = build_silence_aligned_ranges(
            duration_seconds=duration,
            silences=silences,
            target_seconds=segment_seconds,
            min_seconds=min_segment_seconds,
            max_seconds=max_segment_seconds,
        )
    if not ranges:
        ranges = build_fixed_ranges(duration, segment_seconds)
    if not ranges:
        # Last-resort path when duration probing failed: let ffmpeg create fixed chunks.
        chunk_dir = work_dir / "chunks"
        chunk_dir.mkdir(parents=True, exist_ok=True)
        for stale in chunk_dir.glob("chunk_*.mp3"):
            stale.unlink()
        pattern = chunk_dir / "chunk_%03d.mp3"
        subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(audio_path),
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-b:a",
                "64k",
                "-f",
                "segment",
                "-segment_time",
                str(segment_seconds),
                "-reset_timestamps",
                "1",
                str(pattern),
            ],
            check=True,
        )
        paths = sorted(chunk_dir.glob("chunk_*.mp3"))
        return [
            AudioChunk(path, index * segment_seconds, (index + 1) * segment_seconds)
            for index, path in enumerate(paths)
        ]
    return export_audio_ranges(audio_path=audio_path, work_dir=work_dir, ffmpeg_path=ffmpeg, ranges=ranges)


def prepare_audio_chunks(
    audio_path: Path,
    work_dir: Path,
    *,
    segment_seconds: int,
    min_segment_seconds: int,
    max_segment_seconds: int,
    segment_mode: str,
    silence_noise_db: str,
    min_silence_seconds: float,
) -> list[AudioChunk]:
    ffmpeg = find_ffmpeg()
    duration = get_audio_duration_seconds(audio_path, ffmpeg) if ffmpeg else None
    if duration and duration > max_segment_seconds:
        return segment_audio_with_ffmpeg(
            audio_path,
            work_dir,
            segment_seconds=segment_seconds,
            min_segment_seconds=min_segment_seconds,
            max_segment_seconds=max_segment_seconds,
            segment_mode=segment_mode,
            silence_noise_db=silence_noise_db,
            min_silence_seconds=min_silence_seconds,
        )

    try:
        data_url_for_audio(audio_path)
        return [AudioChunk(audio_path, 0.0, duration or 0.0)]
    except ValueError:
        return segment_audio_with_ffmpeg(
            audio_path,
            work_dir,
            segment_seconds=segment_seconds,
            min_segment_seconds=min_segment_seconds,
            max_segment_seconds=max_segment_seconds,
            segment_mode=segment_mode,
            silence_noise_db=silence_noise_db,
            min_silence_seconds=min_silence_seconds,
        )


def render_transcript_markdown(
    *,
    source_audio: Path,
    model: str,
    base_url: str,
    language: str,
    chunks: list[TranscriptChunk],
) -> str:
    lines = [
        f"# {source_audio.stem} 逐字稿",
        "",
        f"- 源音频：`{source_audio}`",
        f"- ASR 模型：{model}",
        f"- Base URL：`{base_url}`",
        f"- 语言参数：{language}",
        f"- 分块数：{len(chunks)}",
        "",
        "## 辅助摘要",
        "",
    ]
    summary_lines = build_overall_summary(chunks)
    if summary_lines:
        lines.extend(summary_lines)
    else:
        lines.append("（暂无可用摘要，需人工复核逐字稿。）")
    lines.extend(
        [
            "",
            "## 短分段逐字稿",
            "",
        ]
    )
    for chunk in chunks:
        start = format_timestamp(chunk.start_seconds)
        end = format_timestamp(chunk.end_seconds) if chunk.end_seconds else "未知"
        lines.append(f"### [{start} --> {end}] chunk {chunk.index:03d}")
        lines.append("")
        if chunk.summary:
            lines.append(f"> 摘要：{chunk.summary}")
            lines.append("")
        lines.append(chunk.text.strip() or "（空转写结果，需人工复核）")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    *,
    output_md: Path,
    segments_json: Path,
    source_audio: Path,
    model: str,
    base_url: str,
    language: str,
    chunks: list[TranscriptChunk],
) -> None:
    output_md.parent.mkdir(parents=True, exist_ok=True)
    segments_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(
        render_transcript_markdown(
            source_audio=source_audio,
            model=model,
            base_url=base_url,
            language=language,
            chunks=chunks,
        ),
        encoding="utf-8",
    )
    segments_json.write_text(
        json.dumps(
            {
                "source_audio": str(source_audio),
                "model": model,
                "base_url": base_url,
                "language": language,
                "chunks": [
                    {
                        "index": chunk.index,
                        "start_seconds": chunk.start_seconds,
                        "end_seconds": chunk.end_seconds,
                        "source_path": str(chunk.source_path),
                        "text": chunk.text,
                        "summary": chunk.summary,
                        "usage": chunk.usage,
                    }
                    for chunk in chunks
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe audio with MiMo-V2.5-ASR.")
    parser.add_argument("audio", help="Audio file. wav/mp3 can be sent directly when small enough; other formats are chunked through ffmpeg.")
    parser.add_argument("--output-md", help="Transcript Markdown path.")
    parser.add_argument("--segments-json", help="Transcript segment JSON path.")
    parser.add_argument("--work-dir", help="Chunk/cache directory.")
    parser.add_argument("--base-url", default=os.environ.get("MIMO_ASR_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--language", default="zh", choices=["auto", "zh", "en"])
    parser.add_argument("--env-var", default="MIMO_ASR_API_KEY")
    parser.add_argument(
        "--keychain-service",
        default=os.environ.get("MIMO_ASR_KEYCHAIN_SERVICE", DEFAULT_KEYCHAIN_SERVICE),
        help=f"macOS Keychain generic-password service. Default: {DEFAULT_KEYCHAIN_SERVICE}",
    )
    parser.add_argument("--keychain-account")
    parser.add_argument(
        "--segment-mode",
        choices=["silence", "fixed"],
        default="silence",
        help="Use silence-aware short chunks by default; fixed uses even segment lengths.",
    )
    parser.add_argument("--segment-seconds", type=int, default=DEFAULT_SEGMENT_SECONDS)
    parser.add_argument("--min-segment-seconds", type=int, default=DEFAULT_MIN_SEGMENT_SECONDS)
    parser.add_argument("--max-segment-seconds", type=int, default=DEFAULT_MAX_SEGMENT_SECONDS)
    parser.add_argument("--silence-noise-db", default=DEFAULT_SILENCE_NOISE_DB)
    parser.add_argument("--min-silence-seconds", type=float, default=DEFAULT_MIN_SILENCE_SECONDS)
    parser.add_argument("--summary-chars", type=int, default=DEFAULT_SUMMARY_CHARS)
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--dry-run", action="store_true", help="Prepare chunks and output paths without calling MiMo.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.min_segment_seconds <= 0 or args.max_segment_seconds < args.min_segment_seconds:
        print("Invalid segment range: require 0 < min-segment-seconds <= max-segment-seconds.", file=sys.stderr)
        return 2
    if args.segment_seconds < args.min_segment_seconds or args.segment_seconds > args.max_segment_seconds:
        print("Invalid segment-seconds: keep it between min-segment-seconds and max-segment-seconds.", file=sys.stderr)
        return 2
    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.exists():
        print(f"Audio file not found: {audio_path}", file=sys.stderr)
        return 2

    work_dir = Path(args.work_dir).expanduser() if args.work_dir else DEFAULT_WORK_ROOT / audio_path.stem
    output_md = Path(args.output_md).expanduser() if args.output_md else audio_path.with_name(f"{audio_path.stem}_mimo_asr_逐字稿.md")
    segments_json = (
        Path(args.segments_json).expanduser()
        if args.segments_json
        else output_md.with_name(f"{output_md.stem}_segments.json")
    )
    work_dir.mkdir(parents=True, exist_ok=True)
    chunk_plan = prepare_audio_chunks(
        audio_path,
        work_dir,
        segment_seconds=args.segment_seconds,
        min_segment_seconds=args.min_segment_seconds,
        max_segment_seconds=args.max_segment_seconds,
        segment_mode=args.segment_mode,
        silence_noise_db=args.silence_noise_db,
        min_silence_seconds=args.min_silence_seconds,
    )

    if args.dry_run:
        print(
            json.dumps(
                {
                    "audio": str(audio_path),
                    "chunks": [
                        {
                            "path": str(chunk.path),
                            "start_seconds": chunk.start_seconds,
                            "end_seconds": chunk.end_seconds,
                        }
                        for chunk in chunk_plan
                    ],
                    "output_md": str(output_md),
                    "segments_json": str(segments_json),
                    "model": args.model,
                    "base_url": args.base_url,
                    "language": args.language,
                    "segment_mode": args.segment_mode,
                    "segment_seconds": args.segment_seconds,
                    "min_segment_seconds": args.min_segment_seconds,
                    "max_segment_seconds": args.max_segment_seconds,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    api_key = resolve_api_key(
        env_var=args.env_var,
        keychain_service=args.keychain_service,
        keychain_account=args.keychain_account,
    )
    chunks: list[TranscriptChunk] = []
    for index, chunk in enumerate(chunk_plan):
        payload = build_payload(
            data_url=data_url_for_audio(chunk.path),
            model=args.model,
            language=args.language,
        )
        response = post_chat_completion(
            base_url=args.base_url,
            api_key=api_key,
            payload=payload,
            timeout=args.timeout,
        )
        text = postprocess_transcript_text(extract_transcript_text(response))
        chunks.append(
            TranscriptChunk(
                index=index,
                start_seconds=chunk.start_seconds,
                end_seconds=chunk.end_seconds,
                source_path=chunk.path,
                text=text,
                summary=summarize_chunk_text(text, max_chars=args.summary_chars),
                usage=response.get("usage") if isinstance(response.get("usage"), dict) else {},
            )
        )

    write_outputs(
        output_md=output_md,
        segments_json=segments_json,
        source_audio=audio_path,
        model=args.model,
        base_url=args.base_url,
        language=args.language,
        chunks=chunks,
    )
    print(json.dumps({"ok": True, "output_md": str(output_md), "segments_json": str(segments_json), "chunks": len(chunks)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
