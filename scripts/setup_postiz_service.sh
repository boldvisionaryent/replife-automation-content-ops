#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/replife-backend"
SERVICE_DIR="$BASE/services/postiz"
POSTIZ_DIR="$SERVICE_DIR/postiz-docker-compose"

echo "RepLife Postiz setup"
echo "This script clones the official Postiz Docker Compose repository, then patches local-only ports."
echo "You do not need to copy and paste a Postiz docker-compose.yml from this manual."

if sudo ss -tulpn | grep -q ':4007 '; then
  echo "STOP: port 4007 is already in use. Do not continue until this is reviewed."
  sudo ss -tulpn | grep ':4007 ' || true
  exit 1
fi
if sudo ss -tulpn | grep -q ':4080 '; then
  echo "STOP: port 4080 is already in use. Do not continue until this is reviewed."
  sudo ss -tulpn | grep ':4080 ' || true
  exit 1
fi

cd "$SERVICE_DIR"
if [ ! -d "$POSTIZ_DIR" ]; then
  git clone https://github.com/gitroomhq/postiz-docker-compose "$POSTIZ_DIR"
else
  echo "Postiz compose folder already exists. Keeping it and applying the RepLife patch again."
fi

cd "$POSTIZ_DIR"

if [ -f "$BASE/.env" ]; then
  set -a
  . "$BASE/.env"
  set +a
fi

python3 "$BASE/scripts/patch_postiz_compose_ports.py" docker-compose.yml

docker compose config
docker compose pull
docker compose up -d
docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}' | grep -E 'postiz|temporal' || true

if docker ps --format '{{.Ports}}' | grep -E '0\.0\.0\.0:4007|0\.0\.0\.0:4080|0\.0\.0\.0:8080|:::4007|:::4080|:::8080' >/dev/null; then
  echo "STOP: Postiz appears to expose an unsafe public port. Review docker-compose.yml before continuing."
  exit 1
fi

echo "Postiz containers are started with RepLife local-only port settings."
echo "Next manual step: add the social.YOURDOMAIN.com Caddy block."
echo "Then open https://social.YOURDOMAIN.com, create the owner account, and disable open registration."
