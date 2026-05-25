#!/usr/bin/env python3
import argparse
from datetime import date, timedelta
from replife_common import OUTPUTS, ensure_dirs, write_csv
parser = argparse.ArgumentParser()
parser.add_argument("--start", default=str(date.today()))
parser.add_argument("--theme", default="Faith Over Fear")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
start = date.fromisoformat(args.start)
rows = [{"scheduled_date": str(start + timedelta(days=i)), "theme": args.theme, "platform": p, "business_workstream": "Social Media"} for i, p in enumerate(["facebook", "instagram", "youtube", "tiktok"])]
out = OUTPUTS / "social-queues" / "postiz_schedule_manifest.csv"
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    write_csv(out, rows)
    print(f"Created {out}")
