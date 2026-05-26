---
name: weixin-daily-push
description: Use to prepare Wyatt's daily Hermes research idea or workflow notification for an isolated Weixin gateway without leaking or double-running tokens.
version: 0.1.0
author: WyattJY Hermes local workflow
---
# Weixin Daily Push

## Workflow
1. Read the latest daily idea, RUN_CARD, ERROR_CARD, or release summary.
2. Compress it into a concise private-message payload.
3. Verify that the intended gateway uses an isolated `HERMES_HOME`.
4. Before claiming delivery, verify the actual delivery channel is configured/listed. If Hermes has no connected Weixin target, do not mark the run delivered.
5. Do not start a gateway or send a message unless Wyatt explicitly asks.
6. If sending fails because the channel is not configured, write the exact final payload to a `WEIXIN_OUTBOX/*.pending.weixin.md` file, report that path, and leave the source run status as `ready`/undelivered.
7. For 24-hour operation, use the server systemd template under `memory/server/`.

## Hard rules
- Never print or store `WEIXIN_TOKEN`, account JSON, cookies, sessions, or pairing files.
- Do not run the same token on the Mac and server at the same time.
- Keep group policy disabled until Wyatt explicitly tests and enables it.
- Prefer private DM pairing and short final notifications; avoid noisy progress messages.

## Wyatt local pitfall
- Wyatt's Weixin credentials may live in the base Hermes home `/Users/jiangyu/.hermes`, while the active orchestrator profile is `/Users/jiangyu/.hermes/profiles/orchestrator`. If `send_message(target="weixin")` says unconfigured, first check whether the base home has `WEIXIN_*` and whether the profile lacks them; do not copy or duplicate the token.
- For an explicitly approved one-shot push, run from `/Users/jiangyu/.hermes/hermes-agent` with the venv Python, set `HERMES_HOME=/Users/jiangyu/.hermes` and `HOME=/Users/jiangyu` inside the process, load `/Users/jiangyu/.hermes/.env` internally without printing values, then call `gateway.platforms.weixin.send_weixin_direct(...)` to `WEIXIN_HOME_CHANNEL`. After success only, mark the research run delivered and move the outbox file from `.pending.weixin.md` to `.delivered.weixin.md`.
- For an explicitly approved base Weixin gateway restart, do **not** rely on `HERMES_HOME=/Users/jiangyu/.hermes` alone when `/Users/jiangyu/.hermes/active_profile` is `orchestrator`; Hermes treats root `HERMES_HOME` as a root and still honors the sticky active profile. Start the base/default gateway with: `cd /Users/jiangyu/.hermes/hermes-agent && unset HERMES_HOME && HOME=/Users/jiangyu /Users/jiangyu/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main --profile default gateway run --replace`. Verify `/Users/jiangyu/.hermes/gateway_state.json` shows `platforms.weixin.state=connected` and that `/Users/jiangyu/.hermes/logs/gateway.log` says `Gateway running with 1 platform(s)`.
- A generated report plus an intended cron is not proof of delivery. Check scheduler/job state, run `delivered_at`/done markers, and the configured messaging target before answering whether a push went out.
- If delivery cannot be completed, preserve an outbox copy and state clearly that the message was not sent.

