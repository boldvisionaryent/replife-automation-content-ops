#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS, ensure_dirs, write_csv
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
rows = [{"business_workstream": "Product Prompting", "prompt_idea": "Internal creative concept tied to RepLife/SHAKEUM theme", "public_social_allowed": "no", "explicit_platforms": ""}]
out = OUTPUTS / "reports" / "product_prompt_drafts.csv"
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    write_csv(out, rows)
    print(f"Created {out}")
