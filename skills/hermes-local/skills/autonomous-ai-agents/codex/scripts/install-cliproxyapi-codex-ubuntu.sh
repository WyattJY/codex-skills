#!/usr/bin/env bash
set -euo pipefail

VERSION="${VERSION:-7.0.7}"
APP_USER="${APP_USER:-cliproxyapi}"
APP_DIR="${APP_DIR:-/opt/cliproxyapi}"
CONFIG_DIR="${CONFIG_DIR:-/etc/cliproxyapi}"
CONFIG_FILE="${CONFIG_FILE:-${CONFIG_DIR}/config.yaml}"
AUTH_DIR="${AUTH_DIR:-/var/lib/cliproxyapi/auths}"
SERVICE_FILE="${SERVICE_FILE:-/etc/systemd/system/cliproxyapi.service}"
CONFIG_SOURCE="${CONFIG_SOURCE:-/tmp/cliproxyapi-config.yaml}"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Please run as root: sudo bash $0"
  exit 1
fi

case "$(uname -m)" in
  x86_64|amd64) ASSET="CLIProxyAPI_${VERSION}_linux_amd64.tar.gz" ;;
  aarch64|arm64) ASSET="CLIProxyAPI_${VERSION}_linux_aarch64.tar.gz" ;;
  *) echo "Unsupported architecture: $(uname -m)"; exit 1 ;;
esac

URL="https://github.com/router-for-me/CLIProxyAPI/releases/download/v${VERSION}/${ASSET}"

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y curl ca-certificates tar

id -u "${APP_USER}" >/dev/null 2>&1 || useradd --system --home "/var/lib/${APP_USER}" --create-home --shell /usr/sbin/nologin "${APP_USER}"
install -d -o root -g root -m 0755 "${APP_DIR}" "${CONFIG_DIR}"
install -d -o "${APP_USER}" -g "${APP_USER}" -m 0750 "${AUTH_DIR}"
install -d -o "${APP_USER}" -g "${APP_USER}" -m 0750 "/var/lib/${APP_USER}"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT
cd "${TMP_DIR}"

curl -fL -o cliproxyapi.tar.gz "${URL}"
tar -xzf cliproxyapi.tar.gz
install -o root -g root -m 0755 cli-proxy-api "${APP_DIR}/cli-proxy-api"

if [[ ! -f "${CONFIG_SOURCE}" ]]; then
  echo "Missing config source: ${CONFIG_SOURCE}"
  echo "Copy a config to that path or set CONFIG_SOURCE=/path/to/config.yaml"
  exit 1
fi
install -o root -g "${APP_USER}" -m 0640 "${CONFIG_SOURCE}" "${CONFIG_FILE}"

cat > "${SERVICE_FILE}" <<EOF
[Unit]
Description=CLIProxyAPI Codex proxy
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${APP_DIR}
Environment=HOME=/var/lib/${APP_USER}
ExecStart=${APP_DIR}/cli-proxy-api --config ${CONFIG_FILE}
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ReadWritePaths=/var/lib/${APP_USER} ${AUTH_DIR} ${APP_DIR}

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cliproxyapi
systemctl restart cliproxyapi
systemctl --no-pager --full status cliproxyapi || true

cat <<EOF
Installed CLIProxyAPI.

Next: keep an SSH tunnel open from the local machine:
  ssh -L 1455:127.0.0.1:1455 <user>@<server>

Then run on the server:
  sudo -u ${APP_USER} HOME=/var/lib/${APP_USER} ${APP_DIR}/cli-proxy-api --config ${CONFIG_FILE} --codex-login --no-browser

Open the printed authorization URL in your local browser.
EOF
