#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS, ensure_dirs, slugify
parser = argparse.ArgumentParser()
parser.add_argument("--song", default="Sample Song")
parser.add_argument("--theme", default="Faith Over Fear")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
out = OUTPUTS / "reports" / f"shakeum-{slugify(args.song)}-hero-pack.md"
text = f"# SHAKEUM Hero Song Pack\n\nbusiness_workstream: SHAKEUM\n\nSong: {args.song}\nTheme: {args.theme}\n\n## Draft Angles\n- Lyric-drop concept\n- Short-form hook\n- Playlist pitch draft\n"
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    out.write_text(text, encoding="utf-8")
    print(f"Created {out}")
