#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from replife_common import OUTPUTS
parser = argparse.ArgumentParser()
parser.add_argument("--approved-only", action="store_true")
args = parser.parse_args()
preview = OUTPUTS / "social-queues" / "previews" / "postiz-payload-preview.json"
if not preview.exists():
    print(f"REVIEW: {preview} does not exist yet. Run optional_postiz_loader.py --dry-run --payload-preview-output first.")
    raise SystemExit(0)
json.loads(preview.read_text(encoding="utf-8"))
print(f"Postiz wizard payload JSON is parseable: {preview}")
