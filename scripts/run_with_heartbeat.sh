#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: run_with_heartbeat.sh HEARTBEAT_URL_OR_ENV_VAR command [args...]" >&2
  exit 2
fi

HEARTBEAT="$1"
shift

if [ -f "$HOME/replife-backend/.env" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$HOME/replife-backend/.env"
  set +a
fi

URL="${!HEARTBEAT:-$HEARTBEAT}"
"$@"

if [ -n "$URL" ] && [[ "$URL" == http* ]]; then
  curl -fsS --max-time 10 "$URL" >/dev/null
  echo "Heartbeat sent."
else
  echo "No heartbeat URL configured; command succeeded."
fi
