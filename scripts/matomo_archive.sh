#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/replife-backend"
cd "$BASE/services/matomo"
if [ -f "$BASE/.env" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$BASE/.env"
  set +a
fi
MATOMO_URL="${MATOMO_BASE_URL:-https://analytics.YOURDOMAIN.com}"
docker compose exec -T matomo php /var/www/html/console core:archive --url="$MATOMO_URL"
