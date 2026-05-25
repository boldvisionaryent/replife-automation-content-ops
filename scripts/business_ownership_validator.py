#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path
from replife_common import ALLOWED_WORKSTREAMS, OUTPUTS

parser = argparse.ArgumentParser(description="Validate business_workstream ownership in generated CSV/Markdown outputs.")
parser.add_argument("target", nargs="?", default=str(OUTPUTS))
args = parser.parse_args()
target = Path(args.target)
if not target.exists():
    print(f"REVIEW: {target} does not exist yet. Nothing to validate.")
    raise SystemExit(0)
failures = []
checked = 0
for path in target.rglob("*"):
    if path.suffix.lower() == ".csv":
        checked += 1
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if "business_workstream" not in (reader.fieldnames or []):
                continue
            for idx, row in enumerate(reader, 2):
                value = row.get("business_workstream", "")
                if value not in ALLOWED_WORKSTREAMS:
                    failures.append(f"{path}:{idx}: invalid business_workstream={value!r}")
    elif path.suffix.lower() in {".md", ".txt"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "business_workstream:" in text:
            checked += 1
            found = any(f"business_workstream: {w}" in text for w in ALLOWED_WORKSTREAMS)
            if not found:
                failures.append(f"{path}: invalid or missing business_workstream value")
if failures:
    print("\n".join(failures))
    raise SystemExit("STOP: business ownership validation failed.")
print(f"Business ownership validation passed. Checked {checked} file(s).")
