# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Local Commands

- `~/\.openclaw/workspace/scripts/model-switch openai` → switch default model to `openai-codex/gpt-5.4`
- `~/\.openclaw/workspace/scripts/model-switch opus` → switch default model to `anthropic/claude-opus-4-6`
- `~/\.openclaw/workspace/scripts/model-switch toggle` → flip between the two
- `~/\.openclaw/workspace/scripts/model-switch status` → show current default model

## Research / Browsing Tools

- **agent-browser**
  - Installed at `/usr/bin/agent-browser`
  - Default browser path for web tasks
  - Use for live page inspection, dynamic/React-style sites, and any page where shallow reads look suspiciously thin or contradictory
  - Prefer this before concluding that a site is empty or blocked in a meaningful way

- **Apify**
  - Use as a heavier extraction path when normal browsing/fetching is weak, blocked, too noisy, or too manual
  - Especially useful for job boards, paginated listings, archive-style opportunity sites, and repeated source monitoring
  - Good fallback when a site has visible data but lighter extraction paths are unreliable

- **Nairaland**
  - Use as a secondary Nigeria-specific discovery source across multiple pipelines
  - Good for surfacing local signals on grants, jobs, events, community-support organizations, and other opportunity threads
  - Do not treat Nairaland threads as proof by themselves; verify promising leads at the original source before trusting or reporting them strongly

## Recurring Automation Rule

- Recurring jobs (cron, watchers, heartbeats, reminders) should stay **shell-first and Ollama-first**.
- Prefer plain shell/Python/state files/direct bot sends.
- If lightweight interpretation is needed, prefer local `llama3.2:3b`.
- Do not introduce paid-model dependency into recurring jobs unless there is a documented reason.
- Policy reference: `RECURRING_AUTOMATION_POLICY.md`

---

Add whatever helps you do your job. This is your cheat sheet.
