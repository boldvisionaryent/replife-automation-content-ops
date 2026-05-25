#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/replife-backend"
cd "$BASE"
source .venv/bin/activate
export PYTHONPATH="$BASE"

THEME="${1:-Faith Over Fear}"

python scripts/monthly_theme_validator.py
python scripts/capacity_backlog_report.py
python scripts/validate_content_files.py inputs/media
python scripts/media_spec_validator.py --input inputs/media
python scripts/content_idea_generator.py --dry-run --limit 5
python scripts/content_batch_planner.py --dry-run
python scripts/social_package_builder.py --dry-run --no-ai --theme "$THEME"
python scripts/postiz_queue_builder.py --dry-run --theme "$THEME"
python scripts/platform_caption_linter.py --packages-only
python scripts/postiz_queue_linter.py

echo "Weekly runner stopped before human review, media upload, Postiz loading, or public scheduling."
