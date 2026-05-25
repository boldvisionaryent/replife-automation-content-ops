#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/replife-backend"
cd "$BASE"

if [ -d .venv ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
export PYTHONPATH="$BASE"

TEST_DIR="$BASE/outputs/test-results/day17m"
mkdir -p "$TEST_DIR"

bash scripts/validate_all_scripts_preview.sh
python3 -m compileall -q scripts
bash -n scripts/*.sh
python scripts/media_spec_validator.py --input inputs/end-to-end-dry-run/media
python scripts/social_package_builder.py \
  --no-ai \
  --input inputs/end-to-end-dry-run/social/social_package_requests.csv \
  --output "$TEST_DIR/day17m_social_package.md"
python scripts/postiz_queue_builder.py \
  --theme "Day 17M Sample" \
  --output "$TEST_DIR/day17m_approved_postiz_queue.csv"
python scripts/postiz_queue_linter.py --input "$TEST_DIR/day17m_approved_postiz_queue.csv"

echo "Day 17M strict dry run passed. Review outputs/test-results/day17m and record the result in Microsoft Lists."
echo "No publish, schedule, send, reply, upload, or commerce action was performed."
