#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import OUTPUTS, ensure_dirs, slugify
parser = argparse.ArgumentParser()
parser.add_argument("transcript")
parser.add_argument("--title", default="RepLife Website Draft")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
source = Path(args.transcript)
text = source.read_text(encoding="utf-8", errors="ignore") if source.exists() else ""
out = OUTPUTS / "website-drafts" / f"{slugify(args.title)}.md"
body = f"# {args.title}\n\nbusiness_workstream: Website Drafts\n\nSource: {source}\n\n{text[:1500]}\n\nManual step: copy, edit, review, and publish in WordPress manually.\n"
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    out.write_text(body, encoding="utf-8")
    print(f"Created {out}")
