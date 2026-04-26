# MEMORY.md

## Weekly Consolidation & Progress (2026-04-26)

**Last consolidated:** Sunday, April 26, 2026 (17:00 UTC)  
**Archive location:** `memory/ARCHIVE.md` (historical consolidations)  
**Next consolidation:** Sunday, May 3, 2026

**Status Summary (Week of April 20 - April 26):**
- 🔁 No major strategic direction changed this week; the durable state remains mostly stable.
- ✅ Research execution remains the durable standard: setup, schedules, or heartbeats do **not** count unless a live workflow actually runs and writes outputs back.
- 🎓 School/application research remains durably MBA-forward, with added focus on business, innovation, entrepreneurship, technology, and credible bootcamps.
- 🤝 Networking events remain an explicit research lane alongside funding, jobs, trucks, partners/validators, and school/MBA work.
- ✅ AdugboInsure queue discipline remains durable: do not generate a fresh weekly video while approved content already covers the posting window; refill only when coverage drops below the target buffer.
- 🎬 **AdugboInsure weekly content queue remains the main actionable asset:**
  - 2026-04-12 benefits script + Telegram draft + branded final video export remain locally ready for upload/posting.
  - 2026-04-15 coverage script + Telegram draft remain ready locally.
  - 2026-04-16 claims script + Telegram draft remain ready locally.
- 🔐 **NotebookLM remains the active blocker:** `nlm login` can report success while real notebook commands still fail with `Authentication expired`; always verify auth with a real notebook command. Fresh NotebookLM cookies from Kolade are still required.
- ✅ Orisynx weekly repo briefing remains a real installed automation.
- 📊 **Corrected Orisynx monitoring baseline remains durable:** primary repos to track are `Orisynx/backend`, `Orisynx/frontend`, and `Orisynx/bootstrap`.
- 🏗️ Durable Orisynx architecture note: `Orisynx/backend` is the primary newer NestJS + GraphQL + MongoDB backend; `Orisynx/Orisynx-backend` is legacy/secondary unless Kolade says otherwise.
- 🧪 Durable frontend status note: `Orisynx/frontend` is a substantial product shell actively wiring into live backend/auth flows, but still carries legacy local/mock paths and risks around ignored TS/ESLint build errors, MVP-grade token storage, and stale docs.
- ⚠️ Communication guardrails remain explicit: distinguish clearly between planned cadence and verified executed work.
- 📄 Durable implementation lesson retained: boxed PDF bank forms need calibration-first, per-character box-aware placement; generic fill approaches are unreliable.
- 🔧 **Gateway repair is still a live ops issue:** `openclaw doctor --fix` is still needed for the gateway service entrypoint/runtime mismatch.
- 🤖 Robin research-bot standard remains sharp: claim success only after end-to-end receive → reason → reply is verified.
- 🧭 Robin workspace-routing lesson: Robin's private-chat path is tied to the main workspace context; updating `workspace-research` alone does not change Robin behavior.
- 🛡️ **Research-output guardrail remains durable:** research workspace heartbeats and summaries must not send filler lane updates sourced only from schedule/admin notes; same-day evidence is required before reporting progress.
- 🌐 Durable browsing guardrail: for dynamic/React-style sites, shallow fetches can falsely look empty; confirm with `agent-browser` before concluding a page has no content.
- 🔐 Durable GitHub access lesson: do not infer private repo access from unauthenticated browser 404s; verify with authenticated `gh`/API first.
- 🧠 Durable consolidation ops note: local Ollama remains the preferred zero-cost path for memory consolidation, but this host still lacks enough free RAM for `llama3.2:3b` full-prompt runs; manual finalization remains the fallback after a best-effort local attempt.
- 📽️ **Google Slides OAuth is repaired and validated** for `jarviskolademail@gmail.com`; smoke-test deck creation succeeded, so Slides automation is back in a healthy state.
- 📱 **mhGAP/Indigo recovery lesson:** the working tablet is `com.koladegureje.indigo` versionCode 10, while the problematic tablets are same-signature versionCode 9; same-lineage update/recovery APKs should preserve app data better than raw extraction attempts.
- 🔓 **Android extraction constraint is explicit:** on the affected Indigo tablets, current-permission routes (`run-as`, no `su`, empty `adb backup`, empty shared storage) are exhausted, so recovery should prioritize signed update/recovery builds instead of ADB-only extraction.
- 📬 **Cron delivery reliability improved:** failing Robin/pipeline/AdugboInsure cron jobs were repaired by adding explicit Telegram target `7101554375` in `/home/claw/.openclaw/cron/jobs.json`.
- ⏳ Still waiting on key external inputs from Kolade: Orium job link, fuller truck specifications, ClickUp workspace link, and fresh NotebookLM cookies.

