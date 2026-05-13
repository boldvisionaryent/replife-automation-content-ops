#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/replife-backend"
MODE="${1:-runtime-basic}"

usage() {
  echo "Usage: check_active_placeholders.sh [runtime-basic|cron|ai|postiz-api|backup|scripts|strict]" >&2
}

case "$MODE" in
  runtime-basic)
    TARGETS=("$BASE/services")
    PATTERN='YOURDOMAIN\.com|YOUR_USER|YOUR_VPS_IP|replace_with_|REPLACE_WITH|REPLACE_WITH_VERIFIED|PASTE_BETTER_STACK'
    MESSAGE="required service placeholders"
    ;;

  cron)
    TARGETS=("$BASE/.env")
    PATTERN='BETTERSTACK_[A-Z0-9_]*=(replace_me|replace_me_optional|PASTE_BETTER_STACK|)$'
    MESSAGE="cron heartbeat placeholders"
    ;;

  ai)
    TARGETS=("$BASE/.env")
    PATTERN='GITHUB_TOKEN=(replace_me|)$|GITHUB_MODELS_MODEL=REPLACE_WITH|AI_[A-Z0-9_]*=(replace_me|REPLACE_WITH)'
    MESSAGE="AI provider placeholders"
    ;;

  postiz-api)
    TARGETS=("$BASE/.env")
    PATTERN='POSTIZ_BASE_URL=.*YOURDOMAIN|POSTIZ_API_KEY=(replace_me|replace_me_optional|)$|POSTIZ_API_BASE_PATH=(replace_me|REPLACE_WITH|)$|POSTIZ_ALLOWED_PLATFORMS=(replace_me|)$'
    MESSAGE="Postiz API placeholders"
    ;;

  backup)
    TARGETS=("$BASE/.env" "$BASE/secrets")
    PATTERN='RCLONE_ONEDRIVE_REMOTE=(replace_me|)$|ONEDRIVE_ROOT_FOLDER=(replace_me|)$|RESTIC_ONEDRIVE_REPOSITORY=(replace_me|REPLACE_WITH|)$|RESTIC_PASSWORD_FILE=.*/YOUR_USER/|replace_with_|REPLACE_WITH'
    MESSAGE="backup/archive placeholders"
    ;;

  scripts)
    TARGETS=("$BASE/scripts")
    # Scripts may intentionally contain safe beginner sample placeholders such as
    # PASTE_LINK, PASTE_FINAL_LINK, PASTE_SUBREDDIT, MONTHLY_THEME, YYYYMM-DD,
    # REVIEW_CAPTION_FROM_SOCIAL_PACKAGE, and PASTE_REAL_POSTIZ_INTEGRATION_ID.
    # Do not fail scripts mode on those sample values.
    PATTERN='PASTE_BETTER_STACK'
    MESSAGE="unsafe script runtime placeholders"
    ;;

  strict)
    TARGETS=("$BASE/.env" "$BASE/services")
    # Strict final acceptance checks active runtime configuration.
    # It intentionally ignores sample placeholders inside docs, templates, and Python examples.
    PATTERN='YOURDOMAIN\.com|YOUR_USER|YOUR_VPS_IP|YOUR_GITHUB_EMAIL|YOUR_GITHUB_USERNAME|replace_me|replace_me_optional|replace_with_|REPLACE_WITH|PASTE_BETTER_STACK|REPLACE_WITH_VERIFIED'
    MESSAGE="any active runtime placeholders"
    ;;

  *)
    usage
    exit 2
    ;;
esac

SKIP_PATH_PATTERN='\.env\.example|README|docs/|templates/|\.md$'
FOUND=0

for target in "${TARGETS[@]}"; do
  [ -e "$target" ] || continue

  while IFS= read -r line; do
    file_path="${line%%:*}"
    rest="${line#*:}"
    line_number="${rest%%:*}"
    matched_text="${rest#*:}"

    if echo "$file_path" | grep -Eq "$SKIP_PATH_PATTERN"; then
      continue
    fi

    trimmed="$(printf '%s' "$matched_text" | sed 's/^[[:space:]]*//')"

    if printf '%s' "$trimmed" | grep -Eq '^#'; then
      continue
    fi

    echo "$file_path:$line_number:$matched_text"
    FOUND=1
  done < <(grep -RInE "$PATTERN" "$target" 2>/dev/null || true)
done

if [ "$FOUND" -eq 1 ]; then
  echo
  echo "STOP: $MESSAGE were found for mode '$MODE'." >&2
  echo "Fix the file(s) above, then rerun this exact mode before continuing." >&2
  exit 1
fi

echo "Active placeholder check passed for mode: $MODE"