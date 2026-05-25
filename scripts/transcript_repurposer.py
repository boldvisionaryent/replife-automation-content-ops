#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import OUTPUTS, ensure_dirs, slugify
parser = argparse.ArgumentParser(description="Repurpose transcripts into draft notes, clips, and captions.")
parser.add_argument("transcript", nargs="?")
parser.add_argument("--limit", type=int, default=3)
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
files = [Path(args.transcript)] if args.transcript else sorted((OUTPUTS / "transcripts").glob("*.txt"))[: args.limit]
if args.dry_run:
    print(f"DRY RUN: would repurpose {len(files)} transcript(s).")
else:
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        out = OUTPUTS / "reports" / f"{slugify(path.stem)}-repurposed.md"
        out.write_text(f"# Repurposed Transcript\n\nbusiness_workstream: RepLife Show\n\nSource: {path}\n\n## Clip Ideas\n- Review transcript and add clip ideas.\n\n## Draft Caption\n{text[:400]}\n", encoding="utf-8")
        print(f"Created {out}")