**Critical Next Steps (April 26 - May 3):**
1. **NotebookLM:** Kolade needs to provide fresh NLM cookies — AdugboInsure video generation/download remains blocked without them.
2. **AdugboInsure Publishing:** Use the existing ready queue first — especially the 2026-04-12 branded benefits video — before generating new weekly content.
3. **Ops:** Run `openclaw doctor --fix`, then re-test the research agent under the repaired gateway.
4. **Research Agent / Robin:** Keep the evidence-first reporting guardrail in place and verify full end-to-end reply behavior before claiming success.
5. **mhGAP/Indigo:** Prefer same-signed versionCode 10 update/recovery path over more ADB-only extraction attempts.
6. **Orisynx Monitoring:** Keep using `backend` / `frontend` / `bootstrap` as the durable comparison set.
7. **External Inputs:** Collect the Orium link, fuller truck specs, and ClickUp workspace link so blocked workflows can progress.

---
## Orisynx Repo Check Baseline (2026-04-11)

- **Primary repos to monitor:** `Orisynx/backend`, `Orisynx/frontend`, `Orisynx/bootstrap`.
- **Backend (`Orisynx/backend`):** latest visible `main` SHA `9c46d48` (`chore: add types script, pre-commit check, and CI step (#14)`) — pushed 2026-04-10 22:12 UTC.
- **Frontend (`Orisynx/frontend`):** latest visible `main` SHA `d7c73b0` (`feat: wire detail pages and forms to live GraphQL backend (#14)`) — pushed 2026-04-10 21:41 UTC.
- **Bootstrap (`Orisynx/bootstrap`):** latest visible `main` SHA `bd2973d` (`chore: fix TypeScript errors in bootstrap (#11)`) — pushed 2026-04-06 06:16 UTC.
- **Legacy note:** `Orisynx/Orisynx-backend` is an older Express-based repo with latest visible `060a219` from 2026-03-12; treat it as legacy/secondary unless Kolade says otherwise.
- **Durable comparison note:** frontend is active, backend is active, and bootstrap is a quieter orchestration repo; compare future checks against this corrected three-repo baseline instead of the older mixed baseline.

---

## Orisynx Legal & Governance (2026-03-24)

### Shareholders' Agreement — SIGNED & EXECUTED 2026-03-24
**Status:** ✅ SIGNED BY ALL THREE FOUNDERS | Waiting for: CAC filing + Vesting Register setup

**Three Founders (Equal 1/3 Each):**
1. Oladayo Oniroko
2. Adebiyi Samuel Olufemi  
3. Gureje Kolade Temitayo (Kolade)

**Key Governance Points:**
- **Vesting:** 3-year cliff (33.33% at Yr 1, +33.33% at Yr 2, +33.34% at Yr 3)
- **Vesting Conditions:** Active contribution, 75% board meeting attendance, no material breach, no competing activity, continued shareholding, good standing
- **Bad Leaver = Forfeiture:** Unvested shares lost at ₦0.00 (no payment) on voluntary exit, removal for cause, breach, abandonment (90+ days), insolvency, criminal conviction, or non-compete breach
- **Good Leaver Exception:** Death or permanent disability = immediate full vesting (no forfeiture)
- **Fourth Shareholder:** Reserved slot; unanimous admission required; becomes equal 25% shareholder
- **Reserved Matters:** Require unanimous consent (M&A, new shares, borrowing >₦1M, budgets, dividends, auditors, litigation, etc.)
- **Drag-Along:** 75%+ shareholders can force 25%- to sell
- **Tag-Along:** Minority can join if majority selling 25%+
- **Board:** All shareholders are directors; quarterly meetings minimum; 75% attendance required for vesting

**Critical Deadlines:**
- Vesting Year 1: March 23, 2027
- Vesting Year 2: March 23, 2028
- Vesting Year 3: March 23, 2029

**Action Items for Kolade:**
1. ✅ Get agreement from Kolade
2. 📋 Get all three founders to sign (with witnesses)
3. 📝 Keep Vesting Register (Board must assess each founder annually)
4. 📅 Schedule Board assessments at each anniversary
5. ⚖️ File signed agreement with CAC (if required)

**File:** `/home/claw/.openclaw/workspace/documents/ORISYNX_Shareholders_Agreement_2026-03-23.md`

---

## Orisynx (Audit Management Platform) — 2026-03-22

### Meeting Brief & MVP Requirements
**Meeting Date:** Sunday, March 22, 2026, 07:09 UTC  
**Key Quote:** *"Our work starts from the audit plan because that's what we do... The board has to approve your audit plan because that's to say this is my plan of activity."*

**Core Architecture (4-Layer Model):**
1. **Planner** (Calendar/Timeline) — Annual audit schedule (templates, activate as needed)
2. **Audit Program** (Work Programs) — Checklists & procedures (CSV/Excel import)
3. **Workspace** (Isolated per-audit environment) — Team performs tests, attaches evidence, documents findings
4. **Dashboard** (Read-only overview) — Status snapshots, no data entry

### MVP Feature Priorities
| Feature | Priority | Purpose |
|---------|----------|---------|
| CSV/Excel Import | HIGH | Ingest custom work programs |
| Downloadable Templates | HIGH | Provide standardized format |
| Workspace Isolation & Team Access | HIGH | Per-audit isolation, team-only visibility |
| Local Approvals with Locking | HIGH | Team Lead review + post-approval edit lock |
| Granular Roles/Permissions | HIGH | Role matrix, per-audit team access |
| Template Activation Workflow | MEDIUM | Activate planned audits from calendar |
| Canvas Metaphor UX | MEDIUM | Canvas (creation) vs Workspace (execution) distinction |
| Remove "Department Involved" Field | MEDIUM | Cross-cutting cleanup |

