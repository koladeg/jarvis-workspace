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

### CV & Job Applications
- **Original CV:** Saved as `CV_Original_2025-07.pdf` (software developer focus)
- **Template CV:** Saved as `CV_TEMPLATE_Canada-International.md` (ready for customization per role)
- **Work Authorization:** Requires sponsorship (Kolade willing to fund if needed)
- **Strategy:** Customize CV for each application, highlight relevant skills/projects per role

### AWS Developer Certification (Not Priority, But Planned)
- **Current Study Resources:**
  - AWS Skill Builder (primary)
  - YouTube videos
  - Downloaded video courses
  - NotebookLM (to be used later for consolidation)
- **Target:** 3-month sprint (flexible timeline)
- **Plan:** Structure study schedule + quiz prep when secondary tasks begin
- **Status:** On hold until primary initiatives (funding scans, immigration research, truck monitoring, CV apps) are rolling

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

## Jarvis Support Plan - APPROVED & ACTIVE

**Status:** Live as of 2026-03-19 21:41 UTC
**Scope:** Comprehensive support across 9 major initiatives
**Model:** Sonnet (Kolade's brain dump session) → Opus planning → Haiku execution

**Top 3 Priorities:**
1. AdugboInsure (14 hrs/week) — Funding radar, content, expansion
2. Orisynx (8 hrs/week) — Code coordination, project management
3. SiFax (3-4 hrs/day) — Day job baseline

**Key Deliverables:**
- Funding scans (AdugboInsure): every 3-4 days
- Content packages (POS agents): weekly
- Truck listings (import/export): every 2-3 days
- Job search: ongoing with CV optimization
- Investment tracking: stocks (weekly) + crypto (weekly)
- Visa support: documentation & deadlines
- AWS certification: 3-month plan
- Programming (Python): ongoing learning path

**Organization:** 5 Telegram project groups (2026-03-20 LIVE)
- `Jarvis-Truck-Listings` — truck searches (posted past midnight WAT)
- `Jarvis-AdugboInsure` — content, funding radar, POS agent updates
- `Jarvis-Orisynx` — project coordination, code reviews
- `Jarvis-Job-Search` — CV applications, immigration tracking
- `Jarvis-Portfolio` — weekly investment snapshots

## Investment Portfolio (2026-03-20 LIVE)

**Total Value:** ~$2,000  
**Goal:** 3x in 3-4 years → $6,000  
**Monitoring:** Weekly snapshots → `Jarvis-Portfolio` Telegram group

**US Stocks (Bamboo):**
- NVIDIA 32.08% | Vector Acquisition 23.26% | BAC 7.88% | Netflix 6.52%
- Infrastructure: EQX, RSG | Retail: CNM | Semiconductors: AMD | Energy: TRX
- All-time return: +10.84%

**Crypto (Binance):**
- PAXG: 0.14 units (~$130) — gold hedge
- BTC: 0.005 (~$210-230)
- Others: USDC, ALGO, XLM, HBAR, TRON, SAND (small)

**Nigeria (Luno - Naira):**
- Broadcom: ₦81,210 | Robinhood: ₦121,512 (~$130 total)

**Nigerian Stocks (10+ years held):**
- Confirmed: GTB Bank, Dangote Sugar, Dangote Flour
- Others: TBD (waiting for broker confirmation)
- **Note:** Likely significant unrealized gains after 10 years

**Tracking:** Weekly snapshots sent to Portfolio group every Friday

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

- **Truck Import/Export Business Specs (2026-03-20 FINAL):**
  - **Target Brands:** HOWO, DAF, IVECO
  - **Configuration:** 4x2 (single steer axle, single rear axle only — no 6x4)
  - **Engine Power:** 380hp, 400hp, 430hp
  - **Condition:** Used (good condition, minimal repairs needed)
  - **Age:** Not more than 10 years old
  - **Mileage:** Good/reasonable
  - **Front Axle Weight Limit:** Max 35 tons
  - **Price Budget:** £4,000 max per truck
  - **Search Locations:** Germany, UK, Netherlands (for DAF/IVECO availability)
  - **Buying Strategy:** 3 trucks at a time to fill shipping containers efficiently
  - **Partners:** Kolade + 2 UK-based friends
  - **Monitoring Frequency:** Every 2-3 days
  - **Search Platforms:** AutoScout24, eBay Motors, Truck dealer networks (Germany/UK/Netherlands)
  - **Deliverables:** Filtered listings with direct links (via Telegram here, or WhatsApp group if provided)
