#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path

BASE = Path.home() / "replife-backend"
if not BASE.exists():
    BASE = Path.cwd()

INPUTS = BASE / "inputs"
OUTPUTS = BASE / "outputs"
LOGS = BASE / "logs"

ALLOWED_WORKSTREAMS = {
    "RepLife Show",
    "SHAKEUM",
    "Product Prompting",
    "Website Drafts",
    "Social Media",
    "Operations",
}

COMMERCE_TERMS = {
    "woocommerce",
    "gelato",
    "stripe",
    "checkout",
    "cart",
    "refund",
    "order",
    "payment",
    "coupon",
    "tax",
    "shipping",
    "fulfillment",
    "customer account",
    "store listing",
}


def ensure_dirs() -> None:
    for path in [
        INPUTS / "planning",
        INPUTS / "social",
        INPUTS / "media",
        INPUTS / "end-to-end-dry-run" / "media",
        INPUTS / "end-to-end-dry-run" / "social",
        OUTPUTS / "reports",
        OUTPUTS / "social-packages",
        OUTPUTS / "social-queues",
        OUTPUTS / "website-drafts",
        OUTPUTS / "transcripts",
        OUTPUTS / "visuals",
        OUTPUTS / "archives",
        LOGS,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def load_env() -> dict[str, str]:
    env = dict(os.environ)
    env_file = BASE / ".env"
    if env_file.exists():
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "item"


def today_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def check_workstream(value: str) -> bool:
    return value in ALLOWED_WORKSTREAMS


def find_commerce_terms(text: str) -> list[str]:
    lower = text.lower()
    return sorted(term for term in COMMERCE_TERMS if term in lower)


def require_no_commerce(text: str) -> None:
    hits = find_commerce_terms(text)
    if hits:
        raise SystemExit("STOP: commerce/customer/store terms found: " + ", ".join(hits))


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without changing production state.")


def print_result(path: Path | None = None, message: str = "Done") -> None:
    if path is not None:
        print(f"{message}: {path}")
    else:
        print(message)
