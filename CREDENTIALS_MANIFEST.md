# CREDENTIALS MANIFEST — Status Dashboard

**Purpose:** Human-readable view of all credentials. The machine-readable source of truth is `.credentials/CREDENTIALS_INDEX.json`.

**⚠️ IMPORTANT:** This file shows what SHOULD exist. Run `bash scripts/credentials-verify.sh` to check what ACTUALLY exists on disk.

---

## Live Status Dashboard

| Credential | Service | File | Status | Last Updated | Expires | Notes |
|------------|---------|------|--------|--------------|---------|-------|
| **Notion API Key** | Notion | `notion_api_key.txt` | ✅ PRESENT | 2026-03-16 | Never | Workspace access: AuditBoard, Community Health Insurance, Pro TypeScript |
| **Telegram Bot Config** | Telegram | `telegram_bot_config.txt` | ✅ PRESENT | 2026-03-23 | Never | Bot token + 5 chat IDs for all Jarvis groups |
| **NotebookLM Cookies** | Google | `notebooklm_cookies.txt` | ✅ PRESENT | 2026-03-23 | ~2026-04-13 | Google OAuth session — refresh every 2-4 weeks |
| **YouTube OAuth** | Google | `youtube_oauth.json` | ✅ PRESENT | 2026-03-20 | ~2026-09-20 | OAuth refresh token for uploads |
| **Gmail App Password** | Google | `gmail_app_password.txt` | ✅ PRESENT | 2026-03-23 | Never | `jarviskolademail@gmail.com` IMAP access |
| **GitHub Token** | GitHub | `github_token.txt` | ❌ MISSING | — | Never | **ACTION NEEDED: Kolade must provide** |
| **Vercel Token** | Vercel | `vercel_token.txt` | ⚠️ MISSING | — | Never | Optional — Kolade to provide when available |

**Last verified:** 2026-03-23 by credentials system init

---

## Action Items

### 🔴 CRITICAL — Required Credentials Missing

**GitHub Token**
- What: Personal access token
- Scopes needed: `repo` (read/write), `gist`, `workflow`
- Where to get: github.com → Settings → Developer settings → Personal access tokens
- How to save: `save_credential github_token <value> github null "repo read/write, gist, workflow"`
- Why needed: git auth, GitHub API calls, code pushes

### 🟡 Optional — Nice to Have

**Vercel Token**
- What: Vercel API token
- Where to get: vercel.com → Settings → Tokens
- How to save: `save_credential vercel_token <value> vercel null "deployment management"`
- Why needed: deployment monitoring, site updates

---

## Enforcement Rules

**NEW SYSTEM (2026-03-23):** Jarvis now uses `save_credential()` to save ALL credentials.

1. Kolade provides token in chat
2. Jarvis immediately runs: `save_credential <name> <value> <service>`
3. File is written to `.credentials/` with 600 permissions
4. `CREDENTIALS_INDEX.json` is updated with metadata
5. Confirmation: "✅ CREDENTIAL SAVED AND VERIFIED"
6. This manifest is updated to reflect new status

**The old problem:** Jarvis "intended" to save but never wrote the file.  
**The fix:** Mechanical enforcement via `save_credential()` function in `~/.bashrc`.

See `CREDENTIALS_README.md` for full how-to guide.

---

## Weekly Verification (Heartbeat)

Every Friday, Jarvis runs:
```bash
bash scripts/credentials-verify.sh
```

If missing credentials are found → Jarvis reports to Kolade immediately.

**Expiry monitoring:**
- NotebookLM cookies: Warn 7 days before expiry (~2-4 week cycle)
- YouTube OAuth: Warn 7 days before expiry (~3-6 month cycle)
- All others: No expiry

---

## Audit Trail

| Date | Event | Result |
|------|-------|--------|
| 2026-03-23 20:52 | Full credentials audit | 5/7 present; GitHub + Vercel missing |
| 2026-03-23 20:55 | Credentials system deployed | `save_credential()` + verify scripts live |
| 2026-03-23 20:55 | Gmail app password saved | Moved from MEMORY.md to `.credentials/gmail_app_password.txt` |
| 2026-03-18 | GitHub token claimed saved | ❌ Never actually saved (root cause identified) |
| 2026-03-18 | Vercel token claimed saved | ❌ Never actually saved (root cause identified) |

---

## Git Safety Rules

✅ **SAFE to commit:** This manifest, `CREDENTIALS_INDEX.json` (no values), `CREDENTIALS_README.md`  
❌ **NEVER commit:** Any `.credentials/*.txt` file, `youtube_oauth.json`, anything with actual token values

---

*Source of truth: `.credentials/CREDENTIALS_INDEX.json` — Updated automatically by `save_credential()`*
