#!/bin/bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
CRED_FILE="${WORKSPACE}/.credentials/telegram_bot_config.txt"
CHAT_ID="7101554375"
TZ_WAT="Africa/Lagos"

if [ ! -f "$CRED_FILE" ]; then
  echo "Credentials file not found: $CRED_FILE" >&2
  exit 1
fi

set -a
source "$CRED_FILE"
set +a

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "TELEGRAM_BOT_TOKEN missing" >&2
  exit 1
fi

UTC_NOW=$(date -u '+%Y-%m-%d %H:%M UTC')
WAT_NOW=$(TZ="$TZ_WAT" date '+%Y-%m-%d %H:%M WAT')
WEEKDAY=$(TZ="$TZ_WAT" date '+%A')

cd "$WORKSPACE"

BRANCH_LINE=$(git status --short --branch 2>/dev/null | head -n 1 || true)
CHANGES=$(git status --short 2>/dev/null | wc -l | tr -d ' ')

if [ "$CHANGES" = "0" ]; then
  GIT_LINE="- Workspace: clean"
else
  GIT_LINE="- Workspace: ${CHANGES} uncommitted change(s)"
fi

case "$WEEKDAY" in
  Monday)
    PRIORITIES=$'- SiFax work: 09:00-12:00\n- AdugboInsure focus: afternoon\n- Jarvis funding radar: 18:00 if there are fresh finds'
    ;;
  Tuesday)
    PRIORITIES=$'- SiFax work: 09:00-12:00\n- Truck listing scan target: 12:00\n- AdugboInsure / Orisynx: afternoon focus'
    ;;
  Wednesday)
    PRIORITIES=$'- SiFax work: 09:00-12:00\n- Orisynx sprint check-in prep: 14:00\n- Orisynx team sync: afternoon'
    ;;
  Thursday)
    PRIORITIES=$'- Job application shortlist day\n- Truck listing scan target: 12:00\n- AdugboInsure agent management: evening'
    ;;
  Friday)
    PRIORITIES=$'- SiFax work: 09:00-12:00\n- AWS study nudge + quiz: 17:00\n- AWS study session: evening'
    ;;
  Saturday)
    PRIORITIES=$'- Truck listing scan: 09:00\n- AdugboInsure field work / agent meetings: 10:00\n- Flexible afternoon for Orisynx / programming / personal'
    ;;
  Sunday)
    PRIORITIES=$'- Weekly review & planning summary: 10:00\n- Weekly planning: afternoon\n- Next week priorities finalized: 18:00'
    ;;
  *)
    PRIORITIES='- No schedule loaded'
    ;;
esac

MESSAGE=$(cat <<EOF
🌅 *Morning Brief*\n\n- Time: ${WAT_NOW} (${UTC_NOW})\n- Day: ${WEEKDAY}\n${GIT_LINE}\n\n*Today's priorities*\n${PRIORITIES}\n\n*Assumptions check*\n- Reply if priorities changed today\n- Reply if you want me to tighten this brief further
EOF
)

curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" \
  -d "parse_mode=Markdown" >/dev/null

echo "Morning brief sent to ${CHAT_ID}"
