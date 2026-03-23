#!/usr/bin/env bash
# =============================================================================
# credentials-init.sh - Bootstrap & Initialize Credentials System
# =============================================================================
# Purpose: First-time setup + daily session init. Creates all dirs, 
#          installs save_credential() into ~/.bashrc, runs first verify.
# Usage:   bash scripts/credentials-init.sh
# =============================================================================

set -euo pipefail

WORKSPACE="/home/claw/.openclaw/workspace"
CREDS_DIR="$WORKSPACE/.credentials"
INDEX_FILE="$CREDS_DIR/CREDENTIALS_INDEX.json"
SCRIPTS_DIR="$WORKSPACE/scripts"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║         CREDENTIALS SYSTEM INITIALIZATION                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# --- Step 1: Ensure .credentials directory exists with correct perms ---
if [ ! -d "$CREDS_DIR" ]; then
  mkdir -p "$CREDS_DIR"
  echo "✓ Created .credentials directory"
else
  echo "✓ .credentials directory exists"
fi

# Lock down the directory
chmod 700 "$CREDS_DIR"
echo "✓ Permissions set: 700 (owner-only)"

# --- Step 2: Ensure CREDENTIALS_INDEX.json exists ---
if [ ! -f "$INDEX_FILE" ]; then
  echo "⚠️  CREDENTIALS_INDEX.json missing! This should have been created."
  echo "   Run the credentials-verify.sh script to diagnose."
  exit 1
else
  echo "✓ CREDENTIALS_INDEX.json found"
fi

# --- Step 3: Lock down all credential files ---
find "$CREDS_DIR" -type f -name "*.txt" -o -name "*.json" 2>/dev/null | while read -r f; do
  chmod 600 "$f"
done
echo "✓ All credential files set to 600 (owner-only)"

# --- Step 4: Install save_credential() function into ~/.bashrc ---
BASHRC="$HOME/.bashrc"
MARKER="# === JARVIS CREDENTIALS SYSTEM ==="

if grep -q "$MARKER" "$BASHRC" 2>/dev/null; then
  echo "✓ save_credential() already in ~/.bashrc — skipping install"
else
  cat >> "$BASHRC" << 'BASHRC_BLOCK'

# === JARVIS CREDENTIALS SYSTEM ===
# Auto-installed by credentials-init.sh
# DO NOT EDIT manually — managed by credential system

JARVIS_WORKSPACE="/home/claw/.openclaw/workspace"
JARVIS_CREDS_DIR="$JARVIS_WORKSPACE/.credentials"
JARVIS_INDEX="$JARVIS_CREDS_DIR/CREDENTIALS_INDEX.json"

# Save a credential safely and update the index
# Usage: save_credential <name> <value> <service> [expiry_date] [notes]
save_credential() {
  local NAME="$1"
  local VALUE="$2"
  local SERVICE="$3"
  local EXPIRY="${4:-null}"
  local NOTES="${5:-}"

  if [ -z "$NAME" ] || [ -z "$VALUE" ] || [ -z "$SERVICE" ]; then
    echo "❌ Usage: save_credential <name> <value> <service> [expiry_date] [notes]"
    echo "   Example: save_credential github_token ghp_xxx github 2027-03-23 'repo read/write'"
    return 1
  fi

  # Normalize: lowercase, underscores
  local FILENAME="${SERVICE}_${NAME}.txt"
  local FILEPATH="$JARVIS_CREDS_DIR/$FILENAME"
  local NOW
  NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # Save the file
  echo "$VALUE" > "$FILEPATH"
  chmod 600 "$FILEPATH"

  # Format expiry for JSON
  local EXPIRY_JSON
  if [ "$EXPIRY" = "null" ] || [ -z "$EXPIRY" ]; then
    EXPIRY_JSON="null"
  else
    EXPIRY_JSON="\"$EXPIRY\""
  fi

  # Format notes for JSON
  local NOTES_JSON
  NOTES_JSON=$(echo "$NOTES" | sed 's/"/\\"/g')

  # Update CREDENTIALS_INDEX.json using Python (handles JSON properly)
  python3 << PYTHON_BLOCK
import json, sys, os
from datetime import datetime

index_path = "$JARVIS_INDEX"

with open(index_path, 'r') as f:
    index = json.load(f)

# Check if credential already exists
existing = None
for cred in index['credentials']:
    if cred['file'] == "$FILENAME":
        existing = cred
        break

entry = {
    "name": "$NAME",
    "file": "$FILENAME",
    "service": "$SERVICE",
    "status": "present",
    "last_updated": "$NOW",
    "expiry_date": $EXPIRY_JSON,
    "notes": "$NOTES_JSON",
    "required": existing.get("required", False) if existing else False
}

if existing:
    for i, cred in enumerate(index['credentials']):
        if cred['file'] == "$FILENAME":
            index['credentials'][i] = entry
            break
    print(f"  (updated existing entry)")
else:
    index['credentials'].append(entry)
    print(f"  (added new entry)")

index['_meta']['last_updated'] = "$NOW"
index['_meta']['updated_by'] = "save_credential()"

with open(index_path, 'w') as f:
    json.dump(index, f, indent=2)
PYTHON_BLOCK

  if [ $? -eq 0 ]; then
    echo ""
    echo "✅ CREDENTIAL SAVED AND VERIFIED"
    echo "   Name:    $NAME"
    echo "   Service: $SERVICE"
    echo "   File:    $FILEPATH"
    echo "   Updated: $NOW"
    [ "$EXPIRY" != "null" ] && echo "   Expires: $EXPIRY"
    echo ""
    echo "✓ Index updated: $JARVIS_INDEX"
    echo "✓ File exists: $([ -f "$FILEPATH" ] && echo "YES" || echo "NO — BUG!")"
  else
    echo "❌ FAILED to update credentials index!"
    echo "   File was saved to: $FILEPATH"
    echo "   But index update failed. Fix manually."
    return 1
  fi
}

# Quick verification check (run on login)
check_credentials() {
  if [ -f "$JARVIS_WORKSPACE/scripts/credentials-verify.sh" ]; then
    bash "$JARVIS_WORKSPACE/scripts/credentials-verify.sh" --quiet
  fi
}

# Export for subshells
export -f save_credential
export -f check_credentials
# === END JARVIS CREDENTIALS SYSTEM ===
BASHRC_BLOCK

  echo "✓ save_credential() installed into ~/.bashrc"
  echo "  Reload with: source ~/.bashrc"
fi

# --- Step 5: Run initial verification ---
echo ""
echo "Running initial verification..."
echo ""
bash "$SCRIPTS_DIR/credentials-verify.sh"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              INITIALIZATION COMPLETE                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Run:  source ~/.bashrc"
echo "  2. Save missing creds: save_credential github_token <value> github"
echo "  3. Schedule weekly: Add scripts/credentials-verify.sh to HEARTBEAT.md"
echo ""
