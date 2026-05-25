#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import INPUTS, OUTPUTS, ensure_dirs, write_csv
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
rows = [{"asset_file": str(p), "business_workstream": "Social Media", "status": "manifested"} for p in sorted((INPUTS / "media").rglob("*")) if p.is_file()]
out = OUTPUTS / "social-packages" / "content_asset_manifest.csv"
if args.dry_run:
    print(f"DRY RUN: would create manifest with {len(rows)} row(s).")
else:
    write_csv(out, rows, ["asset_file", "business_workstream", "status"])
    print(f"Created {out}")
