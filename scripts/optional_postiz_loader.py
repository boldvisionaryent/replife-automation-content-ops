#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from replife_common import OUTPUTS, load_env, read_csv
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--payload-preview-output", default=str(OUTPUTS / "social-queues" / "previews" / "postiz-payload-preview.json"))
parser.add_argument("--confirm-send", action="store_true")
parser.add_argument("--limit", type=int, default=3)
parser.add_argument("--resend", action="store_true")
args = parser.parse_args()
env = load_env()
queue = OUTPUTS / "social-queues" / "approved_postiz_queue.csv"
rows = [r for r in read_csv(queue) if r.get("approved") == "yes"][: args.limit]
payload = {"mode": "preview", "rows": rows}
preview = Path(args.payload_preview_output)
preview.parent.mkdir(parents=True, exist_ok=True)
preview.write_text(json.dumps(payload, indent=2), encoding="utf-8")
if args.dry_run or not args.confirm_send:
    print(f"DRY RUN: wrote payload preview to {preview}")
elif env.get("POSTIZ_API_ENABLED") != "yes":
    raise SystemExit("STOP: POSTIZ_API_ENABLED must be yes for supervised sending.")
else:
    print("Send placeholder passed safety gate. Keep manual Postiz scheduling as fallback.")
    print("Set POSTIZ_API_ENABLED=no immediately after any supervised session.")
