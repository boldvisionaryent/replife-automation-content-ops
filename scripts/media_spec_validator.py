#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import OUTPUTS, ensure_dirs, write_csv

parser = argparse.ArgumentParser(description="Validate media file extensions and basic size readiness.")
parser.add_argument("--input", default="inputs/media")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
target = Path(args.input)
if not target.is_absolute():
    target = Path.cwd() / target
allowed = {".mp4", ".mov", ".mkv", ".wav", ".mp3", ".flac", ".png", ".jpg", ".jpeg", ".webp"}
rows = []
for path in sorted(target.rglob("*")) if target.exists() else []:
    if path.is_file():
        ext_ok = path.suffix.lower() in allowed
        size = path.stat().st_size
        size_ok = size > 0
        rows.append({"file": str(path), "extension_ok": ext_ok, "size_bytes": size, "size_ok": size_ok, "passed": "yes" if ext_ok and size_ok else "no"})
report = OUTPUTS / "reports" / "media_spec_report.csv"
write_csv(report, rows, ["file", "extension_ok", "size_bytes", "size_ok", "passed"])
failed = [r for r in rows if r["passed"] != "yes"]
print(f"Media spec report: {report}")
if failed:
    raise SystemExit(f"STOP: {len(failed)} media file(s) failed validation.")
print(f"Media spec validation passed for {len(rows)} file(s).")
