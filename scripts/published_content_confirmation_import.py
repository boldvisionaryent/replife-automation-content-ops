#!/usr/bin/env python3
from pathlib import Path
from replife_common import INPUTS, OUTPUTS, ensure_dirs, read_csv, write_csv
ensure_dirs()
source = INPUTS / "social" / "published_content_confirmation.csv"
rows = read_csv(source)
if not rows:
    raise SystemExit(f"STOP: missing or empty {source}")
out = OUTPUTS / "reports" / "published_content_confirmation_report.csv"
write_csv(out, rows)
print(f"Created {out}")
