#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import OUTPUTS
parser = argparse.ArgumentParser()
parser.add_argument("--packages-only", action="store_true")
args = parser.parse_args()
targets = list((OUTPUTS / "social-packages").glob("*.md"))
failures = []
for path in targets:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if len(text) > 12000:
        failures.append(f"{path}: package is unusually long")
if failures:
    print("\n".join(failures))
    raise SystemExit("STOP: caption/package lint failed.")
print(f"Platform caption linter passed for {len(targets)} package(s).")
