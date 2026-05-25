#!/usr/bin/env python3
from replife_common import load_env
env = load_env()
base = env.get("POSTIZ_BASE_URL", "")
path = env.get("POSTIZ_API_BASE_PATH", "")
if not base or "YOURDOMAIN" in base:
    raise SystemExit("STOP: POSTIZ_BASE_URL is not configured.")
if not path:
    raise SystemExit("STOP: POSTIZ_API_BASE_PATH is not configured.")
print(f"Postiz API smoke-test configuration ready: {base}{path}")
print("Run a live API check manually before integrations, uploads, or optional loading.")
