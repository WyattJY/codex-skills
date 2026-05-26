# CLIProxyAPI for Codex OAuth proxying

Use this when the user wants to expose a Codex/OpenAI OAuth-backed account through a local or remote OpenAI-compatible API endpoint for other clients (Codex CLI, Hermes custom provider, OpenAI SDK-style clients).

Upstream project: `router-for-me/CLIProxyAPI`.

## Endpoint shape

For a default CLIProxyAPI server on port `8317`, the client `base_url` is:

```text
http://127.0.0.1:8317/v1
```

For a remote server:

```text
http://<server-ip-or-domain>:8317/v1
```

If HTTPS/reverse proxy is configured:

```text
https://<domain>/v1
```

Do not include endpoint-specific suffixes like `/v1/responses` or `/v1/chat/completions` in the base URL. Clients append those.

## Codex CLI client config

`~/.codex/config.toml`:

```toml
model_provider = "cliproxyapi"
model = "gpt-5-codex"
model_reasoning_effort = "xhigh"

[model_providers.cliproxyapi]
name = "cliproxyapi"
base_url = "http://<host>:8317/v1"
wire_api = "responses"
```

`model_reasoning_effort` accepts `minimal`, `low`, `medium`, `high`, and `xhigh` in current Codex CLI docs; use `xhigh` for maximum reasoning when the selected model supports it.

`~/.codex/auth.json`:

```json
{
  "OPENAI_API_KEY": "<cliproxyapi-api-key>"
}
```

## Server install outline

1. Download the latest Linux release asset from GitHub releases, matching architecture:
   - `CLIProxyAPI_<version>_linux_amd64.tar.gz`
   - `CLIProxyAPI_<version>_linux_aarch64.tar.gz`
2. Extract `cli-proxy-api` to `/opt/cliproxyapi/cli-proxy-api`.
3. Put config at `/etc/cliproxyapi/config.yaml`.
4. Store OAuth credentials under a service-owned directory like `/var/lib/cliproxyapi/auths`.
5. Run under a dedicated system user, e.g. `cliproxyapi`.
6. Start via systemd with `ExecStart=/opt/cliproxyapi/cli-proxy-api --config /etc/cliproxyapi/config.yaml`.
7. Open TCP 8317 in both host firewall and cloud security group if external clients should connect.

## Minimal config skeleton

```yaml
host: "0.0.0.0"
port: 8317

tls:
  enable: false
  cert: ""
  key: ""

remote-management:
  allow-remote: false
  secret-key: "<random-management-secret>"
  disable-control-panel: false

auth-dir: "/var/lib/cliproxyapi/auths"

api-keys:
  - "<random-client-api-key>"

debug: false
logging-to-file: false
usage-statistics-enabled: false
proxy-url: ""

request-retry: 3
max-retry-credentials: 0
max-retry-interval: 30

routing:
  strategy: "round-robin"
  session-affinity: true
  session-affinity-ttl: "1h"

quota-exceeded:
  switch-project: true
  switch-preview-model: true
  antigravity-credits: true
```

## Codex OAuth login on remote server

CLIProxyAPI Codex OAuth uses local callback port `1455`. On a remote server, create an SSH tunnel from the local machine before login:

```bash
ssh -L 1455:127.0.0.1:1455 <user>@<server>
```

Then, inside that SSH session (or another one while the tunnel remains open), run the login as the same user that owns the service credentials:

```bash
sudo -u cliproxyapi HOME=/var/lib/cliproxyapi \
  /opt/cliproxyapi/cli-proxy-api \
  --config /etc/cliproxyapi/config.yaml \
  --codex-login --no-browser
```

Open the printed OpenAI authorization URL in the local browser. The redirect to `localhost:1455` will be forwarded to the server through the SSH tunnel. On success, credentials are saved under the configured `auth-dir` (example filename: `codex-<email>-pro.json`).

After login, restart the service if needed:

```bash
sudo systemctl restart cliproxyapi
```

CLIProxyAPI also has a file watcher, so new auth files may load automatically, but a restart is a simple verification step.

## Verification

List models:

```bash
curl http://<host>:8317/v1/models \
  -H 'Authorization: Bearer <cliproxyapi-api-key>'
```

Responses API:

```bash
curl http://<host>:8317/v1/responses \
  -H 'Authorization: Bearer <cliproxyapi-api-key>' \
  -H 'Content-Type: application/json' \
  -d '{"model":"gpt-5-codex","input":"Say hi in one sentence."}'
```

## Security notes

- Do not put real server passwords, OpenAI credentials, OAuth files, or generated client API keys into skills or templates.
- Generate fresh API keys per deployment and rotate if exposed.
- If a password was pasted into a chat, advise the user to rotate it after deployment.
- Prefer SSH keys and disable password login for production servers.
- Remind the user to check whether sharing a subscription-backed account this way is allowed by the relevant service terms.
