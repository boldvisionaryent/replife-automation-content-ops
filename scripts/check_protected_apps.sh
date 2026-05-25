#!/usr/bin/env bash
set -euo pipefail

failures=0

check_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "STOP: required command not found: $1" >&2
    failures=$((failures + 1))
  fi
}

require_listener() {
  local label="$1"
  local port="$2"
  if sudo ss -tulpn | grep -q ":${port} "; then
    echo "OK: $label has a listener on port $port"
  else
    echo "REVIEW: $label listener was not found on port $port" >&2
    failures=$((failures + 1))
  fi
}

warn_if_public_bind() {
  local label="$1"
  local port="$2"
  if sudo ss -tulpn | grep ":${port} " | grep -Eq '0\.0\.0\.0|:::'; then
    echo "STOP: $label appears to bind publicly on all interfaces for port $port" >&2
    failures=$((failures + 1))
  fi
}

warn_if_in_use_for_new_service() {
  local label="$1"
  local port="$2"
  if sudo ss -tulpn | grep -q ":${port} "; then
    echo "REVIEW: planned RepLife $label port $port is already in use."
  else
    echo "OK: planned RepLife $label port $port is available."
  fi
}

echo "=== RepLife protected-app preflight ==="
date
echo

check_cmd docker
check_cmd sudo
check_cmd ss
check_cmd curl
check_cmd caddy

echo
echo "=== Caddy ==="
if systemctl is-active caddy >/dev/null 2>&1; then
  echo "OK: Caddy is active"
else
  echo "STOP: Caddy is not active" >&2
  failures=$((failures + 1))
fi

if sudo caddy validate --config /etc/caddy/Caddyfile >/dev/null; then
  echo "OK: Caddyfile validates"
else
  echo "STOP: Caddyfile validation failed" >&2
  failures=$((failures + 1))
fi

echo
echo "=== Existing protected app ports ==="
require_listener "Task Scheduler App" 8135
require_listener "Financial Command Center" 8095
require_listener "existing n8n" 5678

warn_if_public_bind "Task Scheduler App" 8135
warn_if_public_bind "Financial Command Center" 8095
warn_if_public_bind "existing n8n" 5678

echo
echo "=== LobeHub reserved ports ==="
for port in 9000 8080 3210 3000 5050; do
  if sudo ss -tulpn | grep -q ":${port} "; then
    echo "OK: LobeHub reserved port $port is already in use or reserved."
  else
    echo "REVIEW: no listener found on LobeHub reserved port $port. Do not assign this port to RepLife unless you intentionally confirmed LobeHub does not use it."
  fi
done

echo
echo "=== Planned RepLife service ports ==="
warn_if_in_use_for_new_service "Matomo" 8081
warn_if_in_use_for_new_service "Uptime Kuma" 3001
warn_if_in_use_for_new_service "Postiz" 4007
warn_if_in_use_for_new_service "Postiz Temporal UI" 4080

echo
echo "=== Docker containers ==="
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

echo
if [ "$failures" -ne 0 ]; then
  echo "STOP: protected-app preflight found $failures issue(s). Fix or intentionally review them before continuing." >&2
  exit 1
fi

echo "Protected-app preflight passed."
