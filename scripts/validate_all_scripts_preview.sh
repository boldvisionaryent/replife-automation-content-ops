#!/usr/bin/env bash
set -euo pipefail
cd "$HOME/replife-backend"
python3 -m compileall -q scripts
bash -n scripts/*.sh
python3 scripts/monthly_theme_validator.py --init-sample
python3 scripts/content_idea_generator.py --dry-run --limit 3
python3 scripts/social_package_builder.py --dry-run --no-ai
python3 scripts/postiz_queue_builder.py --dry-run
echo "Preview validation passed."
