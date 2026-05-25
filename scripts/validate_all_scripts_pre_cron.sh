#!/usr/bin/env bash
set -euo pipefail
cd "$HOME/replife-backend"
bash scripts/pre_cron_validation.sh basic
python3 -m compileall -q scripts
bash -n scripts/*.sh
echo "Strict pre-cron validation passed."
