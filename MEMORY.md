# MEMORY.md

## Preferences

- **Browser (default for connecting to the internet):** `agent-browser` CLI v0.21.1
  - Installed at `/usr/bin/agent-browser`
  - Tested and working (2026-03-19 14:11 UTC)
  - This is Kolade's chosen default for internet browsing.
  
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

- Model preference schedule (timezone: Africa/Lagos):
  - **ACTIVE OVERRIDE (Mar 19, 2026 ~14:22 UTC): Use Sonnet for Kolade's brain dump session**
  - After brain dump: resume regular schedule
  - Regular schedule:
    - Use `anthropic/claude-haiku-4-5` on weekends.
    - Use `anthropic/claude-haiku-4-5` on weekdays from 7:00 PM to 12:00 AM (midnight).
    - Outside those times, use OpenAI/Codex model.

- **Model switching announcement rule:**
  - **Notify Kolade every time the model switches** (both Anthropic AND OpenAI models).
  - Always explain why the switch was necessary.
  - Format: "📢 MODEL SWITCH: [model name] — reason"

- **Model escalation hierarchy** (for complex tasks):
  - **Default:** Haiku (lightweight, cost-efficient)
  - **If task is moderately complex:** Switch to **Sonnet** (`anthropic/claude-sonnet-4-6`)
  - **If task is very complex/needs best reasoning:** Switch to **Opus** (`anthropic/claude-opus-4-6`)
  - For OpenAI: escalate similarly (Codex → GPT-5.1 → GPT-5.4)
  - Escalate as needed. Announce each switch with reason.

- **Subagent delegation:**
  - Use subagents when needed for parallel/lower-leverage work
  - Spawn subagents for subtasks to stay on Haiku while delegating complex work
  - Announce subagent spawns and results
  - Pattern: Haiku coordinates, spawns Sonnet/Opus subagents for heavy lifting

- Model usage strategy:
  - **Opus** (`anthropic/claude-opus-4-6`): PAUSED — Anthropic at 85% limit (2026-03-20)
  - **Codex** (`openai-codex/gpt-5.4`): PRIMARY for automation — truck searches, portfolio tracking, content generation, coordination
  - **Haiku** (`anthropic/claude-haiku-4-5`): Lightweight checks only (git status, quick summaries)
  - **Always announce** which model I'm using before starting a task.

## Memory System

- **Current setup (2026-03-16):** Ollama embeddings + built-in SQLite vector search.
  - Simple, lightweight, local-only (no external API calls).
  - `MEMORY.md` and `memory/YYYY-MM-DD.md` are automatically indexed and searchable.
  - File watcher auto-syncs changes (debounce 1.5s).
  - Tools: `memory_search` (semantic) and `memory_get` (targeted read).

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

## Credentials & Access

**Secure storage:** 
- `/home/claw/.openclaw/workspace/.credentials` — API keys and tokens
- `/home/claw/.openclaw/workspace/.google-drive-sa.json` — Google Drive service account (archived, not used)

**Backup System (2026-03-18):**
- **Location:** jarviskolademail@gmail.com
- **Method:** IMAP direct access
- **Label:** `[Backups] Memory Archive`
- **Strategy:** Monthly compression + archival of memory files
- **IMAP account:** jarviskolademail@gmail.com
  - App Password: `urun qvjm dfad xlwk`
  - Full IMAP access configured

**Credentials saved (2026-03-18):**
- GitHub token: Stored in `.credentials` (Read + Write scope)
  - Scopes: repo (read/write), gist, workflow
- Vercel token: Stored in `.credentials`
  - Allows: view deployments, manage deployments, create new deployments

**Rule:** Every credential Kolade sends me MUST be saved in `.credentials` file. Never commit tokens to GitHub.

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
   - Status: Currently registering as organization
   - Team: 4 members (lawyer, internal audit expert, backend dev, frontend dev)
   - Solution: Internal audit software for organizations to conduct audits
   - Kolade's role: Project lead/director (brings team together, not primary coder)
   - Documentation: AuditBoard GRC Application Technical Proposal (in Notion)
   - Project Management: ClickUp
   - Codebase: Frontend + backend on GitHub (will be pushed soon)
   - Commitment: 8 hours/week
   - Current work: Reviewing code, coordinating team

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
  - **Age:** Not more than 10 years old
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