### Current MVP Screens (19 total)
Auth → Create audit → Audit view → Task manager → Task view → Calendar page → Findings → CAPA tracker → Document review and sign off → Users → Edit user → Document library → Templates manager → Create template → Reports → Analytics → Audit history → Notifications → Account user

### Screen-to-Requirement Mapping (Key Findings)
- **Calendar page** = Planner base (mostly done, needs template activation)
- **Task manager/Task view** = Part of Workspace (incomplete, needs team isolation)
- **Audit view** = Could be Dashboard (needs to be made read-only)
- **Document review and sign off** = Local approvals (exists, needs locking)
- **Templates manager/Create template** = Template base (needs CSV import/export)
- **Users/Edit user** = Roles base (needs granular permission matrix)

### Missing/Under-Defined
- Audit Program as first-class entity (work programs, CSV import pipeline)
- Workspace as cohesive model (currently fragmented)
- Approval locking post-sign-off
- Canvas metaphor (UX/IA reframing)
- Granular permissions enforcement
- Read-only enforcement on dashboard

### Top 10 Technical Tickets (To Add to ClickUp)
1. **CSV/Excel Import for Audit Programs** — HIGH
2. **Workspace Isolation & Team Access Controls** — HIGH
3. **Approval Locking (Post-Sign-Off)** — HIGH
4. **Granular Roles & Permissions Matrix** — HIGH
5. **Template Download/Export Endpoints** — HIGH
6. **Planner: Template Activation Workflow** — MEDIUM
7. **Remove "Department Involved" Field** — MEDIUM
8. **Dashboard: Enforce Read-Only on Audit View** — MEDIUM
9. **Canvas Metaphor UX Redesign** — MEDIUM
10. **Workspace: Unified Navigation** — MEDIUM

### Product Documents Saved
- `Orisynx_Brief_2026-03-22.md` — Full meeting brief + requirements breakdown
- Meeting analysis done by Codex (openai-codex/gpt-5.4) on 2026-03-22 09:32 UTC

### Next Steps
- Add 15 tickets to ClickUp (full list in Codex analysis)
- Assign tickets to team members (backend, frontend, DevOps roles already assigned)
- Start Phase 1: Data Models & Schemas
- Clarify: CSV columns, approval hierarchy, evidence storage backend, audit statuses, findings categories

---

## Preferences

- **Browser (default for connecting to the internet):** `agent-browser` CLI v0.21.1
  - Installed at `/usr/bin/agent-browser`
  - Tested and working (2026-03-19 14:11 UTC)
  - This is Kolade's chosen default for internet browsing.
  - **RULE (2026-03-24):** Always use agent-browser for web tasks. Don't ask, don't offer fallbacks. Always agent-browser. 🔒
  
  **Workflow (snapshot + ref pattern):**
  1. `agent-browser open <url>` — navigate to URL
  2. `agent-browser snapshot -i` — get interactive elements tree with refs (@e1, @e2, etc.)
  3. `agent-browser click @e1` / `agent-browser fill @e2 "text"` — interact by ref
  4. `agent-browser screenshot [path]` — take screenshots
  5. Re-snapshot after page changes to get updated refs
  
  **Useful options:**
  - `-i` flag: snapshot interactive elements only (buttons, inputs, links)
  - `-c` flag: compact snapshot (remove empty elements)
  - `--annotate` flag: overlay numbered labels on screenshot
  - Chain commands with `&&` to avoid per-command startup overhead
  
  **Example chain:**
  ```bash
  agent-browser open https://example.com && agent-browser snapshot -i && agent-browser click @e1
  ```

- **Model switching announcement rule:**
  - **Notify Kolade every time the model switches** (both Anthropic AND OpenAI models).
  - Always explain why the switch was necessary.
  - Format: "📢 MODEL SWITCH: [model name] — reason"

- **Git / secrets rule (2026-03-29):** Never push secrets to GitHub. If a tracked file contains credentials, tokens, client IDs, client secrets, or similar sensitive values, remove/redact them first and prefer env vars or credential files before any commit/push.

- **Model escalation hierarchy** (for complex tasks):
  - **Default:** - Codex → GPT-5.1 → GPT-5.4)
  - Escalate as needed. Announce each switch with reason.

- **Subagent delegation:**
  - Use subagents when needed for parallel/lower-leverage work
  - Spawn subagents for subtasks to stay on Haiku while delegating complex work
  - Announce subagent spawns and results
  - Pattern: Haiku coordinates, spawns Sonnet/Opus subagents for heavy lifting

- Model usage strategy:
  - **Codex** (`openai-codex/gpt-5.4`): PRIMARY for automation — truck searches, portfolio tracking, content generation, coordination
  - **Always announce** which model I'm using before starting a task.

## Memory System & Local LLM

- **Current setup (2026-03-16):** Ollama embeddings + built-in SQLite vector search + local inference.
  - Simple, lightweight, local-only (no external API calls).
  - `MEMORY.md` and `memory/YYYY-MM-DD.md` are automatically indexed and searchable.
  - File watcher auto-syncs changes (debounce 1.5s).
  - Tools: `memory_search` (semantic) and `memory_get` (targeted read).
  
