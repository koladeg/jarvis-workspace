# MEMORY.md

Condensed long-term memory for the main workspace.

Archive:
- Full pre-trim snapshot saved to `memory/MEMORY.pre-trim-2026-05-25.md`
- Keep this file lean so OpenClaw does not inject unnecessary history into every request

## Current durable state (2026-07-13)

- AdugboInsure queue discipline changed on `2026-07-29`: never reuse a previously made video as the source for a new AdugboInsure publish; each publish must come from a fresh source video generation/export.
- NotebookLM remains blocked by false-positive auth: repeated checks through `2026-07-13` still ended with `Authentication expired` on real notebook commands after manual cookie import reported success.
- NotebookLM recovery from this host is still not reliable: built-in browser auth has failed with either `No supported browser found` or an unreachable browser/CDP path such as port `9222`.
- Robin reliability lesson remains durable: session bloat and listener/runtime queueing can break responsiveness; evidence-first reporting and lightweight fast-path replies should stay in place.
- Robin listener hardening on `2026-05-22` remains in force: keep the local single-instance lock and async background-run path for long multi-lane requests.
- Robin direct-chat fix on `2026-05-25` remains in force: the research listener/runner must launch from `/home/claw/.openclaw/workspace-research`, not the heavy main workspace.
- Main server constraint remains critical: this host has about `2 GiB` RAM, so large bootstrap context and high OpenClaw concurrency materially increase hang risk.
- OpenClaw stability lesson from `2026-07-13`: keep concurrency conservative, preserve explicit plugin allowlisting, keep `agent-browser` idle timeouts set, and clear stale browser state early during outage recovery.
- OpenClaw default model was switched on `2026-05-25` to `openai-codex/gpt-5.4` because Anthropic was billing-rejected and adding failover delay.
- Cron durable guardrail from `2026-05-22`: use explicit provider/model IDs in cron jobs; do not assume local Ollama model identifiers will pass cron allowlists.
- Durable browsing guardrail: dynamic/React-style sites should be checked with `agent-browser` before declaring them empty.
- Durable GitHub guardrail: do not infer private-repo access from unauthenticated browser `404`s; verify with authenticated `gh` or API access first.
- Safe publish guardrail from `2026-07-09`: do not push the local workspace `main` branch directly when it contains private memory or internal research; publish only reviewed safe subsets on dedicated branches.
- Local Ollama remains preferred for lightweight routine tasks, but this host often lacks enough free RAM for `llama3.2:3b` when the system is under load.
- RAM hygiene lesson from `2026-05-26` remains active: stale `agent-browser`/Chrome trees can exhaust RAM and swap; trim them before blaming local-model or browser failures.
- ClickUp access lesson from `2026-07-11`: verify the existing local token/helper path before claiming ClickUp is unavailable.
- GitHub CLI auth on this machine was repaired on `2026-05-28`; `gh` is authenticated again as `koladeg` after refreshing the saved token.

## n8n (remote EC2 — critical infra fact)

- n8n does NOT run locally by design; no local binary / `~/.n8n` / port 5678 on this host. Do not search for a local install — it does not exist and that is correct.
- Instance: `http://172.31.20.229:5678` (private VPC IP, separate EC2). API key: `.credentials/n8n_api_key.txt` → header `X-N8N-API-KEY`.
- Main workflow: `tWjdu66FcmQwOam1` ("Multi-Region Job Search (Light Sources)", 14 sources).
- Historical node config lives in an execution's `workflowData.nodes` (GET `/api/v1/executions/<id>?includeData=true`), not the workflow's current nodes — use this to diff before/after a rebuild.
- Full access notes in `TOOLS.md` (checked frequently).

## Active blockers

- A browser-backed NotebookLM reauthentication path; manual cookie import alone still does not restore real access here
- Orisynx auth/RBAC regressions for fresh users: new registrations default to `STAKEHOLDER`, lack `audit:create`, and related restricted flows still fail poorly

## High-value durable references

- AdugboInsure positioning: the insurance product comes from OYSHIA; AdugboInsure is the community access, awareness, enrollment, and payment-support channel.
- AdugboInsure opportunity tracking: UNICEF Venture Fund Climate and Health 2026 and Visa Africa FinTech Accelerator Program 6 were already submitted as of `2026-05-08`.
- Orisynx primary repos to monitor: `Orisynx/backend` and `Orisynx/frontend-app` (frontend migrated Next.js→Vite/React on 2026-08-17; old `Orisynx/frontend` and `Audit-IS/fe` are superseded/legacy).
- Orisynx durable docs:
  - `ORISYNX_CONFLICT_RESOLUTION_FRAMEWORK.md`
  - `memory/orisynx.md`
- Orisynx QA baseline from `2026-07-13`: fresh users currently default to backend role `STAKEHOLDER`; `/audit/new` and `/audit-plan/new` silently redirect instead of showing permission denial; `Task Manager`, `CAPA`, and `Documents` can show load-failure states; Calendar `Schedule Events` is still a placeholder; direct fresh visits to public SPA routes like `/login` and `/register` can return `403` on the S3-hosted frontend.
- DOCX durable workflow: use the local `skills/docx-safe/` fork.
- mhGAP/Indigo durable lesson: prefer same-signed versionCode `10` recovery/update builds over more ADB-only extraction attempts.
- Resume/deliverable preference: prefer email for personal files/results and GitHub for project/code/docs when Drive is awkward.
- Email evidence reminder from `2026-08-10`: for anything that may depend on company/regulatory/supporting documents, check the Jarvis Gmail inbox first for prior forwarded materials from Kolade before saying the docs are missing or asking again. Verified examples already present there include the forwarded SCUML submission email for `ORISYNX LIMITED` (RC `RC9422696`, portal status later checked as `PENDING`) and prior company/CAC document emails from Kolade. Do not rely on memory alone; re-check the mailbox first.
- Google Drive access reminder from `2026-08-27`: before asking Kolade to open Chrome or proposing OAuth, check the recovered `gws` refresh-token route first. It is working and supports Drive list/search/download and read/export of supported Google files; it is intentionally read-only (`drive.readonly`, `documents.readonly`) and cannot upload, create, or edit. Config/token live under `~/.config/gws/`; verify with a small `gws drive files list` call when needed.

## Next-step reminders

- Keep OpenClaw config conservative on this server.
- Keep MEMORY concise; move bulky historical material into archive files instead of expanding this file again.
- If Robin responsiveness regresses, inspect queue depth, concurrent worker count, and main-session bootstrap size before rebooting.
- Miro OAuth is configured. Credentials are stored in OpenClaw's persistent owner-only MCP OAuth store, NOT in agent memory. Before asking the user to re-authorize Miro, first check that persistent store and attempt the OAuth refresh flow; only request reauthorization if the stored credential/refresh token is genuinely unavailable, revoked, or invalid. Never save raw OAuth tokens in memory or logs. Recovery instructions: `docs/MIRO_OAUTH_RECOVERY.md`. Store reference: `~/.openclaw/mcp-oauth/miro-5be67c33be9f6d16.json` (owner-only; current OpenClaw MCP OAuth storage is persistent but not encrypted).
