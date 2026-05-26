# Weixin / WeChat gateway QR setup notes

Use this reference when configuring Hermes Gateway for personal WeChat via the Weixin/iLink adapter, especially from an agent/tool session where the full interactive setup wizard is awkward.

## Core flow

1. Ensure runtime deps are present in the Hermes venv:
   ```bash
   cd ~/.hermes/hermes-agent
   source venv/bin/activate  # or .venv/bin/activate
   python - <<'PY'
   import importlib.util
   for name in ['aiohttp', 'cryptography', 'qrcode']:
       print(name, bool(importlib.util.find_spec(name)))
   PY
   ```
2. `aiohttp` and `cryptography` are required for the adapter. `qrcode` is optional but useful so the QR renders in the terminal.
3. Some Hermes-installed venvs may not have `pip`; bootstrap it with:
   ```bash
   python -m ensurepip --upgrade
   python -m pip install qrcode
   ```
   Do not record this as a durable environment fact; it is just a setup-state fix.
4. Preferred user-facing setup remains:
   ```bash
   hermes gateway setup
   ```
   Select **Weixin / WeChat**, scan the QR code, confirm on phone, then restart the gateway.

## Non-interactive/agent-assisted QR login helper

If `hermes gateway setup` is hard to drive through a PTY menu, call the adapter helper directly and save the same env vars the wizard saves. Run in PTY/background mode so the QR code is visible and the process can wait while the user scans.

```python
# /tmp/hermes_weixin_setup_once.py
import asyncio
from hermes_cli.config import get_hermes_home, get_env_value, save_env_value
from gateway.platforms.weixin import qr_login

async def main() -> int:
    print('Starting Weixin QR login...', flush=True)
    credentials = await qr_login(str(get_hermes_home()))
    if not credentials:
        print('WEIXIN_SETUP_FAILED: QR login did not complete.', flush=True)
        return 2

    account_id = credentials.get('account_id', '')
    token = credentials.get('token', '')
    base_url = credentials.get('base_url', '')
    user_id = credentials.get('user_id', '')

    save_env_value('WEIXIN_ACCOUNT_ID', account_id)
    save_env_value('WEIXIN_TOKEN', token)
    if base_url:
        save_env_value('WEIXIN_BASE_URL', base_url)
    save_env_value('WEIXIN_CDN_BASE_URL', get_env_value('WEIXIN_CDN_BASE_URL') or 'https://novac2c.cdn.weixin.qq.com/c2c')

    # Conservative defaults: only the scanner can DM Hermes; groups off.
    save_env_value('WEIXIN_DM_POLICY', 'allowlist')
    save_env_value('WEIXIN_ALLOW_ALL_USERS', 'false')
    save_env_value('WEIXIN_ALLOWED_USERS', user_id)
    save_env_value('WEIXIN_GROUP_POLICY', 'disabled')
    save_env_value('WEIXIN_GROUP_ALLOWED_USERS', '')
    if user_id:
        save_env_value('WEIXIN_HOME_CHANNEL', user_id)

    print('WEIXIN_CONFIGURED', flush=True)
    print(f'ACCOUNT_ID={account_id}', flush=True)
    if user_id:
        print(f'USER_ID={user_id}', flush=True)
    return 0

raise SystemExit(asyncio.run(main()))
```

Run:
```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
python /tmp/hermes_weixin_setup_once.py
```

## Verification

After QR confirmation:

```bash
hermes gateway restart
hermes gateway status
grep -i 'weixin\|connected\|startup failed' ~/.hermes/logs/gateway.log | tail -30
```

Success looks like:

```text
Connecting to weixin...
[Weixin] Connected account=<prefix> base=https://ilinkai.weixin.qq.com
✓ weixin connected
Gateway running with 1 platform(s)
```

## Pitfalls

- QR login connects an iLink bot identity, often `...@im.bot`; DMs usually work, ordinary WeChat group delivery often does not.
- Default to `WEIXIN_GROUP_POLICY=disabled` unless the user explicitly wants group experiments.
- Prefer `WEIXIN_DM_POLICY=allowlist` with `WEIXIN_ALLOWED_USERS=<scanner user_id>` after the QR flow, unless the user explicitly asks for open access.
- During gateway restart, iLink may rate-limit the shutdown notification send; if the subsequent startup log says `✓ weixin connected`, the connection itself is fine.
