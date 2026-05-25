#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path


TARGET = Path(sys.argv[1] if len(sys.argv) > 1 else "docker-compose.yml")
DOMAIN = os.environ.get("DOMAIN", "YOURDOMAIN.com")


def line_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def find_service(lines: list[str], service: str) -> tuple[int, int]:
    marker = f"  {service}:"
    start = next((i for i, line in enumerate(lines) if line.rstrip() == marker), -1)
    if start == -1:
        raise SystemExit(f"Could not find service '{service}' in {TARGET}. Stop and patch manually.")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if line_indent(lines[i]) == 2 and lines[i].strip().endswith(":"):
            end = i
            break
    return start, end


def replace_ports(lines: list[str], service: str, mapping: str) -> list[str]:
    start, end = find_service(lines, service)
    ports_idx = -1
    for i in range(start + 1, end):
        if line_indent(lines[i]) == 4 and lines[i].strip() == "ports:":
            ports_idx = i
            break
    new_block = ["    ports:\n", f'      - "{mapping}"\n']
    if ports_idx == -1:
        return lines[: start + 1] + new_block + lines[start + 1 :]
    after = ports_idx + 1
    while after < end and (not lines[after].strip() or line_indent(lines[after]) > 4):
        after += 1
    return lines[:ports_idx] + new_block + lines[after:]


def upsert_postiz_urls(lines: list[str]) -> list[str]:
    start, end = find_service(lines, "postiz")
    env_idx = -1
    for i in range(start + 1, end):
        if line_indent(lines[i]) == 4 and lines[i].strip() == "environment:":
            env_idx = i
            break
    new_values = [
        f'      MAIN_URL: "https://social.{DOMAIN}"\n',
        f'      FRONTEND_URL: "https://social.{DOMAIN}"\n',
        f'      NEXT_PUBLIC_BACKEND_URL: "https://social.{DOMAIN}/api"\n',
    ]
    if env_idx == -1:
        insert_at = start + 1
        return lines[:insert_at] + ["    environment:\n"] + new_values + lines[insert_at:]

    filtered: list[str] = []
    i = env_idx + 1
    while i < end and (not lines[i].strip() or line_indent(lines[i]) > 4):
        key = lines[i].strip().split(":", 1)[0].strip("- ").strip()
        if key not in {"MAIN_URL", "FRONTEND_URL", "NEXT_PUBLIC_BACKEND_URL"}:
            filtered.append(lines[i])
        i += 1
    return lines[: env_idx + 1] + new_values + filtered + lines[i:]


if not TARGET.exists():
    raise SystemExit(f"{TARGET} was not found.")

original = TARGET.read_text(encoding="utf-8")
backup = TARGET.with_suffix(TARGET.suffix + ".replife-backup")
if not backup.exists():
    backup.write_text(original, encoding="utf-8")

lines = original.splitlines(keepends=True)
lines = replace_ports(lines, "postiz", "127.0.0.1:4007:5000")
lines = replace_ports(lines, "temporal-ui", "127.0.0.1:4080:8080")
lines = upsert_postiz_urls(lines)

TARGET.write_text("".join(lines), encoding="utf-8")
print(f"Patched {TARGET}")
print(f"Backup saved as {backup}")
print("Expected ports after docker compose up: 127.0.0.1:4007->5000 and 127.0.0.1:4080->8080")
