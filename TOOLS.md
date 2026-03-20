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

---

Add whatever helps you do your job. This is your cheat sheet.
