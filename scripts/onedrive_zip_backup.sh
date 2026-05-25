#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/replife-backend"
cd "$BASE"
[ -f .env ] && set -a && source .env && set +a
mkdir -p backups
ARCHIVE="backups/replife-source-$(date +%Y%m%d-%H%M%S).tar.gz"
tar --exclude='./.venv' --exclude='./logs' --exclude='./outputs' --exclude='./inputs/media' --exclude='./backups' -czf "$ARCHIVE" .
if [ -n "${RCLONE_ONEDRIVE_REMOTE:-}" ] && [ -n "${ONEDRIVE_ROOT_FOLDER:-}" ]; then
  rclone copy "$ARCHIVE" "${RCLONE_ONEDRIVE_REMOTE}:${ONEDRIVE_ROOT_FOLDER}/zipbackups"
fi
echo "Created $ARCHIVE"
