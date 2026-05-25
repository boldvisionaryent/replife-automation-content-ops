#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from replife_common import OUTPUTS, read_csv

parser = argparse.ArgumentParser(description="Check Postiz queue rows before upload/loading. This does not send anything.")
parser.add_argument("--approved-only", action="store_true")
parser.add_argument("--input", default=str(OUTPUTS / "social-queues" / "approved_postiz_queue.csv"))
args = parser.parse_args()
queue = Path(args.input)
if not queue.is_absolute():
    queue = Path.cwd() / queue
rows = read_csv(queue)
required = {"row_id", "platform", "caption", "approved", "upload_ready"}
if not rows:
    raise SystemExit(f"STOP: no queue rows found at {queue}. Build or select a queue before linting.")
missing = required - set(rows[0])
if missing:
    raise SystemExit(f"STOP: queue missing columns: {sorted(missing)}")
if args.approved_only:
    rows = [r for r in rows if r.get("approved") == "yes"]
allowed_platforms = {"facebook", "instagram", "instagramstandalone", "youtube", "tiktok", "linkedin", "linkedin-page", "x", "reddit", "medium"}
bad: list[str] = []
for idx, row in enumerate(rows, start=1):
    platform = (row.get("platform") or "").strip().lower()
    if platform not in allowed_platforms:
        bad.append(f"row {idx}: unsupported platform '{platform}'")
    if not (row.get("caption") or "").strip():
        bad.append(f"row {idx}: missing caption")
    if row.get("approved") not in {"yes", "no"}:
        bad.append(f"row {idx}: approved must be yes or no")
    if row.get("upload_ready") not in {"yes", "no"}:
        bad.append(f"row {idx}: upload_ready must be yes or no")
if bad:
    raise SystemExit("STOP: queue linter failed:\n" + "\n".join(bad))
print(f"Postiz queue linter passed for {len(rows)} row(s) at {queue}.")
