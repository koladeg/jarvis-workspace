#!/bin/bash
# Send shareholder agreement reminder to Jarvis-Orisynx group

MESSAGE="Team, please sign the shareholder agreement if you haven't already."

# Using openclaw message tool via CLI
openclaw msg send \
  --channel telegram \
  --target "Jarvis-Orisynx" \
  --message "$MESSAGE"

echo "[$(date)] Orisynx shareholder reminder sent" >> /home/claw/.openclaw/workspace/logs/orisynx-reminder.log
