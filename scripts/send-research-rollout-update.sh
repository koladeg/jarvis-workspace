#!/bin/bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
RESEARCH_WORKSPACE="${RESEARCH_WORKSPACE:-/home/claw/.openclaw/workspace-research}"
BOT_TOKEN_FILE="${WORKSPACE}/.credentials/telegram_research_agent_bot_token.txt"
ROLLOUT_FILE="${WORKSPACE}/RESEARCH_AGENT_ROLLOUT.md"
STATE_DIR="${WORKSPACE}/.state"
STATE_FILE="${STATE_DIR}/research-rollout-last-hash.txt"
CHAT_ID="${CHAT_ID:-7101554375}"
TZ_WAT="Africa/Lagos"

mkdir -p "$STATE_DIR" "${WORKSPACE}/logs"

if [ ! -f "$BOT_TOKEN_FILE" ]; then
  echo "Bot token file not found: $BOT_TOKEN_FILE" >&2
  exit 1
fi

if [ ! -f "$ROLLOUT_FILE" ]; then
  echo "Rollout file not found: $ROLLOUT_FILE" >&2
  exit 1
fi

TELEGRAM_BOT_TOKEN=$(cat "$BOT_TOKEN_FILE")

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "TELEGRAM_BOT_TOKEN missing" >&2
  exit 1
fi

CURRENT_HASH=$(sha256sum "$ROLLOUT_FILE" | awk '{print $1}')
LAST_HASH=""
if [ -f "$STATE_FILE" ]; then
  LAST_HASH=$(cat "$STATE_FILE")
fi

UTC_NOW=$(date -u '+%Y-%m-%d %H:%M UTC')
WAT_NOW=$(TZ="$TZ_WAT" date '+%Y-%m-%d %H:%M WAT')

extract_value() {
  local key="$1"
  local line
  line=$(grep -F -- "$key" "$ROLLOUT_FILE" | head -n 1 || true)
  line="${line#*${key} }"
  printf '%s' "$line"
}

LATEST_RESEARCH_FILE=$(find "$RESEARCH_WORKSPACE/memory" -maxdepth 1 -type f -name '20*.md' 2>/dev/null | sort | tail -n 1 || true)
LATEST_RESEARCH_BASENAME=$(basename "${LATEST_RESEARCH_FILE:-none}" 2>/dev/null || true)

CURRENT_PHASE=$(extract_value "**Current phase:**")
OVERALL_STATUS=$(extract_value "**Overall status:**")
LAST_UPDATED=$(extract_value "**Last updated (UTC):**")
TODAY_STATUS=$(extract_value "- **Today status:**")
COMPLETED_TODAY=$(extract_value "- **What completed today:**")
MAIN_BLOCKER=$(extract_value "- **Main blocker:**")
NEXT_ACTION=$(extract_value "- **Next action:**")

if [ "$CURRENT_HASH" = "$LAST_HASH" ]; then
  CHANGE_LINE="No major rollout-tracker change since the previous update."
else
  CHANGE_LINE="The rollout tracker changed since the previous update."
fi

MESSAGE=$(cat <<EOF
🔎 Research Agent Rollout

Time: ${WAT_NOW} (${UTC_NOW})
Overall status: ${OVERALL_STATUS}
Current phase: ${CURRENT_PHASE}
Rollout tracker last updated: ${LAST_UPDATED}
Latest research note seen: ${LATEST_RESEARCH_BASENAME}

What this means
- ${CHANGE_LINE}
- Today: ${TODAY_STATUS}
- Completed: ${COMPLETED_TODAY}
- Blocker: ${MAIN_BLOCKER}
- Next: ${NEXT_ACTION}
EOF
)

curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" >/dev/null

echo "$CURRENT_HASH" > "$STATE_FILE"
echo "Research rollout update sent to ${CHAT_ID}"
