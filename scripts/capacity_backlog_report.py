#!/usr/bin/env python3
import shutil
from replife_common import BASE, OUTPUTS, ensure_dirs
ensure_dirs()
usage = shutil.disk_usage(BASE)
out = OUTPUTS / "reports" / "capacity_backlog_report.md"
out.write_text(f"# Capacity and Backlog Report\n\nDisk total: {usage.total}\nDisk used: {usage.used}\nDisk free: {usage.free}\n\nReview old queues, transcripts, media, and outputs before adding new work.\n", encoding="utf-8")
print(f"Created {out}")
