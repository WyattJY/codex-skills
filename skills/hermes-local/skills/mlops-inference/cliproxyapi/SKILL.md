---
name: cliproxyapi
description: "CLIProxyAPI: expose ChatGPT/Codex/Claude/Gemini OAuth subscriptions as OpenAI/Claude/Gemini-compatible HTTP APIs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [proxy, oauth, codex, claude-code, gemini-cli, openai-compatible, subscription]
    homepage: https://github.com/router-for-me/CLIProxyAPI
    docs: https://help.router-for.me/
    related_skills: [codex, claude-code, hermes-agent]
---

# CLIProxyAPI

Go-based proxy server (`router-for-me/CLIProxyAPI`) that wraps OAuth-only AI subscriptions — ChatGPT Plus/Pro/Codex, Claude Pro/Code, Gemini CLI, Antigravity — and re-exposes them as OpenAI / OpenAI Responses / Claude Messages / Gemini compatible HTTP endpoints. Lets the user point any OpenAI-SDK-compatible client (Hermes, Cursor, Cline, OpenCode, Continue, custom scripts) at a local proxy and consume their existing subscription quota without API keys.

## When to use this skill

- User wants to use a ChatGPT/Codex/Claude/Gemini **subscription account** (no API billing) from API clients
- User says "CLIProxyAPI", "CPA", "cli proxy", or asks how to use their Codex/Claude Plus account from another tool
- User wants to pool multiple OAuth accounts with round-robin load balancing
- User wants OpenAI-compatible endpoint that fronts Codex Responses API

Do NOT confuse with:
- **ACP** (Agent Client Protocol) — editor integration, totally different. The user has used "cpa" as a typo/shorthand for CLIProxyAPI before; if they say "cpa" and context isn't clear, ask.
- **OpenAI Codex CLI** — `@openai/codex` npm package, a coding agent CLI. CLIProxyAPI can authenticate via the Codex OAuth flow but is not the Codex CLI itself.

## Install (macOS, current as of v7.0.7)

Apple Silicon:
```bash
mkdir -p ~/Apps/cliproxyapi && cd ~/Apps/cliproxyapi
curl -LO https://github.com/router-for-me/CLIProxyAPI/releases/latest/download/CLIProxyAPI_7.0.7_darwin_aarch64.tar.gz
tar -xzf CLIProxyAPI_*_darwin_aarch64.tar.gz
xattr -dr com.apple.quarantine ./CLIProxyAPI 2>/dev/null || true
chmod +x ./CLIProxyAPI
```

Intel: swap `aarch64` for `amd64`. Linux/Windows assets are in the same release. Always check `https://api.github.com/repos/router-for-me/CLIProxyAPI/releases/latest` for the current tag — version moves fast.

## Config

```bash
curl -LO https://raw.githubusercontent.com/router-for-me/CLIProxyAPI/main/config.example.yaml
cp config.example.yaml config.yaml
```

Key fields to set:
- `port` — listen port (default 8317)
- `auth-dir` — where OAuth tokens are stored (default `./auths`)
- `api-keys` — list of client-side bearer keys you invent (e.g. `sk-mylocal-xyz`); clients send these in `Authorization: Bearer ...`
- `proxy-url` — set if the host needs an outbound proxy to reach openai.com / anthropic.com / google.com
- `remote-management.secret-key` — optional, for the Management API and Web UI

Detailed options: https://help.router-for.me/configuration/options.html

## OAuth login per provider

Each subscription is added via a one-time CLI login flow. Tokens land in `auth-dir`. Running the same login again adds another account → automatic round-robin.

```bash
./CLIProxyAPI --codex-login          # ChatGPT/Codex subscription
./CLIProxyAPI --claude-login         # Claude Pro / Claude Code
./CLIProxyAPI --gemini-cli-login     # Gemini CLI subscription
./CLIProxyAPI --antigravity-login    # Antigravity
```

Each prints a URL — open in browser, sign in, authorize, done. If outbound network is blocked, prepend `--proxy-url http://host:port` or `socks5://...`.

## Run

```bash
./CLIProxyAPI --config config.yaml
```

Daemonize on macOS without writing a plist:
```bash
tmux new -d -s cpa "cd ~/Apps/cliproxyapi && ./CLIProxyAPI --config config.yaml"
```

