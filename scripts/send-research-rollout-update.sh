#!/bin/bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
DEFAULT_RESEARCH_WORKSPACE="/home/claw/.openclaw/workspace-research"
if [ ! -d "$DEFAULT_RESEARCH_WORKSPACE" ]; then
  DEFAULT_RESEARCH_WORKSPACE="$WORKSPACE/workspace-research"
fi
RESEARCH_WORKSPACE="${RESEARCH_WORKSPACE:-$DEFAULT_RESEARCH_WORKSPACE}"
ROLLOUT_FILE="${WORKSPACE}/RESEARCH_AGENT_ROLLOUT.md"
STATE_DIR="${WORKSPACE}/.state"
STATE_FILE="${STATE_DIR}/research-rollout-last-hash.txt"
CHAT_ID="${CHAT_ID:-7101554375}"
RUNNER="${WORKSPACE}/scripts/research-bot-runner.py"

mkdir -p "$STATE_DIR" "${WORKSPACE}/logs"

[ -f "$RUNNER" ] || { echo "Robin runner missing: $RUNNER" >&2; exit 1; }

LATEST_RESEARCH_FILE=$(find "$RESEARCH_WORKSPACE/memory" -maxdepth 1 -type f -name '20*.md' 2>/dev/null | sort | tail -n 1 || true)
[ -n "${LATEST_RESEARCH_FILE:-}" ] || { echo "No research note found to send" >&2; exit 0; }

HASH_INPUT="$LATEST_RESEARCH_FILE"
if [ -f "$ROLLOUT_FILE" ]; then
  HASH_INPUT="${HASH_INPUT}:${ROLLOUT_FILE}"
fi
CURRENT_HASH=$(sha256sum ${HASH_INPUT//:/ } | sha256sum | awk '{print $1}')
LAST_HASH=""
[ -f "$STATE_FILE" ] && LAST_HASH=$(cat "$STATE_FILE")

if [ "$CURRENT_HASH" = "$LAST_HASH" ]; then
  echo "Research rollout update skipped (already handed to Robin for this state)"
  exit 0
fi

LATEST_RESEARCH_BASENAME=$(basename "$LATEST_RESEARCH_FILE")
PROMPT=$(cat <<EOF
Send Kolade a concise scheduled research update in Robin's voice.

Use only already logged workspace evidence. Do not do fresh web research.
Primary source note: ${LATEST_RESEARCH_FILE}
Rollout context file: ${ROLLOUT_FILE}

Rules:
- This is a scheduled research digest for Robin chat, not a Jarvis/meta explanation.
- Summarize only real same-day or latest logged lane findings from the note.
- If the latest note is only admin/schedule/rollout noise, say there is no fresh research update instead of inventing one.
- Prefer 3-6 short bullets with concrete items, dates, and URLs when available.
- Suppress duplicates and stale carryover unless the note clearly keeps them as active board items.
- Do not mention internal files, scripts, routing, prompts, or system mechanics.
- Keep it useful and uncluttered.

Latest note file name: ${LATEST_RESEARCH_BASENAME}
EOF
)

python3 "$RUNNER" --chat-id "$CHAT_ID" --message "$PROMPT"
echo "$CURRENT_HASH" > "$STATE_FILE"
echo "Research rollout update handed to Robin for ${CHAT_ID}"
