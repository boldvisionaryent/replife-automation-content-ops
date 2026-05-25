#!/usr/bin/env python3
import argparse
from replife_common import load_env
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--confirm-upload", action="store_true")
args = parser.parse_args()
env = load_env()
if args.dry_run or not args.confirm_upload:
    print("DRY RUN: would upload only upload_ready=yes rows with local files.")
elif env.get("POSTIZ_API_ENABLED") != "yes":
    raise SystemExit("STOP: POSTIZ_API_ENABLED must be yes for a supervised upload session.")
else:
    print("Upload placeholder passed safety gate. Implement live upload only after API route is smoke-tested.")
