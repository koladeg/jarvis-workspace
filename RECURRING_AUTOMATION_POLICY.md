# RECURRING_AUTOMATION_POLICY.md

## Purpose
Guardrails for cron jobs, heartbeats, watchers, reminders, and recurring background automation.

## Core Rule
Recurring automation must be **shell-first and Ollama-first**.

That means:
- Prefer plain shell, Python, cron, file reads/writes, hashes, state files, and direct API calls where safe.
- If lightweight interpretation is needed, prefer **Ollama `llama3.2:3b`**.
- Do **not** default recurring jobs to paid cloud models.

## Allowed by Default
These are acceptable for recurring/background work without extra justification:
- `bash`
- `python3`
- `cron`
- `git status`, `git diff --name-only`, file hashing, state tracking
- Local logs and memory-file reads
- Direct Telegram bot sends for reminders/updates
- `agent-browser` for pre-approved automation flows
- Ollama for lightweight summaries/checks

## Avoid by Default
Do not use these in recurring jobs unless there is a clear reason and it is documented:
- OpenAI model calls
- Anthropic model calls
- Codex/ACP for routine recurring checks
- repeated web search bursts
- browser-heavy flows when a direct/local path exists

## Escalation Rule
Escalate a recurring task beyond shell/Ollama only if:
1. the task truly requires deeper reasoning,
2. local/scripted logic is insufficient,
3. the stronger model use is explicitly documented in the task script or related notes.

## Current Approved Pattern
Recurring jobs should follow this pattern:
1. gather local or direct-source inputs
2. compare against prior state
3. send update only if changed or scheduled
4. keep logs compact
5. avoid paid-model dependency unless justified

## Current Recurring Jobs Status
The following jobs are currently compliant with this policy:
- `scripts/reminder-daemon.sh`
- `scripts/send-morning-brief.sh`
- `scripts/send-research-rollout-update.sh`
- `scripts/send-research-activity-update.sh`

## Review Rule
Before adding any new cron job or watcher:
- check whether shell/Python is enough
- check whether Ollama is enough for interpretation
- document any reason for using a paid model

## One-line Rule
If a recurring task can be done without a paid model, it must be.
