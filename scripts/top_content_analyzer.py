#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import OUTPUTS, ensure_dirs
parser = argparse.ArgumentParser()
parser.add_argument("--input", default=str(OUTPUTS / "reports" / "matomo_content_report.md"))
args = parser.parse_args()
ensure_dirs()
source = Path(args.input)
out = OUTPUTS / "reports" / "top_content_analyzer.md"
out.write_text(f"# Top Content Analyzer\n\nSource reviewed: {source}\n\nUse this report to choose repeat topics, not commerce actions.\n", encoding="utf-8")
print(f"Created {out}")
