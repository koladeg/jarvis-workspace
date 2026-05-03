# HEARTBEAT.md - Periodic Tasks

Run every ~30 minutes. Uses `ollama/llama3.2:3b` (free, local) for lightweight checks.

## Tasks

- Check git status in workspace (any uncommitted changes?)
- Note: Add email/calendar checks when needed

## Jarvis Mistake Review

Run a lightweight self-audit on a 12-hour cadence during heartbeat — 7:00 AM WAT and 7:00 PM WAT — or immediately after a clear mistake.

### Goal
- Quietly capture real lessons
- Update guardrails when a repeated pattern appears
- Stay silent unless there is something actionable

### Trigger rules
- Run at most **twice per day** during heartbeat on the 12-hour schedule above unless a fresh notable error happened
- Also run after mistakes involving:
  - wrong assumptions about access/auth
  - repeating the same workflow mistake
  - group-chat judgment failures
  - claiming work was done/blocked before verifying

### Process
1. Review only the current session / recent work
2. If there was no meaningful mistake or pattern, do nothing
3. If there was a meaningful mistake:
   - append a concise entry to `memory/mistakes-log.md`
   - if useful, tighten the relevant local rule/checklist
4. Only alert Kolade if there is a **new durable guardrail** or a **repeated pattern** worth knowing

### Logging command
```bash
python3 /home/claw/.openclaw/workspace/scripts/analyze-mistake.py \
  --mistake "short description" \
  --context "where it happened" \
  --root-cause "why it happened" \
  --guardrail "mechanical prevention rule" \
  --pattern "optional pattern note"
```

## Scheduled Reminders

**Saturdays at 08:00 WAT (07:00 UTC)** — RECURRING
- Reminder: Ask Kolade for fresh NotebookLM cookies **privately** for AdugboInsure automation
- Task: Get cookie file/session needed to run NotebookLM content automation for **3 videos** covering the next **3 weeks**
- Why: We are switching from browser-bridge setup to cookie-based execution for reliability/speed
- Security: Never request or accept cookies in the group chat; ask for them via private/direct channel only

**Fridays at 18:00 UTC (7:00 PM WAT)** — RECURRING
- Reminder: Check NotebookLM token before Sunday automation
- Task: Provide fresh NotebookLM auth token (if expired) so AdugboInsure content generation can run Sunday 18:00 UTC
- Why: Tokens last ~2-4 weeks; refresh before they expire
- ⚠️ ALSO: Run `bash scripts/credentials-verify.sh` and report results to Kolade
  - If any REQUIRED creds missing: tell Kolade immediately, ask to re-provide
  - If any creds expiring in < 7 days: warn Kolade to refresh
  - Format: "🔐 Weekly Creds Check: X/Y present. [list any issues]"

**Robin News Lane (cron-owned):**
- Tuesday — 7:05 PM WAT
- Saturday — 9:05 AM WAT
- Status: ✅ Present in `/home/claw/.openclaw/cron/jobs.json`

**ACTIVE CRON JOBS (Set 2026-03-25 10:06 UTC):**

**Bank Document Reminders** — Daily at 09:00, 15:00, 21:00 UTC (10:00, 16:00, 22:00 WAT)
- Message: "Bank Document Reminder — Everyone needs to fill the bank document"
- Duration: Today + tomorrow (auto-sends via `/scripts/send-reminders.sh`)
- Status: ✅ LIVE

**Dev Sync-Up Reminder** — Every Thursday at 08:00 UTC (09:00 WAT)
- Message: "Dev Sync-Up Today — Front-end & Back-end sync scheduled"
- Frequency: Weekly (repeating)
- Status: ✅ LIVE
