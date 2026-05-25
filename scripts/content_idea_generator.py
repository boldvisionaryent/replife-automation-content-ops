#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS, ensure_dirs, write_csv
parser = argparse.ArgumentParser(description="Generate safe draft content ideas.")
parser.add_argument("--limit", type=int, default=10)
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
rows = [{"idea_id": i, "business_workstream": "RepLife Show", "theme": "Faith Over Fear", "idea": f"Draft content idea {i}", "status": "Idea"} for i in range(1, args.limit + 1)]
out = OUTPUTS / "reports" / "content_ideas.csv"
if args.dry_run:
    print(f"DRY RUN: would write {len(rows)} ideas to {out}")
else:
    write_csv(out, rows)
    print(f"Created {out}")
