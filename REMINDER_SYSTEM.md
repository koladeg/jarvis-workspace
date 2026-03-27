# Autonomous Reminder & Notification System

**Status:** ✅ LIVE & OPERATIONAL (installed 2026-03-25 13:41 UTC)

## Overview

The reminder system is a background daemon that automatically sends Telegram notifications at scheduled times. It requires no manual intervention — set it and forget it.

### What It Does

- ✅ Monitors `config/reminders.json` for scheduled events
- ✅ Sends Telegram messages automatically at the scheduled time
- ✅ Persists across system restarts (via cron)
- ✅ Prevents duplicate messages (24-hour state tracking)
- ✅ Logs all activity for debugging
- ✅ Runs every 5 minutes (negligible resource overhead)

---

## Current Configuration

### Active Reminders

1. **Friday NotebookLM Check** (Every Friday at 18:00 UTC / 19:00 WAT)
   - Reminds to check/refresh NotebookLM token before Sunday automation
   - Recipient: AdugboInsure channel

2. **AdugboInsure Meeting Alert** (Every Tuesday at 14:00 UTC / 15:00 WAT)
   - 30-minute advance notice before team meeting
   - Recipient: AdugboInsure channel

3. **Dev Sync-Up** (Every Thursday at 08:00 UTC / 09:00 WAT)
   - Weekly front-end & back-end synchronization
   - Recipient: AdugboInsure channel

### Channels Configured

- `adugboinsure` → -5126825082 (Jarvis-AdugboInsure)
- `orisynx` → -5249388197 (Jarvis-Orisynx)
- `truck` → -5025917446 (Jarvis-Truck-Listings)
- `job_search` → -5224228330 (Jarvis-Job-Search)
- `portfolio` → -5174964902 (Jarvis-Portfolio)

---

## Installation & Setup

### Verify Installation

```bash
# Check daemon status
bash scripts/setup-reminder-daemon.sh status

# Output shows:
# ✅ Cron job installed
# Cron entry: */5 * * * * cd /home/claw/.openclaw/workspace && ...
```

### Initial Installation (if needed)

```bash
bash scripts/setup-reminder-daemon.sh install
```

Requirements automatically checked:
- ✅ curl (for Telegram API)
- ✅ config/reminders.json (configuration)
- ✅ .credentials/telegram_bot_config.txt (Telegram bot token)

### Test Run

```bash
bash scripts/setup-reminder-daemon.sh test

# Output:
# ✅ All requirements met
# ✅ Daemon executed successfully
```

---

## How to Add a New Reminder

Edit `config/reminders.json` and add an entry to the `reminders` array:

```json
{
  "id": "my-weekly-check",
  "enabled": true,
  "channel": "adugboinsure",
  "schedule": "0 10 * * 1",
  "description": "Monday 10am check",
  "message": "📋 **Weekly Task Check**\n\nTime to review this week's tasks!"
}
```

### Schedule Format (Cron)

Standard 5-field cron format: `minute hour day month weekday`

Examples:
- `0 9 * * 1` — Every Monday at 09:00 UTC
- `30 15 * * 5` — Every Friday at 15:30 UTC
- `0 18 * * *` — Every day at 18:00 UTC
- `0 12 15 * *` — Every 15th of month at 12:00 UTC

### Message Format

Messages support Markdown:
- **bold** → `**text**`
- _italic_ → `_text_`
- Newlines → `\n` (in JSON: `\\n`)
- Monospace → `` `code` ``
- Links → `[text](url)`

Example:
```json
"message": "📅 **Meeting Today**\n\nScheduled for 14:00 UTC.\n\n[Join Zoom](https://zoom.link)"
```

### Channel Reference

Available channels (use channel ID as `"channel"` value):
- `adugboinsure` — Main AdugboInsure updates
- `orisynx` — Orisynx project
- `truck` — Truck listings
- `job_search` — Job search automation
- `portfolio` — Portfolio updates

---

## Remove a Reminder

Set `"enabled": false` in `config/reminders.json`:

```json
{
  "id": "old-reminder",
  "enabled": false,
  ...
}
```

Or delete the entire block. The daemon will skip disabled reminders.

---

## Troubleshooting

### No messages being sent?

Check the daemon log:
```bash
tail -20 logs/reminder-daemon.log
```

Common issues:
- **Config file missing:** Create or verify `config/reminders.json`
- **Credentials missing:** Verify `.credentials/telegram_bot_config.txt` exists
- **Schedule doesn't match:** Verify cron schedule is correct for current time
- **Channel ID invalid:** Check channel IDs in `config/reminders.json`

### Manual test of specific reminder

