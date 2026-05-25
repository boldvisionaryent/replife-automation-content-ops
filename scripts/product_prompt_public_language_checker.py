#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import find_commerce_terms
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()
path = Path(args.input)
text = path.read_text(encoding="utf-8", errors="ignore")
hits = find_commerce_terms(text)
if hits:
    raise SystemExit("STOP: public-language checker found blocked terms: " + ", ".join(hits))
print(f"Public-language check passed: {path}")
