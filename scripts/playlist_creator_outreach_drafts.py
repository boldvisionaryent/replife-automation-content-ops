#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS, ensure_dirs
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
out = OUTPUTS / "reports" / "playlist_creator_outreach_drafts.md"
text = "# Playlist / Creator Outreach Drafts\n\nbusiness_workstream: SHAKEUM\n\nDraft only. Send manually after relationship/context review.\n"
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    out.write_text(text, encoding="utf-8")
    print(f"Created {out}")
