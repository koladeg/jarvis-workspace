#!/usr/bin/env bash
# =============================================================================
# credentials-verify.sh - Verify All Credentials Are Present & Valid
# =============================================================================
# Purpose: Check every credential in CREDENTIALS_INDEX.json exists on disk.
#          Flag missing files. Flag expiring credentials.
#          Used by: Heartbeat checks, session startup, CI, manual audits.
#
# Usage:
#   bash scripts/credentials-verify.sh           # Full verbose output
#   bash scripts/credentials-verify.sh --quiet   # Only show problems
#   bash scripts/credentials-verify.sh --json    # Machine-readable output
#
# Exit codes:
#   0 = All required credentials present (warnings OK)
#   1 = One or more REQUIRED credentials are missing → STOP AND ASK KOLADE
#   2 = Index file missing or unreadable
# =============================================================================

WORKSPACE="/home/claw/.openclaw/workspace"
CREDS_DIR="$WORKSPACE/.credentials"
INDEX_FILE="$CREDS_DIR/CREDENTIALS_INDEX.json"

QUIET=false
JSON_OUT=false

for arg in "$@"; do
  case "$arg" in
    --quiet) QUIET=true ;;
    --json)  JSON_OUT=true ;;
  esac
done

# ─── Check index exists ───────────────────────────────────────────────────────
if [ ! -f "$INDEX_FILE" ]; then
  echo "❌ CRITICAL: CREDENTIALS_INDEX.json NOT FOUND at $INDEX_FILE"
  echo "   This is the source of truth. Something is very wrong."
  echo "   Run: bash scripts/credentials-init.sh to rebuild."
  exit 2
fi

# ─── Python verification engine ───────────────────────────────────────────────
python3 << PYTHON_SCRIPT
import json, os, sys
from datetime import datetime, timezone

CREDS_DIR = "$CREDS_DIR"
INDEX_FILE = "$INDEX_FILE"
QUIET = $( $QUIET && echo "True" || echo "False" )
JSON_OUT = $( $JSON_OUT && echo "True" || echo "False" )

try:
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)
except Exception as e:
    print(f"❌ Failed to parse CREDENTIALS_INDEX.json: {e}")
    sys.exit(2)

now = datetime.now(timezone.utc)
WARN_DAYS = 7  # flag credentials expiring within this many days

results = []
missing_required = []
missing_optional = []
expiring_soon = []
expired = []

for cred in index['credentials']:
    name = cred.get('name', '?')
    filename = cred.get('file', '')
    service = cred.get('service', '?')
    required = cred.get('required', False)
    expiry_str = cred.get('expiry_date')
    notes = cred.get('notes', '')
    expected_status = cred.get('status', 'missing')

    filepath = os.path.join(CREDS_DIR, filename)
    file_exists = os.path.isfile(filepath) and os.path.getsize(filepath) > 0

    # Check expiry
    expiry_warning = None
    if expiry_str and expiry_str != 'null':
        try:
            expiry_dt = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            days_left = (expiry_dt - now).days
            if days_left < 0:
                expiry_warning = f"EXPIRED {abs(days_left)} days ago"
                expired.append(name)
            elif days_left <= WARN_DAYS:
                expiry_warning = f"EXPIRES IN {days_left} DAYS"
                expiring_soon.append(name)
        except:
            pass

    actual_status = "present" if file_exists else "missing"

    results.append({
        "name": name,
        "file": filename,
        "service": service,
        "required": required,
        "file_exists": file_exists,
        "actual_status": actual_status,
        "expected_status": expected_status,
        "expiry_warning": expiry_warning,
        "notes": notes
    })

    if not file_exists:
        if required:
            missing_required.append(name)
        else:
            missing_optional.append(name)

# ─── Output ───────────────────────────────────────────────────────────────────

if JSON_OUT:
    output = {
        "timestamp": now.isoformat(),
        "summary": {
            "total": len(results),
            "present": sum(1 for r in results if r['file_exists']),
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "expiring_soon": expiring_soon,
            "expired": expired,
            "all_required_present": len(missing_required) == 0
        },
        "credentials": results
    }
    print(json.dumps(output, indent=2))
    sys.exit(1 if missing_required else 0)

# ─── Human-readable output ────────────────────────────────────────────────────

if not QUIET:
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║           CREDENTIALS VERIFICATION REPORT                ║")
    print(f"║  {now.strftime('%Y-%m-%d %H:%M:%S UTC'):<52}║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    total = len(results)
    present_count = sum(1 for r in results if r['file_exists'])

    print(f"  Checking {total} credentials in index...")
    print()

    for r in results:
        icon = "✅" if r['file_exists'] else ("❌" if r['required'] else "⚠️ ")
        req_tag = "[REQUIRED]" if r['required'] else "[optional]"
        line = f"  {icon} {r['name']} ({r['service']}) {req_tag}"
        if r['expiry_warning']:
            line += f" — ⏰ {r['expiry_warning']}"
        print(line)
        if not r['file_exists']:
            print(f"     └─ Expected: .credentials/{r['file']}")
            if r['notes']:
                print(f"     └─ Notes: {r['notes'][:80]}")
    
    print()

# ─── Summary block (always shown) ─────────────────────────────────────────────

present_count = sum(1 for r in results if r['file_exists'])
total = len(results)

if not QUIET or missing_required or expiring_soon or expired:
    print(f"  📊 SUMMARY: {present_count}/{total} credentials present")
    print()

if missing_required:
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║  ⛔ REQUIRED CREDENTIALS MISSING — ACTION NEEDED   ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()
    for name in missing_required:
        print(f"    ❌ {name} — MISSING (REQUIRED)")
    print()
    print("  🛑 JARVIS RULE: STOP ALL WORK THAT NEEDS THESE.")
    print("     Ask Kolade to provide the missing credentials.")
    print("     Then save with: save_credential <name> <value> <service>")
    print()

if missing_optional:
    print(f"  ⚠️  Optional missing ({len(missing_optional)}):", ", ".join(missing_optional))
    print()

if expiring_soon:
    print("  ⏰ EXPIRING SOON (< 7 days):")
    for name in expiring_soon:
        print(f"     • {name}")
    print()

if expired:
    print("  💀 EXPIRED:")
    for name in expired:
        print(f"     • {name}")
    print()

if not missing_required and not expiring_soon and not expired:
    if not QUIET:
        print("  ✅ All checks passed. System healthy.")
        print()

sys.exit(1 if missing_required else 0)
PYTHON_SCRIPT

EXIT_CODE=$?

if [ $EXIT_CODE -eq 1 ] && [ "$QUIET" = "false" ]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "HOW TO FIX:"
  echo "  source ~/.bashrc"
  echo "  save_credential <name> <token_value> <service>"
  echo ""
  echo "EXAMPLE:"
  echo "  save_credential github_token ghp_yourtoken github null 'repo read/write'"
  echo "  save_credential vercel_token vercel_xxx vercel null 'deployment management'"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

exit $EXIT_CODE
