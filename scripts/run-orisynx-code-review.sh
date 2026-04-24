#!/bin/bash
# One-shot: trigger Orisynx code review via Jarvis session
# Scheduled for 18:00 UTC (7 PM WAT) on 2026-04-16

CHAT_ID="-5249388197"
LOG="/home/claw/.openclaw/workspace/logs/orisynx-code-review.log"
MARKER="/home/claw/.openclaw/workspace/.state/orisynx-code-review-triggered.flag"

# Don't run twice
if [ -f "$MARKER" ]; then
  echo "[$(date -u)] Already triggered, skipping." >> "$LOG"
  exit 0
fi

touch "$MARKER"
echo "[$(date -u)] Starting Orisynx code review subagent..." >> "$LOG"

openclaw session send \
  --message "INTERNAL_TRIGGER: Run the Orisynx code review now using the subagent. Repos: Orisynx/backend, Orisynx/frontend, Orisynx/bootstrap. Use gh CLI, compare against baselines (backend 9c46d48, frontend d7c73b0, bootstrap bd2973d). Save report to outputs/orisynx-code-review-2026-04-16.md and post a summary to the Jarvis-Orisynx Telegram group." \
  2>> "$LOG" || true

echo "[$(date -u)] Trigger sent." >> "$LOG"
