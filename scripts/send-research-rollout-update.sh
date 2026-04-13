#!/bin/bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
DEFAULT_RESEARCH_WORKSPACE="$WORKSPACE/workspace-research"
if [ ! -d "$DEFAULT_RESEARCH_WORKSPACE" ]; then
  DEFAULT_RESEARCH_WORKSPACE="/home/claw/.openclaw/workspace-research"
fi
RESEARCH_WORKSPACE="${RESEARCH_WORKSPACE:-$DEFAULT_RESEARCH_WORKSPACE}"
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
TODAY_STATUS=$(extract_value "- **Today status:**")
MAIN_BLOCKER=$(extract_value "- **Main blocker:**")
NEXT_ACTION=$(extract_value "- **Next action:**")

if [ "$CURRENT_HASH" = "$LAST_HASH" ]; then
  CHANGE_LINE="No major rollout-tracker change since the previous update."
else
  CHANGE_LINE="The rollout tracker changed since the previous update."
fi

PARSED_OUTPUT=$(python3 - "$LATEST_RESEARCH_FILE" <<'PY'
import re, sys
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] else None
if not path or not path.exists():
    print('NO_FILE=1')
    raise SystemExit

text = path.read_text(encoding='utf-8')


def get_section(title):
    m = re.search(rf'^## {re.escape(title)}\n(.*?)(?=^## |\Z)', text, re.S | re.M)
    return m.group(1).strip() if m else ''


def clean(s):
    s = re.sub(r'\*\*', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def find_entries(section):
    entries = []
    for m in re.finditer(r'^###\s+(.+?)\n(.*?)(?=^###\s+|\Z)', section, re.S | re.M):
        title = clean(m.group(1))
        body = m.group(2)
        fields = {}
        for line in body.splitlines():
            line = line.strip()
            m2 = re.match(r'^-\s+\*\*(.+?)\*\*:\s*(.+)$', line)
            if m2:
                fields[clean(m2.group(1)).lower()] = clean(m2.group(2))
        entries.append((title, fields, clean(body)))
    return entries

funding = get_section('Funding')
events = get_section('Networking events')
trucks = get_section('Trucks')
jobs = get_section('Jobs')

fund_entries = find_entries(funding)
event_entries = find_entries(events)
truck_summary = ''
job_summary = ''

if jobs:
    m = re.search(r'No .*?jobs.*?(?:\.|$)', jobs, re.I | re.S)
    if m:
        job_summary = clean(m.group(0))
    else:
        lines = [clean(ln.lstrip('- ').strip()) for ln in jobs.splitlines() if ln.strip() and not ln.startswith('###')]
        if lines:
            job_summary = lines[0]

if trucks:
    lines = [clean(ln.lstrip('- ').strip()) for ln in trucks.splitlines() if ln.strip()]
    for ln in lines:
        if 'no clean fit' in ln.lower() or 'no meaningful fit' in ln.lower() or 'budget' in ln.lower() or 'configuration mismatch' in ln.lower():
            truck_summary = ln
            break
    if not truck_summary and lines:
        truck_summary = lines[0]

def out(key, value):
    print(f'{key}={value}')

out('NO_FILE', '0')
out('JOBS_SUMMARY', job_summary or 'No strong new jobs summary surfaced cleanly yet.')
out('TRUCKS_SUMMARY', truck_summary or 'No trucks summary captured.')

for idx in range(2):
    if idx < len(fund_entries):
        title, fields, body = fund_entries[idx]
        out(f'FUND{idx+1}_TITLE', title)
        out(f'FUND{idx+1}_URL', fields.get('official source') or fields.get('source') or '')
        out(f'FUND{idx+1}_WHY', fields.get('why it fits') or fields.get('fit') or fields.get('why it made the cut') or '')
        out(f'FUND{idx+1}_DEADLINE', fields.get('deadline status') or fields.get('preliminary application deadline') or '')
    else:
        out(f'FUND{idx+1}_TITLE', '')
        out(f'FUND{idx+1}_URL', '')
        out(f'FUND{idx+1}_WHY', '')
        out(f'FUND{idx+1}_DEADLINE', '')

for idx in range(2):
    if idx < len(event_entries):
        title, fields, body = event_entries[idx]
        out(f'EVENT{idx+1}_TITLE', title)
        out(f'EVENT{idx+1}_URL', fields.get('direct source') or fields.get('source') or '')
        out(f'EVENT{idx+1}_DATE', fields.get('date / place') or '')
        out(f'EVENT{idx+1}_WHY', fields.get('why it matters') or '')
    else:
        out(f'EVENT{idx+1}_TITLE', '')
        out(f'EVENT{idx+1}_URL', '')
        out(f'EVENT{idx+1}_DATE', '')
        out(f'EVENT{idx+1}_WHY', '')
PY
)

declare -A DATA
while IFS='=' read -r key value; do
  [ -n "$key" ] || continue
  DATA["$key"]="$value"
done <<< "$PARSED_OUTPUT"

if [ "${DATA[NO_FILE]:-0}" = "1" ]; then
  MESSAGE=$(cat <<EOF
🔎 Research Update

Time: ${WAT_NOW} (${UTC_NOW})
Latest note: none

No research note was available yet.
EOF
)
else
  MESSAGE=$(cat <<EOF
🔎 Research Update

Time: ${WAT_NOW} (${UTC_NOW})
Latest note: ${LATEST_RESEARCH_BASENAME}

Funding
- ${DATA[FUND1_TITLE]:-No funding lead captured}
- URL: ${DATA[FUND1_URL]:-n/a}
- Why it matters: ${DATA[FUND1_WHY]:-n/a}
- Deadline/status: ${DATA[FUND1_DEADLINE]:-n/a}
- ${DATA[FUND2_TITLE]:-No second funding lead captured}
- URL: ${DATA[FUND2_URL]:-n/a}
- Why it matters: ${DATA[FUND2_WHY]:-n/a}
- Deadline/status: ${DATA[FUND2_DEADLINE]:-n/a}

Networking events
- ${DATA[EVENT1_TITLE]:-No event lead captured}
- URL: ${DATA[EVENT1_URL]:-n/a}
- Date/place: ${DATA[EVENT1_DATE]:-n/a}
- Why it matters: ${DATA[EVENT1_WHY]:-n/a}
- ${DATA[EVENT2_TITLE]:-No second event lead captured}
- URL: ${DATA[EVENT2_URL]:-n/a}
- Date/place: ${DATA[EVENT2_DATE]:-n/a}
- Why it matters: ${DATA[EVENT2_WHY]:-n/a}

Jobs
- ${DATA[JOBS_SUMMARY]:-No strong new jobs summary surfaced cleanly yet.}

Trucks
- ${DATA[TRUCKS_SUMMARY]:-No trucks summary captured.}

Rollout status
- ${CHANGE_LINE}
- Today: ${TODAY_STATUS}
- Blocker: ${MAIN_BLOCKER}
- Next: ${NEXT_ACTION}
EOF
)
fi

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
