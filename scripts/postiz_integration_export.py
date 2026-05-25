#!/usr/bin/env python3
from replife_common import OUTPUTS, ensure_dirs, write_csv
ensure_dirs()
rows = [{"platform": "facebook", "integration_id": "PASTE_REAL_POSTIZ_INTEGRATION_ID", "verified": "no"}]
out = OUTPUTS / "social-queues" / "postiz_integrations_export.csv"
write_csv(out, rows)
print(f"Created manual integration export worksheet: {out}")