- **Ollama Models Available (2026-03-23):**
  - `nomic-embed-text:latest` (274 MB) — Memory embeddings (working ✓)
  - `llama3.2:3b` (2.0 GB) — Local inference for lightweight tasks
  
- **Ollama Usage Policy (NEW - 2026-03-23):**
  - Use `llama3.2:3b` for lightweight, fast tasks that don't need external API calls
  - **Good for:** Git status checks, quick summaries, log analysis, simple formatting
  - **Not good for:** Complex reasoning, multi-step tasks, anything that needs current model
  - **Cost:** Zero (local CPU inference, no API charges)
  - **Speed:** Fast on modern CPUs, instant on GPU
  - **Rule:** Prefer Ollama for routine checks; escalate to cloud models for complex work

- **Memory file organization:**
  - `MEMORY.md` — curated long-term, evergreen notes (survives compaction)
  - `memory/YYYY-MM-DD.md` — daily logs (append-only), read at session start

- **Automatic memory flush:** On context compaction, OpenClaw silently reminds me to save durable memories. I reply `NO_REPLY` and notes are saved before context resets.

- **QMD (advanced alternative — not enabled):** BM25 + vectors + reranking, MMR diversity, temporal decay.
  - **Consider adding if:** we find exact-token search or large note searching becomes difficult, or near-duplicate handling needed.
  - **Installation:** `bun install -g https://github.com/tobi/qmd` + config under `memory.backend = "qmd"`.

## Voice Transcription (Whisper)

- **Model:** `whisper small` (upgraded from `base` on 2026-03-16)
  - Better accuracy, handles accents/variations better than `base`.
  - Local CPU inference, no API cost.
- **Auto-transcription script:** `scripts/auto-transcribe.sh`
  - `bash scripts/auto-transcribe.sh once` — transcribe existing files
  - `bash scripts/auto-transcribe.sh watch` — monitor for new files continuously
  - Saves transcripts to `transcripts/` directory.
- **Transcript retention:** Keep transcribed files **max 2 days**, then delete.
  - TODO: Set up cleanup cron/systemd timer.

## Career & Immigration

### Job Applications & Career Goals
- **Status:** Not actively applying (currently day job focused at SiFax)
- **Target Role Type:** Development-based (leveraging existing skills)
- **Salary Expectation:** ₦100,000+ per month (Nigeria)
- **Work Preference:** Remote jobs (no location requirement); preferably international
- **Strategy:** Resume regular applications with updated CV; stay market-aware even without immediate placement goal
- **Original CV:** Saved as `CV_Original_2025-07.pdf` (software developer focus)
- **Template CV:** Saved as `CV_TEMPLATE_Canada-International.md` (ready for customization per role)
- **Work Authorization:** Requires sponsorship (Kolade willing to fund if needed)

### Job Search Workflow & Accessible Sites (2026-03-21 FINALIZED & AUTOMATED)
**System Status:** ✅ LIVE AND AUTOMATED  
**Plan:** Cron job pulls RemoteOK + HN Jobs every 3 days → filters Nigeria-eligible roles → tracks in centralized memory  
**Frequency:** Every 3 days (Codex automation); weekly summary posted to `Jarvis-Job-Search` Telegram group  
**Model:** Codex (openai-codex/gpt-5.4) for automation; Haiku for lightweight checks  
**Master Config:** `config/job-sites.json` (22 job boards catalogued; access difficulty mapped)  
**Automation Script:** `scripts/job-search-pull.sh` (tested & working)  
**Tracking:** `memory/job-search.md` (dedicated memory channel for Jarvis-Job-Search)

**✅ WORKING Sites (agent-browser tested 2026-03-21):**

