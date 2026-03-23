# HEARTBEAT.md - Periodic Tasks

Run every ~30 minutes. Uses `ollama/llama3.2:3b` (free, local) for lightweight checks.

## Tasks

- Check git status in workspace (any uncommitted changes?)
- Note: Add email/calendar checks when needed

## Scheduled Reminders

**Fridays at 18:00 UTC (7:00 PM WAT)** — RECURRING
- Reminder: Check NotebookLM token before Sunday automation
- Task: Provide fresh NotebookLM auth token (if expired) so AdugboInsure content generation can run Sunday 18:00 UTC
- Why: Tokens last ~2-4 weeks; refresh before they expire
- ⚠️ ALSO: Run `bash scripts/credentials-verify.sh` and report results to Kolade
  - If any REQUIRED creds missing: tell Kolade immediately, ask to re-provide
  - If any creds expiring in < 7 days: warn Kolade to refresh
  - Format: "🔐 Weekly Creds Check: X/Y present. [list any issues]"

**Tomorrow (2026-03-23) at 2:30 PM UTC (3:30 PM WAT):**
- Send reminder to Jarvis-Orisynx group: "Team, please sign the shareholder agreement if you haven't already."
- Task: Post message to telegram group chat
