#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS, ensure_dirs, write_csv
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
rows = [{"week": "Week 1", "business_workstream": "RepLife Show", "planned_action": "Build one approved social package", "status": "planned"}]
out = OUTPUTS / "reports" / "content_batch_plan.csv"
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    write_csv(out, rows)
    print(f"Created {out}")
