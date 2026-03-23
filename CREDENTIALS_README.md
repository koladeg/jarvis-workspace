# CREDENTIALS_README.md — How to Manage Credentials

**This is the how-to guide. For the live status dashboard, see `CREDENTIALS_MANIFEST.md`. For the machine-readable source of truth, see `.credentials/CREDENTIALS_INDEX.json`.**

---

## The Problem This Solves

Previously, Jarvis (Haiku) would "intend" to save credentials but never actually write the file. Tokens were claimed as "saved" in logs/manifest but didn't exist on disk. This caused silent failures.

**The fix:** A system where saving is enforced mechanically, not by intention.

---

## System Architecture

```
.credentials/
├── CREDENTIALS_INDEX.json   ← Source of truth (tracked in git)
├── github_token.txt         ← Actual token (NOT in git)
├── vercel_token.txt         ← Actual token (NOT in git)
├── notion_api_key.txt       ← Actual key (NOT in git)
├── telegram_bot_config.txt  ← Bot config (NOT in git)
├── notebooklm_cookies.txt   ← Session cookies (NOT in git)
├── youtube_oauth.json       ← OAuth token (NOT in git)
└── gmail_app_password.txt   ← App password (NOT in git)

scripts/
├── credentials-init.sh      ← One-time bootstrap + ~/.bashrc installer
└── credentials-verify.sh    ← Health check (run any time)

CREDENTIALS_MANIFEST.md      ← Human-readable dashboard (tracked in git)
CREDENTIALS_README.md        ← This file (tracked in git)
```

**Rule:** `.credentials/` is in `.gitignore`. Only `CREDENTIALS_INDEX.json` (metadata, no values) is committed.

---

## How to Save a New Credential

### Step 1: Kolade provides the token
Kolade shares a token value in chat or message.

### Step 2: Jarvis IMMEDIATELY calls `save_credential()`
```bash
save_credential <name> <value> <service> [expiry_date] [notes]
```

**Arguments:**
- `name` — identifier, e.g. `github_token`
- `value` — the actual secret value
- `service` — which service, e.g. `github`, `vercel`, `google`
- `expiry_date` — ISO date string or `null`, e.g. `2027-01-01`
- `notes` — description of scopes/purpose

**Example:**
```bash
save_credential "github_token" "ghp_abc123xyz" "github" "null" "repo read/write, gist, workflow"
save_credential "vercel_token" "vercel_xxx" "vercel" "null" "deployment management"
save_credential "notebooklm_cookies" "SID=xxx; HSID=yyy..." "google" "2026-04-15" "Google session cookies"
```

**What this does:**
1. Writes `<value>` to `.credentials/<service>_<name>.txt`
2. Sets file permissions to 600 (owner-only)
3. Updates `CREDENTIALS_INDEX.json` with metadata
4. Confirms: "✅ CREDENTIAL SAVED AND VERIFIED"

### Step 3: Verify it saved
```bash
bash scripts/credentials-verify.sh
```
Check that the credential appears as ✅ PRESENT.

### Step 4: Update the manifest
Edit `CREDENTIALS_MANIFEST.md` to update the status table.

---

## How to Verify All Credentials

```bash
bash scripts/credentials-verify.sh
```

**Exit codes:**
- `0` — All required credentials present (healthy)
- `1` — One or more REQUIRED credentials missing (action needed)
- `2` — Index file missing or unreadable (critical failure)

**JSON output (for automation):**
```bash
bash scripts/credentials-verify.sh --json
```

**Quiet mode (only show problems):**
```bash
bash scripts/credentials-verify.sh --quiet
```

---

## How to Retrieve a Credential

```bash
cat /home/claw/.openclaw/workspace/.credentials/<service>_<name>.txt
```

**Examples:**
```bash
cat .credentials/github_token.txt
cat .credentials/notion_api_key.txt
cat .credentials/telegram_bot_config.txt
```

Or in a script:
```bash
GITHUB_TOKEN=$(cat .credentials/github_token.txt)
```

---

## Weekly Heartbeat Check (Fridays)

Add this to `HEARTBEAT.md` for automatic weekly checks:

