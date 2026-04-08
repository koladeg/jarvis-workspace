#!/bin/bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
CRED_FILE="${WORKSPACE}/.credentials/telegram_bot_config.txt"
CACHE_DIR="${WORKSPACE}/.cache/orisynx-weekly-brief"
STATE_DIR="${WORKSPACE}/.state/orisynx-weekly-brief"
LOG_FILE="${WORKSPACE}/logs/orisynx-weekly-brief.log"
BOT_TARGET_DEFAULT="-5249388197"
BACKEND_REPO_URL="https://github.com/Orisynx/Orisynx-backend.git"
FRONTEND_REPO_URL="https://github.com/Audit-IS/fe.git"
BACKEND_DIR="${CACHE_DIR}/Orisynx-backend"
FRONTEND_DIR="${CACHE_DIR}/fe"
LAST_SENT_FILE="${STATE_DIR}/last_sent_utc.txt"
TARGET_CHAT_ID="${1:-$BOT_TARGET_DEFAULT}"

mkdir -p "$CACHE_DIR" "$STATE_DIR" "$(dirname "$LOG_FILE")"

log() {
  echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] $*" >> "$LOG_FILE"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 1; }
}

require_cmd git
require_cmd curl
require_cmd python3

if [ ! -f "$CRED_FILE" ]; then
  echo "Credentials file not found: $CRED_FILE" >&2
  exit 1
fi

set -a
source "$CRED_FILE"
set +a

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "TELEGRAM_BOT_TOKEN missing from $CRED_FILE" >&2
  exit 1
fi

if [ -f "$LAST_SENT_FILE" ]; then
  SINCE="$(cat "$LAST_SENT_FILE")"
else
  SINCE="$(date -u -d '7 days ago' '+%Y-%m-%dT%H:%M:%SZ')"
fi
NOW_UTC="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
NOW_LABEL="$(date -u '+%Y-%m-%d %H:%M UTC')"

sync_repo() {
  local url="$1"
  local dir="$2"
  if [ ! -d "$dir/.git" ]; then
    git clone --quiet "$url" "$dir"
    log "Cloned $url into $dir"
  else
    git -C "$dir" fetch --all --prune --quiet
    log "Fetched updates for $dir"
  fi
}

format_repo_section() {
  local label="$1"
  local dir="$2"
  local remote_url="$3"

  local head branch count log_lines status_line
  head="$(git -C "$dir" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  branch="$(git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
  count="$(git -C "$dir" rev-list --count --since="$SINCE" HEAD 2>/dev/null || echo 0)"
  if [ "$count" -eq 0 ] 2>/dev/null; then
    status_line="No new commits since last brief"
    log_lines="- none"
  else
    log_lines="$(git -C "$dir" log --since="$SINCE" --pretty=format:'- %ad — %s' --date=short -n 5 2>/dev/null || true)"
    status_line="${count} new commit(s) since last brief"
  fi

  printf '*%s*\n- Status: %s\n- Branch: `%s`\n- HEAD: `%s`\n- Repo: %s\n%s\n' \
    "$label" "$status_line" "$branch" "$head" "$remote_url" "$log_lines"
}

sync_repo "$BACKEND_REPO_URL" "$BACKEND_DIR"
sync_repo "$FRONTEND_REPO_URL" "$FRONTEND_DIR"

BACKEND_SECTION="$(format_repo_section 'Backend' "$BACKEND_DIR" "$BACKEND_REPO_URL")"
FRONTEND_SECTION="$(format_repo_section 'Frontend' "$FRONTEND_DIR" "$FRONTEND_REPO_URL")"

MESSAGE=$(cat <<EOF
📊 *Orisynx Friday Repo Brief*

Period: ${SINCE} → ${NOW_UTC}
Generated: ${NOW_LABEL}

${BACKEND_SECTION}
${FRONTEND_SECTION}
*Notes*
- This is the automatic repo-change brief.
- If needed, Jarvis can follow up with deeper code-review commentary on risk, architecture, and meeting talking points.
EOF
)

RESPONSE=$(curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TARGET_CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" \
  -d "parse_mode=Markdown")

if echo "$RESPONSE" | grep -q '"ok":true'; then
  printf '%s' "$NOW_UTC" > "$LAST_SENT_FILE"
  log "Brief sent successfully to ${TARGET_CHAT_ID}"
  echo "OK"
else
  log "Failed to send brief: $RESPONSE"
  echo "$RESPONSE" >&2
  exit 1
fi
