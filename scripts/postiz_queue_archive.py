#!/usr/bin/env python3
import argparse, shutil
from replife_common import OUTPUTS, ensure_dirs, today_stamp
parser = argparse.ArgumentParser()
parser.add_argument("--confirm-archive", action="store_true")
parser.add_argument("--allow-unsent", action="store_true")
args = parser.parse_args()
ensure_dirs()
queue = OUTPUTS / "social-queues" / "approved_postiz_queue.csv"
archive = OUTPUTS / "archives" / f"approved_postiz_queue_{today_stamp()}.csv"
if not queue.exists():
    print("No approved_postiz_queue.csv exists. Nothing to archive.")
elif not args.confirm_archive:
    print(f"DRY RUN: would archive {queue} to {archive}. Add --confirm-archive to proceed.")
else:
    archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(queue, archive)
    print(f"Archived queue to {archive}")