```
FRIDAY CREDENTIAL CHECK:
- Run: bash scripts/credentials-verify.sh
- If any REQUIRED creds missing: ask Kolade immediately
- If any creds expiring in < 7 days: warn Kolade to refresh
- If NotebookLM cookies > 3 weeks old: warn Kolade to refresh
```

**Expected Jarvis behavior on Fridays:**
1. Run `credentials-verify.sh`
2. Report results in a message to Kolade
3. If anything is missing/expiring: flag it clearly, don't bury it
4. Do NOT claim credentials are present without running the check

---

## Jarvis Rules — MANDATORY

**Rule #1: Never claim a credential is saved without running `save_credential()`.**
Saying "I'll save it" is not saving it. The file must exist on disk.

**Rule #2: If `credentials-verify.sh` exits with code 1, STOP and tell Kolade.**
Do not proceed with tasks that require missing credentials.

**Rule #3: Save on first receipt.**
When Kolade provides a token, save it in the SAME message response. Don't say "I'll save it later" or "saved for future use."

**Rule #4: Always verify after saving.**
After calling `save_credential()`, confirm the file exists:
```bash
[ -f ".credentials/<filename>" ] && echo "✓ EXISTS" || echo "✗ MISSING — BUG"
```

**Rule #5: Index is the source of truth.**
If a credential exists in `CREDENTIALS_INDEX.json` with `"status": "present"` but the file doesn't exist, something went wrong. Fix it immediately.

---

## Expiry Management

| Credential | Expiry Type | Action |
|------------|-------------|--------|
| NotebookLM cookies | ~2-4 weeks | Ask Kolade to re-auth in browser, extract new cookies |
| YouTube OAuth | ~3-6 months | Run `scripts/youtube_auth.py` to refresh |
| Notion API Key | None | No action needed |
| Telegram Bot Token | None | No action needed |
| GitHub Token | Until revoked | Regenerate if scopes change |
| Vercel Token | Until revoked | Regenerate if needed |
| Gmail App Password | None | No action needed |

**Expiry warnings:** `credentials-verify.sh` flags credentials expiring within 7 days.

---

## Recovery: If `.credentials/` Is Lost

If the directory is deleted or the machine is wiped:

1. `CREDENTIALS_INDEX.json` tells you what needs to be recreated (no values stored)
2. Ask Kolade to re-provide each token
3. Use `save_credential()` to restore each one
4. Run `credentials-verify.sh` to confirm all present

---

## File Naming Convention

Credentials are stored as: `.credentials/<service>_<name>.txt`

| Service | Naming Pattern | Example |
|---------|---------------|---------|
| github | `github_<name>.txt` | `github_token.txt` → saved as `github_github_token.txt` |
| vercel | `vercel_<name>.txt` | `vercel_vercel_token.txt` |
| google | `google_<name>` | `google_notebooklm_cookies.txt` |
| notion | `notion_<name>.txt` | `notion_notion_api_key.txt` |

**Exception:** Pre-existing files (e.g., `notion_api_key.txt`) keep their original names for backward compatibility. New credentials use the `<service>_<name>.txt` pattern.

---

## Git Safety

```
.gitignore must contain:
.credentials/*.txt
.credentials/*.json (except CREDENTIALS_INDEX.json)
.credentials/*.json
```

**What IS committed:**
- `CREDENTIALS_INDEX.json` — metadata only (names, files, status, expiry)
- `CREDENTIALS_MANIFEST.md` — human dashboard
- `CREDENTIALS_README.md` — this file

**What is NEVER committed:**
- Any `.txt` file in `.credentials/`
- `youtube_oauth.json`
- Any file containing actual token values

---

## Troubleshooting

**"save_credential: command not found"**
```bash
source ~/.bashrc
```

**"CREDENTIALS_INDEX.json not found"**
```bash
bash scripts/credentials-init.sh
```

**"Index says present but file doesn't exist"**
The index is stale. Kolade needs to re-provide the credential.
```bash
save_credential <name> <new_value> <service>
```

**"Python3 not found"**
The scripts require Python 3. Install with: `sudo apt install python3`

---

*System designed 2026-03-23. Updated automatically via `save_credential()`.*
