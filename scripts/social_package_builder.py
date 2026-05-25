#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from replife_common import OUTPUTS, ensure_dirs, slugify

parser = argparse.ArgumentParser(description="Create reviewable platform-specific social package drafts. No public posting occurs.")
parser.add_argument("--from-manifest", action="store_true", help="Reserved for future manifest-driven package generation.")
parser.add_argument("--theme", default="Faith Over Fear")
parser.add_argument("--no-ai", action="store_true", help="Force local template-only drafting.")
parser.add_argument("--input", default="", help="Optional CSV of package requests. Used by Day 17M sample dry run.")
parser.add_argument("--output", default=str(OUTPUTS / "social-packages" / "sample_social_package.md"), help="Output Markdown file path.")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

ensure_dirs()
out = Path(args.output)
if not out.is_absolute():
    out = Path.cwd() / out

rows: list[dict[str, str]] = []
if args.input:
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = Path.cwd() / input_path
    if not input_path.exists():
        raise SystemExit(f"STOP: input CSV not found: {input_path}")
    with input_path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"STOP: input CSV has no rows: {input_path}")
else:
    rows = [{"theme": args.theme, "platform": "facebook", "business_workstream": "Social Media", "caption_prompt": "Draft caption for review."}]

sections = ["# Social Package", "", "business_workstream: Social Media", f"theme: {args.theme}", f"ai_used: {'no' if args.no_ai else 'optional'}", ""]
for idx, row in enumerate(rows, start=1):
    platform = (row.get("platform") or "multi-platform").strip()
    theme = (row.get("theme") or args.theme).strip()
    workstream = (row.get("business_workstream") or "Social Media").strip()
    prompt = (row.get("caption_prompt") or row.get("topic") or "Draft caption for human review.").strip()
    sections.extend([
        f"## Package {idx}: {platform}",
        f"business_workstream: {workstream}",
        f"theme: {theme}",
        "approval_stage: Drafted",
        "public_action: no",
        "caption_draft:",
        f"{prompt}",
        "",
    ])
text = "\n".join(sections)

if args.dry_run:
    print(f"DRY RUN: would create {out} from {len(rows)} request row(s)")
else:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Created {out} from {len(rows)} request row(s)")
