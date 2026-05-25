#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from replife_common import OUTPUTS, ensure_dirs, write_csv

parser = argparse.ArgumentParser(description="Build reviewable Postiz queue rows. Rows start approved=no unless intentionally changed by a human.")
parser.add_argument("--from-manifest", action="store_true")
parser.add_argument("--theme", default="Faith Over Fear")
parser.add_argument("--start", default="")
parser.add_argument("--output", default=str(OUTPUTS / "social-queues" / "approved_postiz_queue.csv"))
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
rows = [{
    "row_id": "sample-1",
    "business_workstream": "Social Media",
    "platform": "facebook",
    "caption": f"Draft caption for {args.theme}",
    "approved": "no",
    "upload_ready": "no",
    "scheduled_time": args.start,
    "integration_id": "",
    "postiz_sent_at": "",
}]
out = Path(args.output)
if not out.is_absolute():
    out = Path.cwd() / out
if args.dry_run:
    print(f"DRY RUN: would create {out} with {len(rows)} row(s), all approved=no")
else:
    write_csv(out, rows)
    print(f"Created {out}; rows start approved=no")
