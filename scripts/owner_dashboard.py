#!/usr/bin/env python3
from replife_common import OUTPUTS, ensure_dirs
ensure_dirs()
out = OUTPUTS / "reports" / "owner_dashboard.md"
out.write_text("# Owner Dashboard\n\n- Check monitors.\n- Check content queue.\n- Check backups.\n- Check monthly theme.\n- Check human approvals.\n", encoding="utf-8")
print(f"Created {out}")
