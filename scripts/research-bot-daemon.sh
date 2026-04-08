#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/home/claw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/research-bot-daemon.log"
PID_FILE="$WORKSPACE/.state/research-bot-daemon.pid"
LOCK_DIR="$WORKSPACE/.state/research-bot-daemon.lock"

mkdir -p "$WORKSPACE/logs" "$WORKSPACE/.state"

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "research-bot-daemon already running" >> "$LOG_FILE"
  exit 0
fi

cleanup() {
  rm -f "$PID_FILE"
  rmdir "$LOCK_DIR" 2>/dev/null || true
}

trap cleanup EXIT

echo $$ > "$PID_FILE"

while true; do
  python3 "$WORKSPACE/scripts/research-bot-listener.py" >> "$LOG_FILE" 2>&1 || true
  sleep 1
done
