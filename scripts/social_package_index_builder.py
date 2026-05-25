#!/usr/bin/env python3
from replife_common import OUTPUTS, ensure_dirs, write_csv
ensure_dirs()
rows = [{"package_file": str(p), "business_workstream": "Social Media"} for p in sorted((OUTPUTS / "social-packages").glob("*.md"))]
out = OUTPUTS / "social-packages" / "social_package_index.csv"
write_csv(out, rows, ["package_file", "business_workstream"])
print(f"Created {out}")
