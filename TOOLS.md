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

## Resume / Email Delivery

- **Job application email path exists and should be checked first**
  - Primary sender account: `jarviskolademail@gmail.com`
  - Existing workspace automation env: `/home/claw/.openclaw/workspace/job_automation/.env`
  - App password file: `/home/claw/.openclaw/workspace/.credentials/gmail_app_password.txt`
  - Before saying email delivery is unavailable, first check whether the requested file can be sent through this existing Gmail/SMTP path.
  - For resume/CV deliverables, default behavior should be: generate file → verify file exists → use existing email route if user asked for email delivery.

## n8n (remote EC2 — NOT local)

- **n8n does NOT run locally by design.** There is no local `n8n` binary, no `~/.n8n` DB, nothing on port `5678`. Do not search for a local install — it does not exist, and that is correct.
- **Instance URL:** `http://172.31.20.229:5678` (private VPC IP, separate EC2 host).
- **API key:** `/home/claw/.openclaw/workspace/.credentials/n8n_api_key.txt` (public API key, JWT; use header `X-N8N-API-KEY: <key>`).
- **Endpoint pattern:** `http://172.31.20.229:5678/api/v1/...`
  - Workflow GET: `/api/v1/workflows/<id>`
  - Execution GET: `/api/v1/executions/<id>` and `/api/v1/executions/<id>?includeData=true` (the latter exposes `workflowData.nodes` snapshot at exec time)
  - Executions list: `/api/v1/executions?workflowId=<id>&limit=N`
- **Main workflow:** `tWjdu66FcmQwOam1` — "Multi-Region Job Search (Light Sources)" (14 sources).
- **Key lesson:** historical execution node config lives in the execution's `workflowData.nodes` (via `?includeData=true`), NOT under the workflow's current nodes. Use exec history to diff "what worked vs what broke" after a rebuild.

## ClickUp

- **ClickUp API access exists locally and should be checked before saying ClickUp is unavailable**
  - Token file: `/home/claw/.openclaw/workspace/.credentials/clickup_clickup_api_token.txt`
  - Verified workspace: `Orisynx's Workspace` (`9017801638`)
  - Verified space: `GRCS Platform` (`90173715286`)
  - Known folder: `Meetings` (`90176009754`)
  - Existing task-creation helper: `/home/claw/.openclaw/workspace/scripts/create_orisynx_medium_clickup_tickets.sh`
  - Existing MCP config: `/home/claw/.openclaw/workspace/config/mcporter.json`
  - Before saying ClickUp access is unavailable, first verify the token and run a small read-only API check such as `GET /api/v2/team`.

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

## Funding lane source strategy

- Every funding-lane pass runs both known-source monitors:
  - Opportunity Desk Grants RSS
  - Ventureburn RSS
- Every pass also runs one additive Exa discovery search:

  ```bash
  mcporter --config /home/claw/.mcporter/mcporter.json call exa.web_search_exa query="African and Nigerian early-stage healthcare, healthtech, insurtech, digital health, or community-health startup grants and accelerators with 2026 applications or funding"
  ```

- Exa is a discovery layer for finding relevant programs and organizations not already covered by the fixed RSS sources. It does not replace either RSS feed.
- Before an Exa result enters the lane output, cross-check it against the funding tracker, recent funding-lane memory notes, and other current lane records. Deduplicate by organization/program, canonical URL, and opportunity/deadline identity.
- Merge and deduplicate the RSS and Exa results before producing the final lane output. Verify promising Exa discoveries against the official source before treating them as actionable opportunities.

## Recurring Automation Rule

- Recurring jobs (cron, watchers, heartbeats, reminders) should stay **shell-first and Ollama-first**.
- Prefer plain shell/Python/state files/direct bot sends.
- If lightweight interpretation is needed, prefer local `llama3.2:3b`.
- Do not introduce paid-model dependency into recurring jobs unless there is a documented reason.
- Policy reference: `RECURRING_AUTOMATION_POLICY.md`

---

Add whatever helps you do your job. This is your cheat sheet.
