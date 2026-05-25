#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import INPUTS, check_workstream, ensure_dirs, read_csv, today_stamp, write_csv

parser = argparse.ArgumentParser(description="Register an externally-created asset for RepLife processing.")
parser.add_argument("file")
parser.add_argument("--business-workstream", required=True)
parser.add_argument("--content-type", default="media")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
if not check_workstream(args.business_workstream):
    raise SystemExit("STOP: invalid business workstream.")
source = Path(args.file)
row = {
    "registered_at": today_stamp(),
    "source_file": str(source),
    "filename": source.name,
    "business_workstream": args.business_workstream,
    "content_type": args.content_type,
    "status": "registered",
}
manifest = INPUTS / "media" / "external_asset_intake.csv"
rows = read_csv(manifest)
rows.append(row)
if args.dry_run:
    print(f"DRY RUN: would register {source.name} in {manifest}")
else:
    write_csv(manifest, rows, list(row.keys()))
    print(f"Registered external asset: {manifest}")
