#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS, ensure_dirs, load_env
parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=5)
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
env = load_env()
out = OUTPUTS / "reports" / "matomo_content_report.md"
text = f"# Matomo Content Report\n\nMatomo URL: {env.get('MATOMO_BASE_URL', 'not set')}\n\nAdd API-backed rows after MATOMO_TOKEN is configured.\n"
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    out.write_text(text, encoding="utf-8")
    print(f"Created {out}")
