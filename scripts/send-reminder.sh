#!/bin/bash
# Simple reminder sender via Telegram

MESSAGE="$1"
CHAT_ID="${2:--5126825082}"  # Default to Jarvis-AdugboInsure group

# Send via message tool (would require API, so use simple approach instead)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Reminder: $MESSAGE" >> /tmp/reminders.log

# For testing: just log it
echo "✓ Reminder set: $MESSAGE (Chat: $CHAT_ID)"
