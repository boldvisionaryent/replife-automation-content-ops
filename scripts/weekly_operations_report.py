#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS, ensure_dirs, today_stamp
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
out = OUTPUTS / "reports" / f"weekly_operations_report_{today_stamp()}.md"
content = "# Weekly Operations Report\n\n- Review monitors.\n- Review failed jobs.\n- Review content queue.\n- Review backups.\n"
if args.dry_run:
    print(f"DRY RUN: would create {out}")
else:
    out.write_text(content, encoding="utf-8")
    print(f"Created {out}")
