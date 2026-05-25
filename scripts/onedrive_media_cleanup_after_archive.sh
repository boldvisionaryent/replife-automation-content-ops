#!/usr/bin/env bash
set -euo pipefail
if [ "${1:-}" != "--confirm-cleanup" ]; then
  echo "DRY RUN: would clean old archived media. Rerun with --confirm-cleanup only after archive verification."
  exit 0
fi
find "$HOME/replife-backend/outputs/archives" -type f -mtime +45 -print
echo "Cleanup placeholder complete. Delete manually only after review."
