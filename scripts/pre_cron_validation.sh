#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/replife-backend"
MODE="${1:-basic}"

cd "$BASE"

echo "=== RepLife pre-cron validation ==="
date
echo "Mode: $MODE"
echo

echo "=== Protected apps ==="
bash scripts/check_protected_apps.sh
echo

echo "=== Placeholder checks ==="
bash scripts/check_active_placeholders.sh runtime-basic
bash scripts/check_active_placeholders.sh cron

case "$MODE" in
  basic)
    echo "Mode basic: skipping optional AI, Postiz API, and backup placeholder checks."
    ;;
  backup)
    bash scripts/check_active_placeholders.sh backup
    ;;
  ai)
    bash scripts/check_active_placeholders.sh ai
    ;;
  postiz-api)
    bash scripts/check_active_placeholders.sh postiz-api
    ;;
  all)
    bash scripts/check_active_placeholders.sh ai
    bash scripts/check_active_placeholders.sh postiz-api
    bash scripts/check_active_placeholders.sh backup
    ;;
  *)
    echo "Usage: pre_cron_validation.sh [basic|backup|ai|postiz-api|all]" >&2
    exit 2
    ;;
esac
echo

echo "=== Git private-file tracking check ==="
if git ls-files | grep -Ei '(^|/)\.env$|\.sqlite|\.sqlite-wal|\.sqlite-shm|(^|/)secrets/|(^|/)backups/|(^|/)logs/|(^|/)outputs/|(^|/)audit/|(^|/)media-inbox/|(^|/)media-archive/|(^|/)inputs/media/|\.xlsx$|\.bak$'; then
  echo "STOP: private or generated files are tracked by Git." >&2
  exit 1
fi
echo "OK: no private/generated files are tracked by Git."
echo

echo "=== Python syntax checks, if Python scripts exist ==="
if find scripts -maxdepth 1 -name '*.py' -print -quit | grep -q .; then
  python3 -m compileall -q scripts
  echo "OK: Python scripts compile."
else
  echo "No Python scripts found yet. Skipping compile check."
fi
echo

echo "=== Shell syntax checks ==="
while IFS= read -r script; do
  bash -n "$script"
done < <(find scripts -maxdepth 1 -name '*.sh' -print)
echo "OK: shell scripts pass bash -n."
echo

echo "=== Cron policy reminder ==="
echo "Do not add optional Postiz loader sends, media uploads, commerce, customer-service, DMs, or comment auto-replies to cron."
echo
echo "Pre-cron validation passed."