The daemon automatically runs every 5 minutes. To force a test:
```bash
bash scripts/reminder-daemon.sh
```

View output in logs:
```bash
tail logs/reminder-daemon.log
```

### Check if cron job is active

```bash
crontab -l
```

Should show:
```
*/5 * * * * cd /home/claw/.openclaw/workspace && bash /home/claw/.openclaw/workspace/scripts/reminder-daemon.sh >> /home/claw/.openclaw/workspace/logs/reminder-daemon.log 2>&1
```

### Uninstall (remove cron job)

```bash
bash scripts/setup-reminder-daemon.sh uninstall
```

Reminders will stop running, but configuration stays intact.

---

## How It Works (Technical Details)

### Architecture

1. **Cron Entry** — Triggers every 5 minutes
2. **Daemon Script** (`scripts/reminder-daemon.sh`)
   - Locks to prevent concurrent execution
   - Loads Telegram bot credentials
   - Parses `config/reminders.json`
   - Checks each reminder's schedule against current time
   - Prevents duplicates using state files in `.reminder-state/`
   - Sends Telegram messages via API
   - Logs all activity

### State Tracking

Reminders are marked as "sent" for 20 hours to prevent duplicates:
- State file: `.reminder-state/{reminder_id}.state`
- Contains: Unix timestamp of last send
- Resets after 20 hours

### Error Handling

- **Lock file** prevents concurrent executions
- **Timeout** on Telegram API failures (logs error, continues)
- **Log file** tracks all activity: `logs/reminder-daemon.log`
- **Automatic retry** on next 5-minute cycle

### Resource Usage

- CPU: Negligible (brief JSON parse + HTTP call every 5 minutes)
- Memory: < 5 MB (bash process)
- Network: 1 HTTP request per triggered reminder
- Disk: ~1 KB per week of logs

---

## Examples

### Example 1: Daily standup reminder

```json
{
  "id": "daily-standup",
  "enabled": true,
  "channel": "adugboinsure",
  "schedule": "0 9 * * *",
  "description": "Daily 9am standup",
  "message": "🎯 **Daily Standup**\n\nTime for the daily sync.\n\nPlease share:\n• What did you do yesterday?\n• What are you doing today?\n• Any blockers?"
}
```

### Example 2: Monthly deadline

```json
{
  "id": "monthly-report-due",
  "enabled": true,
  "channel": "adugboinsure",
  "schedule": "0 17 25 * *",
  "description": "Monthly report due on 25th",
  "message": "📊 **Monthly Report Due Tomorrow**\n\nPlease submit by EOD tomorrow.\n\n[Template](https://example.com/template)"
}
```

### Example 3: Disable a reminder temporarily

```json
{
  "id": "old-meeting",
  "enabled": false,
  "channel": "adugboinsure",
  "schedule": "0 10 * * 1",
  "message": "This reminder is disabled"
}
```

---

## Reliability Guarantees

| Aspect | Guarantee | How |
|--------|-----------|-----|
| **Missed message** | Will re-send within 5 min | Cron runs every 5 min, state resets after 20h |
| **Duplicate** | Won't send twice in 20h | State file tracking |
| **Persist restart** | Yes, survives system reboot | Cron is persistent |
| **API failure** | Logs error, retries next cycle | Automatic retry |
| **Concurrent run** | Prevented | Lock file mechanism |

---

## Quick Reference

| Task | Command |
|------|---------|
| Check status | `bash scripts/setup-reminder-daemon.sh status` |
| Test daemon | `bash scripts/setup-reminder-daemon.sh test` |
| View logs | `tail logs/reminder-daemon.log` |
| Edit reminders | Open `config/reminders.json` in any editor |
| Reload config | Automatic (checked every 5 min) |
| Disable reminder | Set `"enabled": false` in config |
| Remove reminder | Delete block or disable |

---

## Configuration Files

### `config/reminders.json`
Main configuration file. Edit to add/remove/modify reminders. No restart needed.

### `.reminder-state/` directory
Contains state files (one per reminder). Auto-created. Safe to delete (just clears state history).

### `logs/reminder-daemon.log`
Full activity log. Append-only. Safe to delete or rotate.

### `.credentials/telegram_bot_config.txt`
Telegram bot token and channel IDs. Keep secure. Required for daemon to work.

---

## Support

If reminders aren't working:

1. Run `bash scripts/setup-reminder-daemon.sh status`
2. Check `logs/reminder-daemon.log` for errors
3. Verify `config/reminders.json` is valid JSON
4. Verify schedule format is correct
5. Run `bash scripts/setup-reminder-daemon.sh test` for manual test

---

_System installed: 2026-03-25 13:41 UTC_
_Next review: Add more reminders as needed. No maintenance required._
