#!/bin/bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
RESEARCH_WORKSPACE="${RESEARCH_WORKSPACE:-/home/claw/.openclaw/workspace-research}"
BOT_TOKEN_FILE="${WORKSPACE}/.credentials/telegram_research_agent_bot_token.txt"
ROLLOUT_FILE="${WORKSPACE}/RESEARCH_AGENT_ROLLOUT.md"
STATE_DIR="${WORKSPACE}/.state"
STATE_FILE="${STATE_DIR}/research-rollout-last-hash.txt"
MESSAGE_HASH_FILE="${STATE_DIR}/research-rollout-last-message-hash.txt"
CHAT_ID="${CHAT_ID:-7101554375}"
TZ_WAT="Africa/Lagos"

mkdir -p "$STATE_DIR" "${WORKSPACE}/logs"

[ -f "$BOT_TOKEN_FILE" ] || { echo "Bot token file not found: $BOT_TOKEN_FILE" >&2; exit 1; }
[ -f "$ROLLOUT_FILE" ] || { echo "Rollout file not found: $ROLLOUT_FILE" >&2; exit 1; }

TELEGRAM_BOT_TOKEN=$(cat "$BOT_TOKEN_FILE")
[ -n "${TELEGRAM_BOT_TOKEN:-}" ] || { echo "TELEGRAM_BOT_TOKEN missing" >&2; exit 1; }

CURRENT_HASH=$(sha256sum "$ROLLOUT_FILE" | awk '{print $1}')
LAST_HASH=""
[ -f "$STATE_FILE" ] && LAST_HASH=$(cat "$STATE_FILE")

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

lane_summary() {
  local label="$1"
  local file="$2"
  [ -f "$file" ] || { printf 'No %s summary captured' "$label"; return; }
  python3 - "$label" "$file" <<'PY'
import sys,re
label=sys.argv[1]
path=sys.argv[2]
text=open(path,'r',encoding='utf-8').read()
patterns={
  'Jobs':[r'## Jobs lane quality test.*?(?=\n## |\Z)', r'## Jobs scheduled run.*?(?=\n## |\Z)'],
  'Funding':[r'## Funding lane quality test.*?(?=\n## |\Z)', r'## Funding scheduled run.*?(?=\n## |\Z)'],
  'Events':[r'## Networking events lane quality test.*?(?=\n## |\Z)', r'## Networking events scheduled run.*?(?=\n## |\Z)'],
  'Trucks':[r'## Trucks lane quality test.*?(?=\n## |\Z)', r'## Trucks scheduled run.*?(?=\n## |\Z)'],
  'Partners':[r'## Community sponsors lane.*?(?=\n## |\Z)', r'## Community sponsors scheduled run.*?(?=\n## |\Z)'],
}
block=''
for pat in patterns.get(label,[]):
    matches=re.findall(pat,text,re.S)
    if matches:
        block=matches[-1]
        break
if not block:
    print(f'No {label.lower()} summary captured')
    raise SystemExit
lines=[ln.strip('- ').strip() for ln in block.splitlines()[1:] if ln.strip()]
status=''
useful=[]
for ln in lines:
    low=ln.lower()
    if low.startswith('status:'):
        status=ln.split(':',1)[1].strip()
    elif any(low.startswith(prefix) for prefix in ['1-2 useful','1-2 strongest','2 retained','strongest roles','what happened','live-source condition','source quality notes','honest result','quality judgment','useful outcome']):
        useful.append(ln)
summary=status or (useful[0] if useful else '')
if not summary:
    # prefer first non-empty content line
    summary=lines[0] if lines else f'No {label.lower()} summary captured'
summary=summary.replace('Status: ','').replace('status: ','')
summary=re.sub(r'\s+',' ',summary).strip()
print(summary[:180])
PY
}

JOBS_SUMMARY=$(lane_summary "Jobs" "$LATEST_RESEARCH_FILE")
EVENTS_SUMMARY=$(lane_summary "Events" "$LATEST_RESEARCH_FILE")
FUNDING_SUMMARY=$(lane_summary "Funding" "$LATEST_RESEARCH_FILE")
PARTNERS_SUMMARY=$(lane_summary "Partners" "$LATEST_RESEARCH_FILE")
TRUCKS_SUMMARY=$(lane_summary "Trucks" "$LATEST_RESEARCH_FILE")

MESSAGE=$(cat <<EOF
🔎 Research Agent Rollout

Time: ${WAT_NOW} (${UTC_NOW})
Overall status: ${OVERALL_STATUS}
Current phase: ${CURRENT_PHASE}
Rollout tracker last updated: ${LAST_UPDATED}
Latest research note seen: ${LATEST_RESEARCH_BASENAME}

Pipeline snapshot
- Jobs: ${JOBS_SUMMARY}
- Events: ${EVENTS_SUMMARY}
- Funding: ${FUNDING_SUMMARY}
- Partners: ${PARTNERS_SUMMARY}
- Trucks: ${TRUCKS_SUMMARY}

What this means
- ${CHANGE_LINE}
- Today: ${TODAY_STATUS}
- Completed: ${COMPLETED_TODAY}
- Blocker: ${MAIN_BLOCKER}
- Next: ${NEXT_ACTION}
EOF
)

MESSAGE_HASH=$(printf '%s' "$MESSAGE" | sha256sum | awk '{print $1}')
LAST_MESSAGE_HASH=""
[ -f "$MESSAGE_HASH_FILE" ] && LAST_MESSAGE_HASH=$(cat "$MESSAGE_HASH_FILE")
if [ "$MESSAGE_HASH" = "$LAST_MESSAGE_HASH" ]; then
  echo "Research rollout update skipped (duplicate message)"
  exit 0
fi

curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" >/dev/null

echo "$CURRENT_HASH" > "$STATE_FILE"
echo "$MESSAGE_HASH" > "$MESSAGE_HASH_FILE"
echo "Research rollout update sent to ${CHAT_ID}"
