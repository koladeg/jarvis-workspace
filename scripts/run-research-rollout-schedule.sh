#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
RESEARCH_WORKSPACE="${RESEARCH_WORKSPACE:-/home/claw/.openclaw/workspace-research}"
MEMORY_DIR="$RESEARCH_WORKSPACE/memory"
LOG_DIR="$WORKSPACE/logs"
STATE_DIR="$WORKSPACE/.state"
TODAY_UTC="$(date -u +%Y-%m-%d)"
NOW_UTC="$(date -u '+%Y-%m-%d %H:%M UTC')"
RUN_STAMP="$(date -u '+%H:%M UTC')"
NOTE_FILE="$MEMORY_DIR/${TODAY_UTC}.md"
RUN_LOG="$LOG_DIR/research-rollout-schedule.log"
ISO_DOW="${FORCE_DOW:-$(date -u +%u)}"   # 1=Mon ... 7=Sun
WEEK_NUM="${FORCE_WEEK_NUM:-$(date -u +%V)}"

mkdir -p "$MEMORY_DIR" "$LOG_DIR" "$STATE_DIR"
touch "$RUN_LOG"

log() {
  printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" | tee -a "$RUN_LOG" >&2
}

ensure_note_header() {
  if [ ! -f "$NOTE_FILE" ]; then
    cat > "$NOTE_FILE" <<EOF
# Research pass — ${TODAY_UTC}

## Automated rollout schedule note
- This file tracks scheduled Robin pipeline runs and same-day logging.
EOF
  fi
}

section_exists() {
  local marker="$1"
  grep -Fq "$marker" "$NOTE_FILE" 2>/dev/null
}

append_section() {
  local text="$1"
  printf '\n%s\n' "$text" >> "$NOTE_FILE"
}

run_jobs() {
  local marker="## Jobs scheduled run (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: due today under the approved schedule
- What was actually checked: scheduled jobs lane trigger recorded
- Change state: no fresh lane-specific extraction performed inside this scheduler step
- Follow-up: run or verify the next real jobs-source pass and record sources checked, search depth, and strongest roles surfaced
- Honest note: this scheduler confirms cadence and same-day logging; it does not by itself replace the deeper jobs-search workflow"
  fi
}

run_funding() {
  local marker="## Funding scheduled run (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: due today under the approved schedule
- What was actually checked: scheduled funding lane trigger recorded
- Change state: no fresh funding-source sweep performed inside this scheduler step
- Follow-up: keep only active, deadline-visible, relevant opportunities in the next live funding pass
- Honest note: cadence/logging confirmed; fresh funding findings still depend on the lane-specific scan"
  fi
}

run_networking() {
  local marker="## Networking events scheduled run (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: due today under the approved schedule
- What was actually checked: scheduled networking-events trigger recorded
- Change state: no fresh event-source sweep performed inside this scheduler step
- Follow-up: prefer actionable, near-term, clearly relevant events only; tie each one to AdugboInsure or Orisynx value
- Honest note: scheduler confirmed timing; event quality still depends on the actual source check"
  fi
}

run_trucks() {
  local marker="## Trucks scheduled run (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: due today under the approved schedule
- What was actually checked: scheduled trucks lane trigger recorded
- Change state: no fresh marketplace scan performed inside this scheduler step
- Follow-up: separate strong-fit / near-fit / reject clearly in the next live truck pass
- Honest note: scheduler confirms monitoring cadence; it does not substitute for real listing extraction"
  fi
}

run_school() {
  local marker="## School-MBA scheduled run (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: due today under the approved schedule
- What was actually checked: scheduled school/MBA lane trigger recorded
- Change state: no fresh program/scholarship scan performed inside this scheduler step
- Follow-up: prioritize funded or funding-accessible MBA, business, innovation, entrepreneurship, and technology options
- Honest note: cadence is confirmed here; stronger value still comes from the actual school/MBA pass"
  fi
}

run_community_sponsors() {
  local marker="## Community sponsors scheduled run (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: due today under the approved lower-frequency schedule
- What was actually checked: scheduled community-sponsors trigger recorded
- Change state: no fresh sponsor mapping performed inside this scheduler step
- Follow-up: focus on real community backers, not generic partnership wishlists
- Honest note: cadence/logging confirmed; sponsor quality still depends on the live review"
  fi
}

run_immigration() {
  local marker="## Immigration scheduled run (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: due today under the approved lower-frequency schedule
- What was actually checked: immigration lane due marker recorded with expected route set
- Expected routes: Canada Express Entry, Australia National Innovation Visa, UK Global Talent Visa, EB-2 NIW, EB-1A
- Expected output shape: route, why it matters, new requirement/timing/cost signal, blocker, and next action
- Change state: no fresh route/source review performed inside this scheduler step
- Follow-up: track named routes and practical changes only
- Honest note: scheduler confirms the review slot; actual route progress still depends on the live immigration pass"
  fi
}

run_weekly_roundup() {
  local marker="## Weekly roundup scheduled run (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: due today under the approved schedule
- What was actually checked: scheduled weekly-roundup trigger recorded
- Change state: no compiled cross-lane summary was generated inside this scheduler step
- Follow-up: compare strongest findings, blockers, and next actions across active lanes
- Honest note: this confirms the roundup slot exists; the useful summary still has to be produced"
  fi
}

run_mistake_review() {
  local marker="## Mistake review cycle (${TODAY_UTC} ${RUN_STAMP})"
  if ! section_exists "$marker"; then
    append_section "${marker}
- Status: scheduled improvement loop executed
- Mistake cluster reviewed: rollout/logging reliability, browser/dynamic-site mistakes, misleading reporting risk
- Parallelization: planned for sub-agent use where useful; not yet proven in this scheduler-only step
- Improvement made: same-day logging rule and schedule-backed cadence are now being exercised repeatedly
- Still unresolved: make mistake-review output more concrete and prove real parallel review behavior"
  fi
}

ensure_note_header
run_mistake_review

case "$ISO_DOW" in
  1)
    run_jobs
    run_funding
    run_networking
    ;;
  2)
    if [ $((10#$WEEK_NUM % 2)) -eq 0 ]; then
      run_community_sponsors
    fi
    ;;
  3)
    run_jobs
    run_trucks
    run_school
    ;;
  4)
    if [ $((10#$WEEK_NUM % 2)) -eq 0 ]; then
      run_immigration
    fi
    ;;
  5)
    run_funding
    run_networking
    run_trucks
    ;;
  7)
    run_weekly_roundup
    ;;
esac

log "Scheduled research rollout pass recorded in $NOTE_FILE"

# Push activity updates after the note is refreshed.
# Rollout summaries are sent on their own calmer twice-daily cron cadence.
bash "$WORKSPACE/scripts/send-research-activity-update.sh" >> "$LOG_DIR/research-activity.log" 2>&1 || true
