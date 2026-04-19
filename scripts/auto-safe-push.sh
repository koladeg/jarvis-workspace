#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
cd "$WORKSPACE"

LOG_DIR="$WORKSPACE/logs"
mkdir -p "$LOG_DIR"

SAFE_PATHS=(
  "ADUGBOINSURE_CONTENT_PROCESS.md"
  "MEMORY.md"
  "RESEARCH_AGENT_ROLLOUT.md"
  "SOUL.md"
  "TOOLS.md"
  "memory/2026-04-03.md"
  "memory/ARCHIVE.md"
  "scripts/run-research-rollout-schedule.sh"
  "scripts/research-bot-daemon.sh"
  "scripts/research-bot-listener.py"
  "scripts/send-research-activity-update.sh"
  "scripts/send-research-rollout-update.sh"
)

CHANGED=()
for path in "${SAFE_PATHS[@]}"; do
  if [ -e "$path" ] && ! git diff --quiet -- "$path" 2>/dev/null; then
    CHANGED+=("$path")
  elif [ -e "$path" ] && git diff --cached --quiet -- "$path" 2>/dev/null; then
    if ! git ls-files --error-unmatch "$path" >/dev/null 2>&1; then
      CHANGED+=("$path")
    fi
  elif [ -e "$path" ] && [ -n "$(git status --porcelain -- "$path")" ]; then
    CHANGED+=("$path")
  fi
done

if [ ${#CHANGED[@]} -eq 0 ]; then
  echo "No safe changes to commit"
  exit 0
fi

git add -- "${CHANGED[@]}"

if git diff --cached --quiet; then
  echo "No staged safe changes after git add"
  exit 0
fi

git commit -m "Daily safe automation: $(date +%Y-%m-%d)"
git push origin main

echo "Pushed safe changes: ${CHANGED[*]}"
