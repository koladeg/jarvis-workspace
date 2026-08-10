#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
TRACKER_FILE="${TRACKER_FILE:-$WORKSPACE/config/adugboinsure-funding-tracker.json}"
LOG_FILE="${LOG_FILE:-$WORKSPACE/logs/adugboinsure-grants.log}"
TODAY="$(date -u +%Y-%m-%d)"
REPORT_FILE="${GRANT_FILE:-$WORKSPACE/memory/adugboinsure-weekly-grants-${TODAY}.md}"
RADAR_SCRIPT="${RADAR_SCRIPT:-$WORKSPACE/scripts/adugboinsure-funding-radar.sh}"

mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$REPORT_FILE")"
touch "$LOG_FILE"

log() {
  printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" >> "$LOG_FILE"
}

if [ ! -f "$TRACKER_FILE" ]; then
  log "Funding tracker missing: $TRACKER_FILE"
  echo "Funding tracker missing: $TRACKER_FILE" >&2
  exit 1
fi

if [ ! -x "$RADAR_SCRIPT" ]; then
  log "Funding radar script missing or not executable: $RADAR_SCRIPT"
  echo "Funding radar script missing or not executable: $RADAR_SCRIPT" >&2
  exit 1
fi

python3 "$WORKSPACE/scripts/verify_funding_source.py" validate-tracker "$TRACKER_FILE" >/dev/null

DASHBOARD_PATH="$($RADAR_SCRIPT)"

python3 - "$TRACKER_FILE" "$REPORT_FILE" "$TODAY" "$DASHBOARD_PATH" <<'PY'
import json
import sys
from pathlib import Path

tracker_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
today = sys.argv[3]
dashboard_path = sys.argv[4]

data = json.loads(tracker_path.read_text())
items = data.get("items", [])
active = [i for i in items if i.get("state") == "active"]
watched = [i for i in items if i.get("state") == "watched"]
stale = [i for i in items if i.get("state") == "stale"]
unknown = [i for i in items if i.get("state") == "unknown"]

lines = []
lines.append("# AdugboInsure Weekly Grant Search")
lines.append("")
lines.append(f"- Generated (UTC): {today}")
lines.append(f"- Tracker update: {data.get('meta', {}).get('last_updated', 'unknown')}")
lines.append(f"- Dashboard: {dashboard_path}")
lines.append("")
lines.append("## Verified status")
if active:
    lines.append(f"- Active opportunities: {len(active)}")
    for item in active:
        lines.append(f"  - {item['name']} | deadline: {item.get('deadline') or 'not recorded'} | fit: {item.get('fit', 'unknown')} | last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')}")
elif watched or unknown:
    lines.append("- No active opportunities are currently verified.")
    lines.append(f"- Watched opportunities: {len(watched)}")
    for item in watched:
        lines.append(f"  - {item['name']} | deadline: {item.get('deadline') or 'not recorded'} | fit: {item.get('fit', 'unknown')} | last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')}")
    if unknown:
        lines.append(f"- Unknown / browser-verification-needed opportunities: {len(unknown)}")
        for item in unknown:
            lines.append(f"  - {item['name']} | last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')} | note: {item.get('notes', 'n/a')}")
else:
    lines.append("- No active August funding opportunity is currently verified in the tracker.")
    lines.append("- Do not claim a live funding win until a real source check updates the tracker.")

if stale:
    lines.append("")
    lines.append("## Historical / stale references")
    for item in stale:
        lines.append(f"- {item['name']} | last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')} | note: {item.get('notes', 'n/a')}")

lines.append("")
lines.append("## Honesty rule")
lines.append("- This file is tracker-backed only and intentionally does not send Telegram messages or pretend a live scan happened.")

out_path.write_text("\n".join(lines) + "\n")
PY

log "Weekly grant report generated at $REPORT_FILE using tracker $TRACKER_FILE"
echo "$REPORT_FILE"
