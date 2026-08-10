#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
TRACKER_FILE="${TRACKER_FILE:-$WORKSPACE/config/adugboinsure-funding-tracker.json}"
LOG_FILE="${LOG_FILE:-$WORKSPACE/logs/adugboinsure-funding.log}"
TODAY="$(date -u +%Y-%m-%d)"
DASHBOARD_FILE="${DASHBOARD_FILE:-$WORKSPACE/memory/adugboinsure-dashboard-${TODAY}.md}"
ALLOW_SEND="${ALLOW_SEND:-0}"

mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$DASHBOARD_FILE")"
touch "$LOG_FILE"

log() {
  printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" >> "$LOG_FILE"
}

if [ ! -f "$TRACKER_FILE" ]; then
  log "Funding tracker missing: $TRACKER_FILE"
  echo "Funding tracker missing: $TRACKER_FILE" >&2
  exit 1
fi

python3 "$WORKSPACE/scripts/verify_funding_source.py" validate-tracker "$TRACKER_FILE" >/dev/null

python3 - "$TRACKER_FILE" "$DASHBOARD_FILE" "$TODAY" <<'PY'
import json
import sys
from collections import defaultdict
from pathlib import Path

tracker_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
today = sys.argv[3]

data = json.loads(tracker_path.read_text())
items = data.get("items", [])
by_state = defaultdict(list)
for item in items:
    by_state[item.get("state", "unknown")].append(item)

active = by_state.get("active", [])
watched = by_state.get("watched", [])
stale = by_state.get("stale", [])
rejected = by_state.get("rejected", [])
unknown = by_state.get("unknown", [])

lines = []
lines.append("# AdugboInsure Funding Radar")
lines.append("")
lines.append(f"- Generated (UTC): {today}")
lines.append(f"- Tracker: {tracker_path}")
lines.append(f"- Last tracker update: {data.get('meta', {}).get('last_updated', 'unknown')}")
lines.append(f"- Summary counts: active={len(active)}, watched={len(watched)}, stale={len(stale)}, rejected={len(rejected)}, unknown={len(unknown)}")
lines.append("")

if active:
    lines.append("## Active opportunities")
    for item in active:
        lines.append(f"- **{item['name']}** — deadline: {item.get('deadline') or 'not recorded'} | last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')} | source: {item.get('source', 'missing')}")
        if item.get('notes'):
            lines.append(f"  - Notes: {item['notes']}")
else:
    lines.append("## Active opportunities")
    lines.append("- None currently verified as active. Do not report an active funding opportunity until a real source check updates the tracker.")

if watched:
    lines.append("")
    lines.append("## Watched opportunities")
    for item in watched:
        lines.append(f"- **{item['name']}** — deadline: {item.get('deadline') or 'not recorded'} | last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')} | source: {item.get('source', 'missing')}")
        if item.get('notes'):
            lines.append(f"  - Notes: {item['notes']}")

if unknown:
    lines.append("")
    lines.append("## Unknown / needs browser verification")
    for item in unknown:
        lines.append(f"- **{item['name']}** — last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')} | source: {item.get('source', 'missing')}")
        if item.get('notes'):
            lines.append(f"  - Notes: {item['notes']}")

if stale:
    lines.append("")
    lines.append("## Stale / historical references")
    for item in stale:
        lines.append(f"- **{item['name']}** — last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')} | source: {item.get('source', 'missing')}")
        if item.get('notes'):
            lines.append(f"  - Notes: {item['notes']}")

if rejected:
    lines.append("")
    lines.append("## Rejected opportunities")
    for item in rejected:
        lines.append(f"- **{item['name']}** — last verified: {item.get('last_verified', 'unknown')} | verification: {item.get('verification_method', 'missing')} | source: {item.get('source', 'missing')}")
        if item.get('notes'):
            lines.append(f"  - Notes: {item['notes']}")

lines.append("")
lines.append("## Honesty rule")
lines.append("- This report is tracker-backed only. It does not claim a live funding scan happened unless the tracker was actually updated from real source checks.")

out_path.write_text("\n".join(lines) + "\n")
PY

log "Funding dashboard generated at $DASHBOARD_FILE from tracker $TRACKER_FILE"

if [ "$ALLOW_SEND" = "1" ]; then
  log "ALLOW_SEND=1 requested, but outbound posting is intentionally disabled in this script until a verified send path is wired back in without embedded secrets."
fi

echo "$DASHBOARD_FILE"
