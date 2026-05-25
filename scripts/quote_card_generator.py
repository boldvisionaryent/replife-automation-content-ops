#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS, ensure_dirs, slugify
parser = argparse.ArgumentParser()
parser.add_argument("--title", default="RepLife Quote")
parser.add_argument("--text", default="Keep building with faith and discipline.")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
out = OUTPUTS / "visuals" / f"{slugify(args.title)}.svg"
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080"><rect width="100%" height="100%" fill="#0B2545"/><text x="80" y="180" fill="white" font-size="56">{args.title}</text><text x="80" y="320" fill="white" font-size="38">{args.text}</text></svg>'
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    out.write_text(svg, encoding="utf-8")
    print(f"Created {out}")
