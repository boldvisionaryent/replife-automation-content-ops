#!/usr/bin/env python3
import argparse
from replife_common import OUTPUTS
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
queue = OUTPUTS / "social-queues" / "approved_postiz_queue.csv"
if args.dry_run:
    print(f"DRY RUN: would map reviewed captions into {queue}")
else:
    print(f"Manual helper placeholder: review packages and update {queue} captions intentionally.")
