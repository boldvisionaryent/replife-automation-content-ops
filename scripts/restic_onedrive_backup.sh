#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/replife-backend"
cd "$BASE"
[ -f .env ] && set -a && source .env && set +a
: "${RESTIC_ONEDRIVE_REPOSITORY:?Set RESTIC_ONEDRIVE_REPOSITORY in .env}"
: "${RESTIC_PASSWORD_FILE:?Set RESTIC_PASSWORD_FILE in .env}"
restic -r "$RESTIC_ONEDRIVE_REPOSITORY" --password-file "$RESTIC_PASSWORD_FILE" backup "$BASE" --exclude "$BASE/.venv" --exclude "$BASE/logs" --exclude "$BASE/outputs" --exclude "$BASE/inputs/media"