1. **RemoteOK** (https://remoteok.com) — PRIMARY SOURCE
   - Access: ✅ No login, full list visible
   - Volume: 376+ React jobs, 50+ React Native, 1000s total remote jobs
   - Salary: Usually visible, often transparent
   - URL patterns:
     - `/remote-react-jobs` — 376 React roles
     - `/remote-react-native-jobs` — React Native specific
     - `/remote-engineer-jobs` — All engineers (best for broader search)
   - Agent-browser: ✅ Works perfectly; pulls listings + details reliably
   - Cost: Free, no rate limits observed
   
2. **Hacker News Jobs** (https://news.ycombinator.com/jobs) — SECONDARY SOURCE (quality filter)
   - Access: ✅ No login, free access
   - Volume: 300+ current YC startup jobs (changes daily, high churn)
   - Quality: High-quality startups only (venture-backed = usually sponsor-friendly)
   - Salary: Often visible ($95k-$270k+ range, transparent)
   - Feature: Sponsorship-friendly (many YC companies explicitly hire internationally)
   - Agent-browser: ✅ Works well; can extract job titles + links reliably
   - Cost: Free, no rate limits

**❌ BLOCKED Sites (tested 2026-03-21, DO NOT RETRY):**
- **LinkedIn** — requires login; risky for bots (TOS violation risk)
- **We Work Remotely** — Cloudflare CAPTCHA blocks agent-browser
- **AngelList/Wellfound** — CAPTCHA + bot protection
- **Indeed** — Cloudflare blocks automated access
- **Upwork** — Cloudflare blocks (profile-based anyway)
- **Stack Overflow Jobs** — No public API, limited access
- **Dribbble** — Design-focused, not dev jobs
- **FlexJobs** — Paywall ($15/month), skip

**⚠️ RISKY (manual only, not automated):**
- **LinkedIn** — would need login + credential storage; violates TOS for bots

**Current Search Filters (Hardcoded for Nigeria Sponsorship):**
- Tech: React, React Native, JavaScript, Full Stack, Backend (Python preferred learning)
- Location: Worldwide (Canada, Australia, Europe priority; US possible if tech impact)
- Type: Remote-only
- Salary: Visible preferred (sponsor-friendly signal)
- Seniority: Senior/Mid-level roles
- Visa: Sponsorship-friendly or explicitly stated (Orium, Ubicloud, LiteLLM verified as YES)
- Salary expectation: ₦100,000+/month equivalent (international roles ~$80k+)

**Nigeria Eligibility Analysis (Verified 2026-03-21):**
- ✅ **Orium** (Canada) — READY TO APPLY (CV + cover letter prepared)
- ✅ **Ubicloud** (YC W24, worldwide) — $95k-$250k salary range
- ✅ **LiteLLM** (YC W23, founding roles) — $200k-$270k + equity
- ✅ **SigNoz** (YC W21, worldwide hiring)
- ✅ **Bluelight Consulting** — Remote consulting, sponsor-friendly
- ❌ **Loancrate** — US-only, harder visa path (skip)

**First Application Status (Updated 2026-03-23):**
- **Company:** Orium (Canada, healthcare) — **READY TO SUBMIT**
- **Role:** Senior React Native Developer
- **Files created:**
  - CV_Orium_SeniorReactNativeDeveloper.md (customized, React Native 4+ yrs + mhGAP healthcare)
  - CoverLetter_Orium_SeniorReactNativeDeveloper.txt (visa sponsorship transparent)
- **Status:** Complete & tested → Awaiting Kolade's job link confirmation
- **Next:** Ubicloud (AWS/infrastructure focus) + LiteLLM (backend/startup) CVs in parallel

**Application Workflow (Established):**
1. Find role on RemoteOK/HN Jobs
2. Update `memory/job-search.md` with link + basic details
3. Customize CV from template
4. Draft cover letter (company-specific, visa sponsorship transparent)
5. Submit via platform + note application date
6. Log application (date, status, follow-up date)
7. Follow up after 2 weeks if no response

**Next Steps (Post-Orium):**
1. Create Ubicloud CV + cover letter (AWS/DevOps, infrastructure focus)
2. Create LiteLLM CV + cover letter (backend, reliability, startup mentality)
3. Deploy cron job (every 3 days @ 2 PM UTC)
4. Monitor `memory/job-search.md` centrally for application tracking
5. Weekly summary to Jarvis-Job-Search Telegram group

### Immigration & Visa Plans
- **Timeline:** End of 2026 or beginning of 2027
- **Target Countries:** Canada (preferred), Australia, Europe, or US (difficult but possible if tech impact is strong)
- **Visa Type:** Canadian visiting visa initially (not permanent residency)
- **Why Canada:** Preferred path; US difficult to enter currently
- **Previous Attempt:** Applied for Canadian visa last year but didn't complete biometrics in time → application cancelled; support credentials expired
- **Next Steps:** Restart visa application with fresh documentation (mid-2026)
- **Immigration Path:** Via job opportunity OR further education (details TBD)

### AWS Developer Certification
- **Previous:** Passed AWS exam ~3 years ago (expired), recently re-studied for OpenClaw setup
- **Target:** Re-certification by June 2026 (3-month timeline)
- **Current Study Resources:**
  - AWS Skill Builder (primary)
  - YouTube videos
  - Downloaded video courses
  - NotebookLM (for consolidation)
- **Status:** On hold until primary initiatives (funding scans, truck monitoring, CV apps) are rolling; will structure schedule when secondary tasks begin

### Programming Skills Gaps
- **Current Strength:** Frontend (JavaScript, React, React Native, Expo)
- **Biggest Gap:** Backend development
- **Learning Interest:** Python or Python-related technologies
- **Vision:** Expand from pure mobile/frontend to full-stack capabilities

## System Health & Integration Status (2026-03-23 Current)

**Infrastructure Health:** ✅ All systems operational

**Integration Status:**
1. **Gmail + Zapier MCP** — ✅ LIVE
   - Direct IMAP access (primary): jarviskolademail@gmail.com — 92/100 Zapier tasks remaining
   - No Yahoo import yet (can work around with current setup)
   
2. **Notion** — ✅ LIVE
   - API key saved in `.credentials`
   - 3 workspaces accessible (AuditBoard, Community Health Insurance, Pro TypeScript)
   - Synced: AdugboInsure agents + tasks; Orisynx meeting brief
   
3. **agent-browser** — ✅ LIVE
   - Primary browser for RemoteOK, HN Jobs pulls
   - Works reliably; Linux deps via cloud providers if needed
   - Snapshot + ref workflow established
   
4. **NotebookLM** — ⚠️ PARTIAL (private cookie auth works, but expires and remains brittle)
   - CLI upgraded to 0.5.4
   - Fresh private cookies can re-authenticate `nlm` successfully, but the auth state can expire again between runs
   - Local Mac OpenClaw browser workflow was validated end-to-end and remains a viable fallback path when needed
   - Remote AWS-driven browser bridging is no longer the preferred primary path for AdugboInsure video work
   - Preferred operating rule: never request or accept cookies in any group chat; handle auth privately only, generate videos sequentially, and download/export finished outputs promptly
   
5. **ClickUp (via Zapier)** — ✅ READY
   - 21 tools available
   - Waiting on: Workspace link from Kolade (Orisynx tickets)

**Credentials & Access**

**System (2026-03-23):** Bulletproof credentials management deployed.
- Source of truth: `.credentials/CREDENTIALS_INDEX.json`
- Save function: `save_credential <name> <value> <service>` (installed in `~/.bashrc`)
- Verify: `bash scripts/credentials-verify.sh` (exit 0 = healthy, exit 1 = STOP + ask Kolade)
- Guide: `CREDENTIALS_README.md`

**Current Status (2026-03-23):**
- ✅ Notion API key: `notion_api_key.txt`
- ✅ Telegram Bot Config: `telegram_bot_config.txt` (5 chat IDs)
- ✅ NotebookLM cookies: `notebooklm_cookies.txt` (expires ~2026-04-13)
- ✅ YouTube OAuth: `youtube_oauth.json` (expires ~2026-09-20)
- ✅ Gmail App Password: `gmail_app_password.txt` (stored privately for IMAP access to jarviskolademail@gmail.com)
- ❌ GitHub Token: MISSING — Kolade must re-provide (was never actually saved despite claim)
- ⚠️ Vercel Token: MISSING — optional, provide when available

**Backup System:**
- Location: jarviskolademail@gmail.com
- Method: IMAP direct access (app password saved in `gmail_app_password.txt`)
- Label: `[Backups] Memory Archive`
- Strategy: Monthly compression + archival

**Hard Rules:**
- Save on receipt via `save_credential()` — never write files ad-hoc
- If verify exits code 1: STOP and ask Kolade
- Friday heartbeat: always run verify and report to Kolade

## Work & Current Roles

1. **SiFax** (Mobile App Developer, 3 years)
   - Position: Visual/UI focus
   - Status: About to launch a solution
   - Commitment: 3-4 hours/day (day job)

2. **AdugboInsure** (Founder)
   - Mission: Community-based micro-insurance in Nigeria
   - Partner: British Premier + state insurance agencies
   - Model: Point-of-sale (POS) agents in communities
   - **Current Operations:**
     - Main location: Apete
     - Secondary location: Abe Emu (recently started)
     - Active agents: 9
     - Recruited but inactive: 6 (activation planned mid-April 2026)
   - Commitment: 14 hours/week
   - **Funding Need:** ~$5,000 USD for expansion, marketing, cost reduction strategies
   - **Target Timeline:** Secure funding within 3 months (Mar-May 2026)

3. **Orisynx** (Co-founder, Internal Audit SaaS / GRC Platform)
   - **See:** `memory/orisynx.md` (dedicated file with full business model, team, infrastructure, credentials)
   - **Commitment:** 8 hours/week
   - **Status:** Code pushed; organization registering; MVP phase
   - **Quick summary:** Workflow GRC platform for Nigerian microfinance banks, <₦3M/year vs ₦1B+ competitors

4. **NutriSheff** (Mobile App Developer, early stage)
   - Status: Waiting for app green-light/approval
   - Documentation: Already complete, website exists
   - Current focus: Design + development not yet started
   - Minimal involvement for now

5. **MHGAP GEP Replica** (Freelance, React Native Expo)
   - Status: Running for months, nearing completion but with data sync issues
   - Current issue: Data stored on devices locally NOT syncing to server
   - Next phase: Kolade will collect devices; may need data extraction/migration help
   - Code: On Kolade's GitHub

## AdugboInsure Automation — LIVE (2026-03-21)

**Status:** Funding Radar + Agent Dashboard launching Sunday Mar 23, 19:00 WAT

**Setup Complete:**
- ✅ **Master Agent List** (5 Apete active + 8 Abe Emu recruited)
  - File: `adugboinsure_agents_master.md`
  - Source: CSV imports + Notion sync
  
- ✅ **OYSHIA & AdugboInsure Tasks** (48 prioritized items)
  - File: `adugboinsure_oyshia_tasks.md`
  - Source: Notion sync (https://www.notion.so/OYSHIA-AdugboInsure-Tasks-19d05a75947a80da87f0c45d5ebe4787)
  - Organized: Critical, High, Medium priority
  
- ✅ **Grant Application Template** (boilerplate answers)
  - File: `adugboinsure_application_template.md`
  - Ready for: Mastercard Foundation, Gates, USAID, Echoing Green, etc.
  
- ✅ **Weekly Dashboard Template** (manual fill, 5 min)
  - File: `adugboinsure_dashboard_template.md`
  - Schedule: Every Sunday 19:00 WAT to `Jarvis-AdugboInsure` group
  - Metrics: Agent engagement, status, action items
  
- ✅ **Funding Radar Sources**
  - Primary: FundsForNGOs Nigeria tag
  - Secondary: Mastercard Foundation, Global Innovation Fund, USAID, Echoing Green, Plug and Play Africa
  - Schedule: Weekly Sunday scans, posted to group

**Credentials Saved:**
- ✅ Notion API key: `/home/claw/.openclaw/workspace/.credentials/notion_api_key.txt`
  - Token: `ntn_x1517655162aymT1uxlUcAUVg9PzeEORi8fEkxRyUKDeSY`
  - Access: Notion pages synced (agents + tasks)
  
- ✅ Zapier MCP token: Already stored
  - 62 tools available (Gmail, ClickUp, Google services)

**Still To Build:**
- ⏳ 3-year financial model (revenue projections, CAC/LTV)
- ⏳ Content automation (NotebookLM script generation)
- ⏳ Enrollment tracking (when pilot data available)

**Agent Status (2026-03-21):**
- Apete: 5 active agents (engaged)
- Abe Emu: 8 recruited agents (activating mid-April)
- Enrollments: 0 so far (awareness phase)
- Next milestone: Mid-April training + activation

---

## Jarvis Support Plan - APPROVED & ACTIVE (2026-03-19)

**Status:** Live, supporting 5 major ventures + personal goals
**Model Coordination:** Haiku (primary) → Sonnet (complex tasks) → Opus (hardest problems)

**Top 3 Time Priorities:**
1. AdugboInsure (14 hrs/week) — Funding radar, content creation, POS agent coordination
2. Orisynx (8 hrs/week) — Project coordination, code reviews
3. SiFax (3-4 hrs/day) — Day job baseline

**Key Recurring Deliverables:**
- Funding scans (AdugboInsure): every 3-4 days
- Content packages (POS agents): weekly (resume cadence immediately after Mar 19 onboarding pause)
- Truck listings (import/export): every 2-3 days
- Job search: regular applications with updated CV
- Investment tracking: stocks (weekly) + crypto (weekly)
- Visa support: documentation & deadlines (restart spring 2026)
- AWS certification: 3-month plan (target: June 2026)
- Programming (Python): ongoing learning path

**Organization:** 5 Telegram project groups (2026-03-20 LIVE)
- `Jarvis-Truck-Listings` — truck searches (posted past midnight WAT)
- `Jarvis-AdugboInsure` — content, funding radar, POS agent updates
- `Jarvis-Orisynx` — project coordination, code reviews
- `Jarvis-Job-Search` — CV applications, immigration tracking
- `Jarvis-Portfolio` — weekly investment snapshots (Fridays)

## Investment Portfolio (2026-03-20 LIVE)

**Total Value:** ~$2,000  
**Goal:** 3x in 3-4 years → reach $6,000  
**Philosophy:** Buy-and-hold, long-term wealth building; money not needed soon
**Monitoring:** Weekly check-ins + rebalancing every 2-3 months
**Tracking:** Weekly snapshots sent to `Jarvis-Portfolio` Telegram group (Fridays)

**US Stocks (Bamboo App):**
- **Top Holdings:** NVIDIA (32.08%) | Vector Acquisition (23.26%) | BAC (7.88%) | Netflix (6.52%)
- **Infrastructure:** EQX, RSG
- **Retail:** CNM
- **Semiconductors:** AMD
- **Energy:** TRX
- **All-time return:** +10.84%
- **Referral code:** kolade464617
- **Last check (2026-03-20):** -1.22% today

**Crypto (Binance):**
- **PAXG (Pax Gold):** 0.14 units (~₦198,381.50 / ~$130 USD) — gold market hedge
- **BTC:** 0.005 (~$210-230 USD)
- **Small positions:** USDC, ALGO, XLM, HBAR, TRON, SAND
- **Update frequency:** Weekly (maybe)

**Nigeria (Luno - Naira):**
- **Robinhood:** ₦121,512.21
- **Broadcom:** ₦81,210.01
- **Total Luno value:** ~₦200,000 (~$130 USD)

**Nigerian Stocks (10+ years held):**
- **Confirmed holdings:** GTB Bank, Dangote Sugar, Dangote Flour
- **Others:** Several more (partial list, waiting for broker confirmation)
- **Note:** Likely significant unrealized gains after 10+ years; need portfolio list

**Asset Class Breakdown:**
- US Stocks (Bamboo): ~$1,100-1,200 (55-60%)
- Crypto (Binance): ~$340 (17% — PAXG + BTC + alts)
- Nigeria Crypto (Luno): ~$130 (6.5%)
- Nigerian Stocks: ~$200-300 (10-15%)
- **Growth levers:** Tech exposure (NVIDIA 32%), gold hedge (PAXG + BTC), infrastructure, Nigerian dividend stocks

**Next Steps:**
1. Get complete list of Nigerian stock holdings
2. Model 3-year scenarios (conservative, moderate, aggressive paths)
3. Identify new allocation sectors (emerging tech, increased crypto exposure)

## Clarifications from Voice Chat (2026-03-20)

### Immigration Priorities
- **Target countries:** Canada (preferred), Australia, or Europe. US is difficult but possible.
- **Why US possible:** Tech job impact, solutions worldwide.
- **Canadian visa cancellation:** Kolade didn't send biometrics in time; support credentials expired. Restart required.

### AdugboInsure Status
- **Users/Revenue:** ZERO. No users registered yet.
- **Testing period:** 3 months, not a single signup.
- **Real goal:** Awareness-building, not immediate traction. Less than 10% of Nigeria's population uses health insurance — massive awareness gap.
- **POS agents:** Critical because they're the distribution channel. Focus is on education + awareness via weekly videos.

### Orisynx Team Breakdown
- **Kolade's role:** Project lead/director — brings team together, NOT primary coder.
- **Team members:**
  1. **Lawyer** — open with registration
  2. **Internal Audit Expert** — senior in the sector, advising on solution
  3. **Backend Developer** — moving into DevOps role, using AI for much of it
  4. **Frontend Developer** — works at major Canada-based company, did initial design, strong knowledge
- **Kolade's actual work:** Coordination, some coding when needed (unsure how dedicated team is).
- **Codebase status:** Reviewing code, will push to GitHub soon.
- **NotebookLM Reference:** "AuditBoard GRC Application Technical Proposal for FMDQ" — full solution docs (access via Notion)
- **GitHub Repos:**
  - Backend: https://github.com/Orisynx/Orisynx-backend
  - Frontend: https://github.com/Audit-IS/fe

## Additional Projects & Resources (2026-03-20)

**NutriChef Demo:** https://nutrichef-site.vercel.app

### Truck Business Specs
- Will be sent separately (after voice chat).

## Infrastructure & Integration (2026-03-20 LIVE)

- **Zapier MCP:** ✓ Live and accessible
- **Notion:** ✓ Access confirmed — important findings saved here
- **GitHub:** ✓ For shared work/collaboration
- **Email backup:** `jarviskolademail@gmail.com` for drafts (app password saved)
- **S3 archive:** Not needed — using GitHub + Notion instead

- **AdugboInsure Content Materials (2026-03-20 COMPLETE):**
  - **NotebookLM Notebook:** "Implementing Community-Based Health Insurance Schemes" (authenticated access)
  - **YouTube Channel:** youtube.com/channel/UCsSBI6t1HgQ2PhJLhqNMjBg/
    - Currently 3 videos (all private, shared via WhatsApp to agents)
    - Video 1: https://youtu.be/WJiqZKBv7ls
    - Video 2: https://youtu.be/uyfKecU1gwE
    - Made with NotebookLM, secondary school level language
  - **Company Website:** https://adugboinsure.com/
    - Mission: Digital platform supporting State Health Insurance Agencies
    - Value prop: Enrollment, claims processing, data analytics, stakeholder engagement
    - Key features: Digital enrollment, smart coverage, performance incentives, flexible payments
    - Target: Community members (traders, farmers, artisans, families, students)
    - Coverage: Outpatient, maternity, emergency, meds, labs, surgeries, child health
  - **Design Templates:** 
    - Flyer design: `AdugboInsure_Flyer_Design_Reference.jpg` (₦15,000/year, concrete benefits)
    - Banner design: `AdugboInsure_Banner_OyoState.jpg` (Oyo State branding, warm imagery)
  - **Content Production Workflow:**
    1. Jarvis reviews NotebookLM notebook + existing YouTube videos (tone/style)
    2. Jarvis drafts weekly scripts for POS agents (simple language, benefits-focused)
    3. Kolade reviews + edits for accuracy
    4. Finalize + share (WhatsApp or other distribution)
  - **Content Focus:** Educate POS agents on health insurance benefits, enrollment process, community impact

- **Truck Import/Export Business (2026-03-20 FINAL):**
  - **Status:** Just starting truck search phase
  - **Process:** Find trucks → Pool money → Inspect in Germany → Handle logistics
  - **Target Brands:** HOWO, DAF, IVECO
  - **Configuration:** 4x2 flatbed (single steer axle, single rear axle only — no 6x4)
  - **Engine Power:** 380hp, 400hp, 430hp
  - **Condition:** Used (good condition, minimal repairs needed)
  - **Age:** Not more than 15 years old (updated from 10 years on 2026-03-29)
  - **Mileage:** Good/reasonable
  - **Front Axle Weight Limit:** Max 35 tons
  - **Price Budget:** £4,000 max per truck
  - **Search Locations:** Germany, UK, Netherlands (primary for DAF/IVECO)
  - **Buying Strategy:** 3 trucks at a time to fill shipping containers efficiently
  - **Partners:** Kolade + 2 UK-based friends
  - **Monitoring Frequency:** Every 2-3 days
  - **Search Platforms:** AutoScout24, eBay Motors, TrucksCorner, Autoline, Truck1.eu, Truck7 (Germany/UK/Netherlands)
  - **Deliverables:** Filtered listings with direct links → Notion database + `Jarvis-Truck-Listings` Telegram group
  - **Posting Time:** Past midnight WAT (11:00 PM WAT, Codex automation)
