#!/usr/bin/env bash
# Install matplotlib + pillow for the thesis-technical-route-renderer skill.
# Prefers `uv` (fast, isolated); falls back to `pip` in the current Python.
#
# Usage: bash install_deps.sh

set -euo pipefail

if command -v uv >/dev/null 2>&1; then
  echo "[install_deps] uv detected — creating ./.venv with matplotlib + pillow"
  uv venv .venv >/dev/null
  # shellcheck disable=SC1091
  source .venv/bin/activate
  uv pip install --quiet matplotlib pillow
  echo "[install_deps] done. activate with: source .venv/bin/activate"
  exit 0
fi

if command -v python3 >/dev/null 2>&1; then
  echo "[install_deps] uv not found — using pip in the current python3"
  python3 -m pip install --user --quiet matplotlib pillow
  echo "[install_deps] done (user-site install)"
  exit 0
fi

echo "error: need either uv or python3 on PATH" >&2
exit 1
