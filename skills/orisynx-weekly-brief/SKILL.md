---
name: orisynx-weekly-brief
description: Generate and send the weekly Orisynx repo brief for the backend and frontend GitHub repositories. Use when the user asks why the Orisynx update/brief was not sent, wants the Friday repo summary repaired or automated, wants a compact repo progress brief posted to Telegram, or wants this workflow turned into a durable skill/script.
---

# Orisynx Weekly Brief

Use this skill to make the Orisynx Friday repo brief real and repeatable.

## Workflow

1. Verify the failure mode first.
   - Check `config/reminders.json`.
   - Check `logs/reminder-daemon.log`.
   - Confirm whether a scheduled brief entry exists.
   - Do not assume “send failed” when the real problem might be “no job was installed.”

2. Use the sender script.
   - Primary script: `scripts/send_orisynx_weekly_brief.sh`
   - It clones or fetches both repos into `.cache/orisynx-weekly-brief/`.
   - It compares current history against the timestamp in `.state/orisynx-weekly-brief/last_sent_utc.txt`.
   - It sends a compact Telegram brief to the Orisynx group.

3. Treat the brief as two layers.
   - Layer 1: automatic repo-change brief from git history.
   - Layer 2: optional higher-value follow-up from the agent covering impact, risks, and meeting talking points.

4. Keep the automation durable.
   - Store state under `.state/orisynx-weekly-brief/`.
   - Store mirrors under `.cache/orisynx-weekly-brief/`.
   - Store logs in `logs/orisynx-weekly-brief.log`.
   - Prefer git-based collection over brittle GitHub web scraping.

## Commands

Run the brief now:

```bash
bash /home/claw/.openclaw/workspace/skills/orisynx-weekly-brief/scripts/send_orisynx_weekly_brief.sh
```

Send to a different Telegram chat id:

```bash
bash /home/claw/.openclaw/workspace/skills/orisynx-weekly-brief/scripts/send_orisynx_weekly_brief.sh <chat_id>
```

## Guardrails

- Never claim the automation exists unless the schedule or cron entry is actually installed.
- If the backend or frontend repo cannot be fetched, surface that clearly.
- Do not use this skill as a substitute for deeper architecture review; use it as the durable delivery path.
- In group chats, send the brief content only after confirming it is project-relevant and not exposing secrets.
