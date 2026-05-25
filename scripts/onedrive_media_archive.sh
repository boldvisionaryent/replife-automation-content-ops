#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/replife-backend"
cd "$BASE"
[ -f .env ] && set -a && source .env && set +a
: "${RCLONE_ONEDRIVE_REMOTE:?Set RCLONE_ONEDRIVE_REMOTE in .env}"
: "${ONEDRIVE_ROOT_FOLDER:?Set ONEDRIVE_ROOT_FOLDER in .env}"
mkdir -p outputs/archives
rclone copy outputs "${RCLONE_ONEDRIVE_REMOTE}:${ONEDRIVE_ROOT_FOLDER}/outputs" --exclude "*.tmp"
echo "OneDrive archive copy complete."