Logs go to stdout; capture with tmux pipe-pane or redirect to a file.

## Endpoint surfaces

Same server exposes multiple protocol surfaces simultaneously:

| Surface | Path | Use for |
|---------|------|---------|
| OpenAI Chat Completions | `/v1/chat/completions` | Generic OpenAI-SDK clients |
| OpenAI Responses | `/v1/responses` | Codex-native (better tool/function fidelity for GPT-5/Codex) |
| Anthropic Messages | `/v1/messages` | Claude-SDK clients, Claude Code |
| Gemini generateContent | `/v1beta/models/{model}:generateContent` | Gemini SDK |
| Provider-pinned | `/api/provider/{provider}/v1/...` | Force a specific upstream when model names overlap |

Auth: `Authorization: Bearer <one of api-keys>` on every request.

Quick smoke test:
```bash
curl http://127.0.0.1:8317/v1/chat/completions \
  -H "Authorization: Bearer sk-mylocal-xyz" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5","messages":[{"role":"user","content":"hi"}]}'
```

## Integrating with Hermes Agent

Treat the proxy as a generic OpenAI-compatible provider. In `~/.hermes/config.yaml`:

```yaml
model:
  base_url: http://127.0.0.1:8317/v1
  api_key: sk-mylocal-xyz
  default: gpt-5         # or claude-sonnet-4-5, gemini-2.5-pro, etc.
```

Then `hermes model` to pick the model, or use a custom provider entry so it can coexist with other providers. The user gets their Codex/Claude/Gemini subscription as a Hermes provider with zero API billing.

## Multi-account pooling

Just run the same login command multiple times — each invocation appends a new credential file under `auth-dir/`. The proxy load-balances round-robin. Pull credentials by deleting individual files in `auth-dir/`. For dashboards over quota status see CPA Usage Keeper, CLIProxyAPI Quota Inspector, CPA-Manager — these are sister projects, not built in since v6.10.

## Multi-user sharing, per-user keys, usage, and quota dashboards

When sharing a CPA endpoint with several people, give each user a separate client API key in `api-keys`; do not share OAuth tokens, server credentials, or the management key. Enable `usage-statistics-enabled: true` plus `redis-usage-queue-retention-seconds: 3600` to publish per-request usage events. The Redis-compatible usage queue includes the client `api_key`, token counts, model, upstream `source`/`auth_index`, latency, failure state, and request id, so a collector can persist events to SQLite/Postgres and aggregate by user/key/model/account/time window.

For remaining Codex/ChatGPT pool capacity, present rolling-window quota rather than dollar balance: per upstream account show 5h and 7d used/remaining percentages, reset times, ready/cooling/exhausted/auth_failed status, and recent failure reasons. For hard per-user quotas or concurrency limits, place a small gateway in front of CLIProxyAPI; CPA keys alone are best for authentication and attribution, not full tenant enforcement.

See `references/multi-user-sharing-dashboard.md` for dashboard IA, schema ideas, reference projects, and small-pool memory planning.

## Pitfalls

- **macOS Gatekeeper**: first run may be blocked. `xattr -dr com.apple.quarantine ./CLIProxyAPI` fixes it.
- **Codex Responses vs Chat Completions**: GPT-5/Codex models behave best via `/v1/responses`. Some clients only speak `/v1/chat/completions` — the proxy auto-translates, but tool-call fidelity is better on Responses.
- **OAuth tokens expire / get revoked** by upstream (esp. when ChatGPT detects "unusual usage"). Re-run the matching `--*-login` to refresh. Don't capture "Codex login broke" as a permanent rule — it's a refresh task.
- **Port conflict**: 8317 is the default; change `port` in config.yaml if something else uses it.
- **Outbound network from China**: set `proxy-url` in config AND pass `--proxy-url` to the login command, otherwise OAuth handshake fails silently with a timeout.
- **"cpa" acronym**: when ambiguous, ask the user — they may mean CLIProxyAPI or ACP (editor protocol) or something else.

## See also

- Codex provider config: https://help.router-for.me/configuration/provider/codex.html
- Agent-client config: https://help.router-for.me/agent-client/codex.html
- Management API: https://help.router-for.me/management/api.html
