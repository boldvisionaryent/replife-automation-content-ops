#!/usr/bin/env python3
from replife_common import load_env
env = load_env()
token = env.get("GITHUB_TOKEN", "")
model = env.get("GITHUB_MODELS_MODEL", "")
if not token or token == "replace_me":
    raise SystemExit("STOP: GITHUB_TOKEN is not set.")
if not model or "REPLACE_WITH" in model:
    raise SystemExit("STOP: GITHUB_MODELS_MODEL is not set.")
print(f"GitHub Models configuration looks ready for model: {model}")
print("Manual live API validation should be done before AI-dependent automation.")
