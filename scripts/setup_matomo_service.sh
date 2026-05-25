#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/replife-backend"
SERVICE_DIR="$BASE/services/matomo"

echo "RepLife Matomo setup"
echo "This script uses the docker-compose.yml already included in the zip."
echo "You do not need to copy and paste the Matomo Docker Compose code."

cd "$SERVICE_DIR"

if sudo ss -tulpn | grep -q ':8081 '; then
  echo "STOP: port 8081 is already in use. Do not continue until this is reviewed."
  sudo ss -tulpn | grep ':8081 ' || true
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  chmod 600 .env
  MATOMO_PASSWORD="$(openssl rand -hex 24)"
  MATOMO_ROOT_PASSWORD="$(openssl rand -hex 24)"
  sed -i "s/^MATOMO_DB_PASSWORD=.*/MATOMO_DB_PASSWORD=${MATOMO_PASSWORD}/" .env
  sed -i "s/^MATOMO_DB_ROOT_PASSWORD=.*/MATOMO_DB_ROOT_PASSWORD=${MATOMO_ROOT_PASSWORD}/" .env
  echo "Created services/matomo/.env from .env.example and generated database passwords."
else
  echo "services/matomo/.env already exists. Keeping the existing file."
fi

set -a
. ./.env
set +a

docker manifest inspect "$MATOMO_IMAGE_REF" >/dev/null
docker manifest inspect "$MARIADB_IMAGE_REF" >/dev/null
docker compose config
docker compose pull
docker compose up -d
docker compose ps
curl -I http://127.0.0.1:8081 >/dev/null

echo "Matomo is running locally at http://127.0.0.1:8081."
echo "Next manual step: add the analytics.YOURDOMAIN.com Caddy block, replacing YOURDOMAIN.com with your real domain."
echo "Then open https://analytics.YOURDOMAIN.com and complete the Matomo browser setup."
