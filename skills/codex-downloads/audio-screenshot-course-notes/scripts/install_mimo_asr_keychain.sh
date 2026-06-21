#!/usr/bin/env bash
set -euo pipefail

SERVICE="${MIMO_ASR_KEYCHAIN_SERVICE:-wyatt-mimo-asr-api-key}"
ACCOUNT="${MIMO_ASR_KEYCHAIN_ACCOUNT:-${USER:-jiangyu}}"

if ! command -v security >/dev/null 2>&1; then
  echo "macOS security command not found." >&2
  exit 2
fi

printf "Paste MiMo ASR API key for Keychain service '%s' account '%s': " "$SERVICE" "$ACCOUNT" >&2
stty -echo
IFS= read -r API_KEY
stty echo
printf "\n" >&2

if [ -z "$API_KEY" ]; then
  echo "Empty key; nothing written." >&2
  exit 2
fi

security add-generic-password -U -s "$SERVICE" -a "$ACCOUNT" -w "$API_KEY" >/dev/null
unset API_KEY

echo "Stored MiMo ASR API key in macOS Keychain service '$SERVICE' for account '$ACCOUNT'."
