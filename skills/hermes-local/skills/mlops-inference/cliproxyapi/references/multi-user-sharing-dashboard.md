# CLIProxyAPI multi-user sharing, usage, quota, and dashboard design

Use this reference when a user wants to share a CPA/CLIProxyAPI-backed Codex/ChatGPT account pool with other people, give each person a separate key, track usage per person, inspect remaining rolling quotas, or design a management dashboard.

## What to provide to users

Share only client connection details:

- `base_url`: `http://<host>:8317/v1` or preferably `https://<domain>/v1`
- model, e.g. `gpt-5-codex`
- per-user client API key
- Codex CLI `~/.codex/config.toml` and `~/.codex/auth.json` snippets

Do not share:

- OpenAI/Codex login credentials
- server SSH credentials
- CLIProxyAPI management key
- OAuth credential files under `auth-dir`
- a single shared API key for everyone, if attribution/revocation matters

Codex CLI snippet:

```toml
model_provider = "cliproxyapi"
model = "gpt-5-codex"
model_reasoning_effort = "xhigh"

[model_providers.cliproxyapi]
name = "cliproxyapi"
base_url = "https://<domain>/v1"
wire_api = "responses"
```

`~/.codex/auth.json`:

```json
{
  "OPENAI_API_KEY": "<that-user-cpa-key>"
}
```

## Per-user API keys

CLIProxyAPI supports multiple client API keys in config:

```yaml
api-keys:
  - "cpa_user_a_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  - "cpa_user_b_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Generate strong keys:

```bash
python3 - <<'PY'
import secrets
for name in ['user1', 'user2', 'user3', 'user4', 'user5']:
    print(f'{name}: cpa_{secrets.token_urlsafe(24)}')
PY
```

Operational guidance:

- Maintain a separate owner mapping: user nickname -> key hash / prefix / suffix / status.
- Do not store or display raw keys unless necessary; show masks like `cpa_abcd...9xyz`.
- Rotate by adding a new key, asking the user to switch, then removing the old key.
- Revoke a user by removing only their key and hot-reloading/restarting CPA.

## Usage tracking

Enable usage publishing:

```yaml
usage-statistics-enabled: true
redis-usage-queue-retention-seconds: 3600
```

CLIProxyAPI exposes a minimal Redis RESP usage queue on the same port. It requires the management key and supports `AUTH`, `LPOP <key> [count]`, `RPOP <key> [count]`, and `SUBSCRIBE usage`.

Each usage event includes fields suitable for per-user attribution:

- `timestamp`
- `latency_ms`
- `source` / `auth_index` for the upstream account used
- `provider`
- `model` / `alias`
- `endpoint`
- `auth_type`
- `api_key` for the client key used
- `request_id`
- `failed`
- `tokens.input_tokens`
- `tokens.output_tokens`
- `tokens.reasoning_tokens`
- `tokens.cached_tokens`
- `tokens.total_tokens`

Collector pattern:

1. Connect to the RESP queue using the management key.
2. Poll `RPOP queue 100` frequently or subscribe to `SUBSCRIBE usage`.
3. Persist events to SQLite/Postgres.
4. Map event `api_key` to a user/key record.
5. Aggregate by user, model, key, upstream account, and time windows.

Useful windows: today, 1h, 5h, 24h, 7d, 30d. Useful metrics: request count, total tokens, input/output/reasoning/cached tokens, success rate, failed count, average latency, last request time.

## Quota / remaining capacity view

Codex/ChatGPT subscription quota is not a conventional dollar balance. Present it as rolling quota windows:

Per upstream account:

- status: `ready`, `cooling`, `exhausted`, `auth_failed`, `network_error`
- Codex 5h used/remaining percentage and reset time
- Codex 7d used/remaining percentage and reset time
- optional credits balance if available
- recent failure reason: `401`, `429`, `quota_exceeded`, network error
- recent success rate

Pool summary:

- ready accounts / total accounts
- average/min remaining 5h quota
- average/min remaining 7d quota
- next account recovery/reset time
- current health score

Reference projects for quota/use inspiration:

- `router-for-me/Cli-Proxy-API-Management-Center`: official management WebUI for config, keys, credentials, logs.
- `Willxup/cpa-usage-keeper`: SQLite-backed persistent usage tracker and dashboard.
- `AllenReder/CLIProxyAPI-Quota-Inspector`: terminal quota inspector for Codex 5h/7d and other providers.
- `zhanglunet/cliproxyapi-usage-dashboard`: local Python + SQLite usage/quota dashboard.
- `sxjeru/CLIProxyAPI-Monitor`: heavier Next.js/Postgres visualization stack.
- `BlueSkyXN/CPA-Panel-LTS`: LTS panel preserving full usage statistics from older CPA lines.

## Dashboard information architecture

Overview:

- today requests
- today tokens
- recent 5h tokens
- active users
- success rate
- average latency
- available upstream accounts
- pool health score
- 24h request bars, token trend, model split, failure-rate trend

Users & Keys:

- user name
- masked key
- status: active / paused / revoked
- today requests
- today tokens
- 7d tokens
- success rate
- last request
- daily/monthly token limits if a gateway enforces limits
- actions: copy config, pause, rotate, revoke

Pool Quota:

- provider
- masked upstream account
- status
- 5h quota progress
- 7d quota progress
- reset time
- recent success rate / recent error

Requests:

- filters: user, key, model, upstream account, status, time range
- columns: time, user, model, upstream account, input/output/reasoning/cached/total tokens, latency, status, request_id

Settings:

- CPA base URL
- management key stored server-side only, never echoed to the browser
- queue retention
- backup settings
- alert thresholds: 5h low, 7d low, failure-rate high, unusual per-user growth

## Enforcement vs visibility

For visibility only, multiple CPA keys plus a usage collector are enough.

For enforced per-user limits, concurrency caps, or paid-tier quotas, add a gateway before CLIProxyAPI:

```text
Client
  -> gateway: user auth, API-key validation, quotas, rate limits, logs
  -> CLIProxyAPI with an internal master key
  -> Codex/ChatGPT account pool
```

CLIProxyAPI `api-keys` are good for authentication and attribution. A separate gateway is a cleaner place for hard per-user daily/monthly token limits and concurrent request caps.

## Capacity planning

Small pools are usually quota-bound, not memory-bound. For about 5 concurrent streaming requests, budget roughly:

- CLIProxyAPI core: 60-150 MB
- lightweight usage collector + SQLite dashboard: 80-250 MB
- Caddy/Nginx: 20-80 MB
- OS/service headroom: 200-400 MB
- 5 active streams extra: 50-150 MB

Practical guidance:

- 1 GB VPS: usually enough for CLIProxyAPI + lightweight SQLite dashboard for ~5 users, if not running a heavy web stack.
- 2 GB VPS: recommended for stability.
- Next.js/Postgres/Docker dashboards should start at 2 GB+.
- HTTPS is strongly recommended before sharing keys over the public internet.
