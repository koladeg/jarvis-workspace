#!/bin/bash
set -euo pipefail

MAIN_WORKSPACE="${MAIN_WORKSPACE:-/home/claw/.openclaw/workspace}"
DEFAULT_RESEARCH_WORKSPACE="$MAIN_WORKSPACE/workspace-research"
if [ ! -d "$DEFAULT_RESEARCH_WORKSPACE" ]; then
  DEFAULT_RESEARCH_WORKSPACE="/home/claw/.openclaw/workspace-research"
fi
RESEARCH_WORKSPACE="${RESEARCH_WORKSPACE:-$DEFAULT_RESEARCH_WORKSPACE}"
BOT_TOKEN_FILE="${MAIN_WORKSPACE}/.credentials/telegram_research_agent_bot_token.txt"
STATE_DIR="${MAIN_WORKSPACE}/.state"
CHAT_ID="${CHAT_ID:-7101554375}"
TZ_WAT="Africa/Lagos"
STALE_HOURS="${STALE_HOURS:-24}"
STALE_STATE="${STATE_DIR}/research-activity-last-stale-date.txt"

mkdir -p "$STATE_DIR" "${MAIN_WORKSPACE}/logs"

if [ ! -f "$BOT_TOKEN_FILE" ]; then
  echo "Bot token file not found: $BOT_TOKEN_FILE" >&2
  exit 1
fi

TELEGRAM_BOT_TOKEN=$(cat "$BOT_TOKEN_FILE")

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "TELEGRAM_BOT_TOKEN missing" >&2
  exit 1
fi

LATEST_FILE=$(find "$RESEARCH_WORKSPACE/memory" -maxdepth 1 -type f -name '20*.md' | sort | tail -n 1)
if [ -z "${LATEST_FILE:-}" ]; then
  echo "No research memory file found" >&2
  exit 0
fi

FILE_HASH=$(sha256sum "$LATEST_FILE" | awk '{print $1}')
BASENAME=$(basename "$LATEST_FILE")
FILE_DATE="${BASENAME%.md}"
HASH_STATE="$STATE_DIR/research-activity-last-hash.txt"
FILE_STATE="$STATE_DIR/research-activity-last-file.txt"
LAST_HASH=""
LAST_FILE=""

[ -f "$HASH_STATE" ] && LAST_HASH=$(cat "$HASH_STATE") || true
[ -f "$FILE_STATE" ] && LAST_FILE=$(cat "$FILE_STATE") || true

UTC_NOW=$(date -u '+%Y-%m-%d %H:%M UTC')
WAT_NOW=$(TZ="$TZ_WAT" date '+%Y-%m-%d %H:%M WAT')
TODAY_UTC=$(date -u '+%Y-%m-%d')
FILE_TS=$(date -d "$FILE_DATE 00:00:00 UTC" +%s)
NOW_TS=$(date -u +%s)
AGE_HOURS=$(( (NOW_TS - FILE_TS) / 3600 ))
HAS_NEW_ACTIVITY="no"

extract_after_line() {
  local marker="$1"
  awk -v marker="$marker" '
    index($0, marker) {found=1; next}
    found && /^### / {exit}
    found && NF {print; exit}
  ' "$LATEST_FILE"
}

JOB_LINE=$(extract_after_line "### 1) Jobs")
EVENT_LINE=$(extract_after_line "### 2) Networking events")
FUNDING_LINE=$(extract_after_line "### 3) Funding")
PARTNER_LINE=$(extract_after_line "### 4) Partners / Validators")
TRUCK_LINE=$(extract_after_line "### 5) Trucks")

if [ "$FILE_HASH" != "$LAST_HASH" ] || [ "$BASENAME" != "$LAST_FILE" ]; then
  HAS_NEW_ACTIVITY="yes"
  MESSAGE=$(cat <<EOF
🧭 Research Agent Update

Time: ${WAT_NOW} (${UTC_NOW})
New activity: yes
Latest research note: ${BASENAME}

Highlights
- Jobs: ${JOB_LINE:-No jobs summary captured}
- Events: ${EVENT_LINE:-No events summary captured}
- Funding: ${FUNDING_LINE:-No funding summary captured}
- Partners: ${PARTNER_LINE:-No partner summary captured}
- Trucks: ${TRUCK_LINE:-No truck summary captured}
EOF
)

  curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    --data-urlencode "text=${MESSAGE}" >/dev/null

  echo "$FILE_HASH" > "$HASH_STATE"
  echo "$BASENAME" > "$FILE_STATE"
  echo "Research activity update sent from ${BASENAME}"
  exit 0
fi

if [ "$AGE_HOURS" -ge "$STALE_HOURS" ]; then
  LAST_STALE_DATE=""
  [ -f "$STALE_STATE" ] && LAST_STALE_DATE=$(cat "$STALE_STATE") || true

  if [ "$LAST_STALE_DATE" != "$TODAY_UTC" ]; then
    MESSAGE=$(cat <<EOF
⚠️ Research Agent Status

Time: ${WAT_NOW} (${UTC_NOW})
New activity: no
Latest research note: ${BASENAME}
Staleness: about ${AGE_HOURS} hours since the last research note

Meaning: the research workspace has not logged a fresh pass recently, so there is nothing new to report yet.
EOF
)

    curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      -d "chat_id=${CHAT_ID}" \
      --data-urlencode "text=${MESSAGE}" >/dev/null

    echo "$TODAY_UTC" > "$STALE_STATE"
    echo "Stale research status sent for ${BASENAME}"
    exit 0
  fi
fi

echo "No new research activity"
