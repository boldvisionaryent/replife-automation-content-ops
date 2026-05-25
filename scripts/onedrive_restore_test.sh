#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/replife-backend"
RESTORE_DIR="$BASE/outputs/restore-test/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RESTORE_DIR"
echo "Restore test folder created: $RESTORE_DIR"
echo "Perform a real restic restore or rclone copy test here, then record the result in Microsoft Lists."
