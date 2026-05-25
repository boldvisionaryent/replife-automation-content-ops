#!/usr/bin/env python3
import argparse
from replife_common import INPUTS, OUTPUTS, ensure_dirs, read_csv, write_csv
parser = argparse.ArgumentParser()
parser.add_argument("--file", default=str(INPUTS / "social" / "manual_social_metrics.csv"))
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
rows = read_csv(__import__("pathlib").Path(args.file))
if not rows:
    raise SystemExit("STOP: manual social metrics CSV is missing or empty.")
out = OUTPUTS / "reports" / "manual_social_metrics_import_report.csv"
if args.dry_run:
    print(f"DRY RUN: would import {len(rows)} metric row(s).")
else:
    write_csv(out, rows)
    print(f"Created {out}")
