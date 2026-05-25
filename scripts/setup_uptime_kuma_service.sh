#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/replife-backend"
SERVICE_DIR="$BASE/services/uptime-kuma"

echo "RepLife Uptime Kuma setup"
echo "This script uses the docker-compose.yml already included in the zip."
echo "You do not need to copy and paste the Uptime Kuma Docker Compose code."

cd "$SERVICE_DIR"

if sudo ss -tulpn | grep -q ':3001 '; then
  echo "STOP: port 3001 is already in use. Do not continue until this is reviewed."
  sudo ss -tulpn | grep ':3001 ' || true
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  chmod 600 .env
  echo "Created services/uptime-kuma/.env from .env.example."
else
  echo "services/uptime-kuma/.env already exists. Keeping the existing file."
fi

set -a
. ./.env
set +a

docker manifest inspect "$UPTIME_KUMA_IMAGE_REF" >/dev/null
docker compose config
docker compose pull
docker compose up -d
docker compose ps
curl -I http://127.0.0.1:3001 >/dev/null

echo "Uptime Kuma is running locally at http://127.0.0.1:3001."
echo "Next manual step: add the monitor.YOURDOMAIN.com Caddy block with basic_auth."
echo "Then open https://monitor.YOURDOMAIN.com and create the Uptime Kuma owner account."
