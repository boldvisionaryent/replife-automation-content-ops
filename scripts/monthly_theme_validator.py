#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import BASE, INPUTS, check_workstream, ensure_dirs, read_csv, write_csv

parser = argparse.ArgumentParser(description="Validate the monthly RepLife theme planning CSV.")
parser.add_argument("--file", default=str(INPUTS / "planning" / "monthly_theme.csv"))
parser.add_argument("--init-sample", action="store_true")
args = parser.parse_args()
ensure_dirs()
path = Path(args.file)
if args.init_sample and not path.exists():
    write_csv(path, [{
        "month": "2026-06",
        "theme": "Faith Over Fear",
        "business_workstream": "RepLife Show",
        "campaign": "RepLife weekly platform content",
        "primary_platforms": "facebook,instagram,youtube,tiktok",
        "notes": "Sample row. Replace before production.",
    }])
rows = read_csv(path)
required = {"month", "theme", "business_workstream", "campaign", "primary_platforms"}
if not rows:
    raise SystemExit(f"STOP: no rows found in {path}.")
missing = required - set(rows[0])
if missing:
    raise SystemExit(f"STOP: missing columns in {path}: {sorted(missing)}")
bad = [r for r in rows if not check_workstream(r.get("business_workstream", ""))]
if bad:
    raise SystemExit("STOP: invalid business_workstream value found.")
print(f"Monthly theme validation passed: {path} ({len(rows)} row(s))")
