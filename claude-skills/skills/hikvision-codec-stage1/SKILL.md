---
name: hikvision-codec-stage1
description: Use when Wyatt mentions Hikvision, 海康威视, research institute onboarding, intelligent algorithm department, C video encode/decode, codec latency, streaming response, FFmpeg, H264/H265, RTSP, or stage-one work reports.
---


# Hikvision Codec Stage 1
## Claude Code Adaptation

- This copy is prepared for Claude Code personal or project skills.
- Resolve bundled files relative to ${CLAUDE_SKILL_DIR} when Claude Code exposes it; otherwise use the local skill directory.
- Map old agent/tool wording to the closest Claude Code capability by intent.

## Overview

This skill routes Wyatt's future stage-one Hikvision work into a safe response workflow for C-language video encode/decode tasks. It is for task understanding, learning plans, debugging strategy, performance response, and reporting. It is not a place to store company source code or raw video data.

## What This Solves

- Fast response to unfamiliar C/video-codec tasks.
- Turning vague assignments into reproducible task cards.
- Debugging encode/decode, stream, timestamp, buffer, latency, crash, and performance issues.
- Converting daily work into weekly and stage reports.
- Keeping Claude Code useful without leaking company confidential material.

## Safety Boundary

- Do not store company source code, raw video files, camera streams, credentials, internal datasets, customer data, or private documents in memory.
- Prefer sanitized screenshots, anonymized stack traces, aggregate metrics, command shapes, and self-written minimal repros.
- If company policy forbids sharing snippets, ask Wyatt for behavior descriptions plus allowed metrics only.
- Write memory as task pattern and lessons, not proprietary implementation.

## Agent Modes

| Mode | Purpose | Typical output |
| --- | --- | --- |
| Onboarding mentor | Explain task, vocabulary, and learning path. | `LEARNING_PLAN.md`, glossary, first-week checklist |
| C codec debugger | Diagnose C, memory, pointer, thread, queue, and bitstream issues. | root-cause tree, safe repro plan, test list |
| Performance responder | Handle latency, FPS, CPU/GPU, memory, queue backlog, and dropped-frame issues. | profiling plan, metrics table, fix priority |
| Report writer | Convert work evidence into daily/weekly/stage report. | daily log, weekly report, stage-one summary |
| Memory archivist | Save reusable lessons after task close. | case, bug, final prompt, prevention checklist |

## Response Workflow

1. Classify the assignment: learning, bug, feature, performance, integration, report, or review.
2. Ask for allowed evidence only: task wording, expected behavior, actual behavior, logs, screenshots, metrics, sanitized snippets, or public docs.
3. Create a `CODEC_TASK_CARD`: goal, module, input/output, environment, success criterion, safety boundary.
4. Build the codec path map: capture/input -> demux -> decode -> preprocess -> algorithm -> encode -> mux/stream/output.
5. Identify the response problem type:
   - startup time
   - per-frame latency
   - throughput/FPS
   - dropped frames
   - A/V sync or PTS/DTS
   - buffer/queue backlog
   - memory leak or crash
   - CPU/GPU bottleneck
6. Produce a minimal next action: one command, one metric table, one code-reading target, or one experiment.
7. Verify with before/after evidence and write a short report section.
8. At close, archive only the safe lesson: symptom, cause category, fix pattern, prevention.

## C / Codec Checklist

- Build flags: warnings, sanitizer availability, optimization level, debug symbols.
- Memory: ownership, lifetime, `malloc/free`, buffer size, alignment, use-after-free, double free.
- Threads: producer/consumer queue, mutex/condition, backpressure, shutdown order.
- Timestamps: PTS/DTS, timebase conversion, monotonic clock, frame reorder.
- Bitstream: Annex B vs AVCC, SPS/PPS/VPS, keyframe, GOP, NAL parsing.
- Encode/decode: pixel format, resolution, stride, color range, hardware/software path.
- Streaming: RTSP/RTP jitter, packet loss, reconnection, buffering, timeout.
- Performance: per-stage latency, FPS, CPU, GPU/NPU, memory, queue depth.

## Report Shape

Daily report:
- Today task
- Evidence received
- What was verified
- Current blocker
- Next command / next reading target

Weekly report:
- Workstream summary
- Completed items
- Bugs and root causes
- Metrics before/after
- Risks and support needed
- Next-week plan

Stage-one summary:
- What I learned
- What tasks I handled
- What problems I solved
- What still needs mentoring
- Reusable checklist for the next stage

## Templates

- `templates/CODEC_TASK_CARD.md`
- `templates/DEBUG_RESPONSE_CARD.md`
- `templates/WEEKLY_STAGE_REPORT.md`

## Hard Rules

- Never request or store raw company source code or raw camera/video data.
- Never ask Wyatt to bypass company security controls.
- Do not claim a codec fix without before/after evidence.
- If the task is about latency or response, always request per-stage timing, queue depth, FPS, and CPU/GPU/memory metrics if allowed.
- If evidence is insufficient, output the smallest safe evidence request instead of guessing.
