#!/usr/bin/env bash
set -euo pipefail
cd "$HOME/replife-backend"
echo "=== Git status ==="
git status --short
STAGED_FILES="$(git diff --cached --name-only || true)"
if [ -z "$STAGED_FILES" ]; then
echo "No staged files. Use git add with specific safe folders/files
first."
exit 1
fi
BLOCKED_PATTERN='(^|/)
(\.env|\.env\..*|.*\.env|.*\.env\..*|rclone\.conf|credentials\.json|token\
.json|postiz\.env|n8n\.env|matomo\.env)$|(^|/)secrets/|(^|/)logs/|
(^|/)backups/|(^|/)outputs/|(^|/)audit/|(^|/)media-inbox/|(^|/)mediaarchive/|(^|/)
inputs/media/|\.
(secret|secrets|bak|mp4|mov|mkv|wav|mp3|flac|png|jpg|jpeg|webp|tar|gz|zip|
db|sqlite|sqlite3)$'
BAD_FILES="$(printf '%s\n' "$STAGED_FILES" | grep -E "$BLOCKED_PATTERN" ||
true)"
if [ -n "$BAD_FILES" ]; then
echo "STOP: blocked private/generated files are staged:"
printf '%s\n' "$BAD_FILES"
echo "Run: git reset HEAD FILE_PATH"
exit 1
fi
git diff --cached --check
echo "Preflight passed. Review staged diff before committing:"
echo "git diff --cached --stat"