#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from replife_common import OUTPUTS, ensure_dirs, write_csv

parser = argparse.ArgumentParser(description="Validate media/content filenames before processing.")
parser.add_argument("path", nargs="?", default="inputs/media")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
target = Path(args.path)
if not target.is_absolute():
    target = Path.cwd() / target
pattern = re.compile(r"^[a-z0-9][a-z0-9._-]*\.(mp4|mov|mkv|wav|mp3|flac|png|jpg|jpeg|webp|txt|md|csv)$")
rows = []
for path in sorted(target.rglob("*")) if target.exists() else []:
    if path.is_file():
        ok = bool(pattern.match(path.name.lower()))
        rows.append({"file": str(path), "filename": path.name, "passed": "yes" if ok else "no", "message": "" if ok else "Use lowercase letters, numbers, hyphen, underscore, dot, and approved extension."})
report = OUTPUTS / "reports" / "content_file_validation_report.csv"
write_csv(report, rows, ["file", "filename", "passed", "message"])
failed = [r for r in rows if r["passed"] != "yes"]
print(f"Filename validation report: {report}")
if failed:
    raise SystemExit(f"STOP: {len(failed)} filename(s) failed validation.")
print(f"Filename validation passed for {len(rows)} file(s).")
