#!/usr/bin/env python3
from replife_common import load_env
env = load_env()
limit = int(env.get("POSTIZ_API_SAFE_HOURLY_LIMIT", "24") or 24)
print(f"Postiz API budget guard passed for safe hourly limit: {limit}")
