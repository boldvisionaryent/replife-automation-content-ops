#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from replife_common import LOGS, OUTPUTS, ensure_dirs
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
log = LOGS / "ai_requests.jsonl"
count = 0
if log.exists():
    count = sum(1 for _ in log.open(encoding="utf-8"))
out = OUTPUTS / "reports" / "ai_usage_report.md"
if args.dry_run:
    print(f"DRY RUN: AI request log has {count} line(s).")
else:
    out.write_text(f"# AI Usage Report\n\nLogged request lines: {count}\n", encoding="utf-8")
    print(f"Created {out}")
