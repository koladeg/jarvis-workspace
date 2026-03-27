# Reminder System — Quick Start

**TL;DR:** System is installed and running. Automatic reminders are now active.

---

## ✅ What's Running

Your reminder daemon is installed and will send Telegram messages automatically. No babysitting required.

### Current Reminders

- 🔐 **Every Friday 18:00 UTC** → NotebookLM token check reminder
- 📅 **Every Tuesday 14:00 UTC** → AdugboInsure meeting alert
- 💻 **Every Thursday 08:00 UTC** → Dev sync-up reminder

---

## 📝 To Add a Reminder

1. Open `config/reminders.json`
2. Add a block to the `reminders` array:

```json
{
  "id": "my-reminder-id",
  "enabled": true,
  "channel": "adugboinsure",
  "schedule": "0 9 * * 1",
  "description": "What this reminds me of",
  "message": "Your reminder text here"
}
```

3. Save. **Done.** It will be active within 5 minutes.

### Schedule Examples

- Every Monday 9 AM: `"0 9 * * 1"`
- Every day at 5 PM: `"0 17 * * *"`
- Every Friday at 3 PM: `"0 15 * * 5"`

### Channels Available

- `adugboinsure` — Main project channel
- `orisynx` — Orisynx work
- `truck` — Truck listings
- `job_search` — Job automation
- `portfolio` — Portfolio channel

---

## ⚙️ To Modify a Reminder

Edit `config/reminders.json`. Changes apply automatically (within 5 minutes).

### Disable without deleting:

Set `"enabled": false`:

```json
{
  "id": "my-reminder",
  "enabled": false,
  ...
}
```

---

## 🔍 To Check Status

```bash
bash scripts/setup-reminder-daemon.sh status
```

Shows:
- ✅ Cron job installed
- Last log entries

---

## 🧪 To Test

```bash
bash scripts/setup-reminder-daemon.sh test
```

Runs daemon once and shows logs.

---

## 📋 Message Formatting

Use Markdown in message field:

```
"message": "📅 **Meeting Today**\n\nAt 3 PM UTC.\n\n[Join here](https://zoom.link)"
```

- **bold** → `**text**`
- _italic_ → `_text_`
- Newlines → `\n`

---

## 🚨 If Nothing Happens

1. Check cron is active:
   ```bash
   bash scripts/setup-reminder-daemon.sh status
   ```

2. Check logs:
   ```bash
   tail logs/reminder-daemon.log
   ```

3. Test manually:
   ```bash
   bash scripts/setup-reminder-daemon.sh test
   ```

---

## 🔧 Remove a Reminder

Delete the block from `config/reminders.json` or set `"enabled": false`.

---

## 📚 Full Docs

Read `REMINDER_SYSTEM.md` for complete details.

---

**Everything is installed and running. You're all set!**
