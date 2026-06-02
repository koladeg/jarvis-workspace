# MEMORY.md

Condensed long-term memory for the main workspace.

Archive:
- Full pre-trim snapshot saved to `memory/MEMORY.pre-trim-2026-05-25.md`
- Keep this file lean so OpenClaw does not inject unnecessary history into every request

## Current durable state (2026-06-02)

- AdugboInsure queue discipline: use already-prepared content before generating fresh weekly videos.
- AdugboInsure ready assets still include the `2026-04-12`, `2026-04-15`, `2026-04-16`, `2026-04-29`, `2026-05-10`, `2026-05-23`, `2026-05-24`, `2026-05-26`, `2026-05-27`, `2026-05-29`, `2026-05-30`, `2026-05-31`, and `2026-06-02` packages.
- NotebookLM remains blocked by expired/false-positive auth; repeated checks through `2026-06-02` still ended with `Authentication expired`, manual cookie import still did not restore real access, and `nlm login --force` still failed with `No supported browser found`.
- Robin reliability lesson remains durable: session bloat and listener/runtime queueing can break responsiveness; evidence-first reporting and lightweight fast-path replies should stay in place.
- Robin listener hardening on `2026-05-22`: keep the local single-instance lock and async background-run path for long multi-lane requests.
- Robin direct-chat fix on `2026-05-25`: the research listener/runner must launch from `/home/claw/.openclaw/workspace-research`, not the heavy main workspace.
- Main server constraint remains critical: this host has about `2 GiB` RAM, so large bootstrap context and high OpenClaw concurrency materially increase hang risk.
- OpenClaw default model was switched on `2026-05-25` to `openai-codex/gpt-5.4` because Anthropic was billing-rejected and adding failover delay.
- Cron durable guardrail from `2026-05-22`: use explicit provider/model IDs in cron jobs; do not assume local Ollama model identifiers will pass cron allowlists.
- Durable browsing guardrail: dynamic/React-style sites should be checked with `agent-browser` before declaring them empty.
- Durable GitHub guardrail: do not infer private-repo access from unauthenticated browser `404`s; verify with authenticated `gh` or API access first.
- Local Ollama remains preferred for lightweight routine tasks, but this host often lacks enough free RAM for `llama3.2:3b` when the system is under load.
- RAM hygiene lesson from `2026-05-26`: stale `agent-browser`/Chrome trees can exhaust RAM and swap; trim them before blaming local-model or browser failures.
- Gmail resume delivery remains operational; the Dash0 tailored DOCX was successfully sent through `jarviskolademail@gmail.com` on `2026-05-26`.
- GitHub CLI auth on this machine was repaired on `2026-05-28`; `gh` is authenticated again as `koladeg` after refreshing the saved token.

## Active blockers

- A browser-backed NotebookLM reauthentication path; manual cookie import alone still does not restore real access here

## High-value durable references

- AdugboInsure positioning: the insurance product comes from OYSHIA; AdugboInsure is the community access, awareness, enrollment, and payment-support channel.
- AdugboInsure opportunity tracking: UNICEF Venture Fund Climate and Health 2026 and Visa Africa FinTech Accelerator Program 6 were already submitted as of `2026-05-08`.
- Orisynx primary repos to monitor: `Orisynx/backend`, `Orisynx/frontend`, `Orisynx/bootstrap`.
- Orisynx durable docs:
  - `ORISYNX_CONFLICT_RESOLUTION_FRAMEWORK.md`
  - `memory/orisynx.md`
- DOCX durable workflow: use the local `skills/docx-safe/` fork.
- mhGAP/Indigo durable lesson: prefer same-signed versionCode `10` recovery/update builds over more ADB-only extraction attempts.
- Resume/deliverable preference: prefer email for personal files/results and GitHub for project/code/docs when Drive is awkward.

## Next-step reminders

- Keep OpenClaw config conservative on this server.
- Keep MEMORY concise; move bulky historical material into archive files instead of expanding this file again.
- If Robin responsiveness regresses, inspect queue depth, concurrent worker count, and main-session bootstrap size before rebooting.
