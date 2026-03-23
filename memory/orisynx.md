# Orisynx - Internal Audit SaaS / GRC Platform

## Core Business Model

**Company Name:** Orisynx (Oversight Sync)

**What:** Workflow-driven GRC/Internal Audit platform for Nigerian organizations

**Problem Solved:**
- Foreign GRC solutions cost ₦500M-₦1B+ upfront + millions annually
- Nigerian orgs default to Word/Excel → fragmented, unreliable, no collaboration
- No real-time reviews, evidence scattered in folders, no aggregation

**Solution Differentiators:**
1. **Workflow-driven** — Plan audit → conduct tests → report → track findings
2. **Single source of truth** — Centralize risks, controls, audit evidence
3. **Evidence-attached-to-tests** — Evidence tied to specific tests, not dumped in folders
4. **Client portal** — Auditees respond to findings, update CAPAs in-system
5. **Auto-aggregated dashboards** — Compliance scores, risk ratings aggregated across org
6. **Cost leadership** — <₦3M/year vs. ₦1B+ for AuditBoard, SAP, Archer

**Business Model:**
- B2B SaaS, subscription-based (per-user pricing)
- Target price: <₦3M/year
- Revenue model: Subscription + potential per-user/per-org variations

**Target Market (Go-to-Market):**
- **Phase 1:** Nigeria (microfinance banks, finance companies primary)
- **Phase 2:** Expand to Africa (manufacturing, healthcare secondary sectors)
- **User personas:** Internal auditors, internal control officers, risk management teams

**MVP Scope:**
- Plan audit (risk register → controls mapping)
- Conduct tests with attached evidence
- Write report
- Track findings / CAPA management
- Template library (incremental, user-feedback driven)
- No complex AI integrations initially

**Key Insight:** Start with microfinance banks (biggest pain point, smallest budget) → prove market fit → expand

---

## Team

1. **Lawyer** — Handling organization registration
2. **Internal Audit Expert** — Senior in sector, advising on solution design
3. **Backend Developer** — Moving into DevOps role, using AI for tooling
4. **Frontend Developer** — Based in Canada, strong design foundation, independent contributor
5. **Kolade (You)** — Project lead/director, coordinates team, code reviews, NOT primary coder

**Team Dynamics:**
- Team autonomy is high (especially frontend dev in Canada)
- Backend dev moving toward DevOps may reduce direct coding involvement
- Need to ensure alignment on MVP scope and timeline

---

## Project Infrastructure

### GitHub Repositories
- **Frontend:** https://github.com/Audit-IS/fe
- **Backend:** https://github.com/Orisynx/Orisynx-backend
- **Status:** Code pushed live (as of 2026-03-21)

### ClickUp
- **Workspace:** "Orisynx's Workspace"
- **Channels:**
  - **Management** 🔒 (private) — Company registration, legal docs
  - **dev** — Development tasks, technical planning
  - **Orisynx's Workspace** — General workspace
  - **Welcome** — Onboarding/reference
- **Integration:** Via Zapier MCP (configured 2026-03-16)
- **Access:** Zapier endpoint: https://mcp.zapier.com/api/v1/connect
- **Token stored:** `.zapier-mcp-config` (bearer token configured)
- **Team members (DMs):** Props Account, Kolade Gureje, FO, Dayo, Orisynx

### NotebookLM
- **Notebook:** "AuditBoard GRC Application Technical Proposal for FMDQ"
- **Notebook ID:** cbefa8a7-c4d4-4d52-adc5-ecaccb4854b8
- **URL:** https://notebooklm.google.com/notebook/cbefa8a7-c4d4-4d52-adc5-ecaccb4854b8
- **Sources:** 18 documents covering GRC domain, internal audit workflows, control testing, RCSA
- **Access:** Via nlm CLI (authenticated 2026-03-21)
- **Credentials stored:** `/home/claw/.openclaw/workspace/.credentials/notebooklm_cookies.txt`

### Notion
- **Documentation:** Used for technical proposal and reference materials
- **Access:** [CONFIRM IF NEEDED]

---

## Credentials & Access

**ClickUp (via Zapier):**
- Workspace/team details: [SAVED IN ZAPIER INTEGRATION]
- Access method: Via Zapier MCP CLI or compatible tools
- Token: Bearer token in `.zapier-mcp-config`

**GitHub:**
- Access already configured in `.credentials` (existing token)

**NotebookLM:**
- Authenticated via cookies in `.credentials/notebooklm_cookies.txt`
- Profile: default
- Auth method: Google cookies (nlm login --manual --file)

---

## Legal Documents & Registration

**Shareholders' Agreement (executed 2026-03-18):**
- **Company:** ORISYNX LIMITED (RC: 9422696)
- **Shareholders (equal 1/3 each currently):**
  1. Oladayo Oniroko (Lagos)
  2. Adebiyi Samuel Olufemi (Ibadan)
  3. Gureje Kolade Temitayo (Lagos) — **YOU**
- **Fourth Shareholder Slot:** Reserved for future admission (unanimous approval required, becomes 25% each)
- **All shareholders are Directors** of the company
- **Key provisions:**
  - Equal shareholding is fundamental
  - Board decisions: simple majority (except Reserved Matters = unanimous)
  - Board meetings: quarterly minimum
  - Drag-along rights: 75% can force minority to sell
  - Tag-along rights: minority can join majority sale
  - Pre-emption: existing shareholders can match any external offers first
  - Exit: 60 days notice; other shareholders can buy at fair market value
  - Non-compete: 2 years post-exit
  - Reserved matters: 12 items require unanimous approval (asset sales >₦500K, borrowing >₦1M, dividends, new shareholders, etc.)

## Current Status

**Organization Registration:** In progress (lawyer handling)

**Code Status:** Pushed to GitHub (as of 2026-03-21)
- Frontend: Live on repo
- Backend: Live on repo
- Code review phase complete

**MVP Product Definition:** Complete (2026-03-22)
- Architecture finalized: Planner → Audit Program → Workspace → Dashboard
- 19 current MVP screens mapped to requirements
- 15+ technical tickets identified for ClickUp
- Gaps identified: CSV import, workspace isolation, approval locking, granular permissions

**Next Steps:**
1. Finalize org registration
2. Add tickets to ClickUp (ready to copy/paste)
3. Assign tickets to team (backend, frontend, DevOps)
4. Start Phase 1: Data Models & Schemas
5. Identify early adopter / pilot customer
6. Plan MVP release schedule

---

## Product Brief & MVP Architecture (2026-03-22 Meeting)

**Key Quote:** *"Our work starts from the audit plan because that's what we do... The board has to approve your audit plan because that's to say this is my plan of activity."*

### 4-Layer Architecture
1. **Planner** (Calendar/Timeline) — Annual audit schedule held as templates, activated as needed
2. **Audit Program** (Work Programs) — Specific checklists & procedures, imported from CSV/Excel or custom-created
3. **Workspace** (Isolated per-audit environment) — Team performs tests, attaches evidence, documents findings, raises exceptions
4. **Dashboard** (Read-only overview) — Status snapshots, no data entry

### Canvas Metaphor
- **Canvas** = Creation menu (where you design audits, import templates, plan schedule)
- **Workspace** = Where you "paint" (actual audit execution: tests, evidence, findings)
- **Dashboard** = Read-only snapshot view (overview only, not for operational work)

### MVP Feature Priorities
| Feature | Priority | Purpose |
|---------|----------|---------|
| CSV/Excel Import for Audit Programs | HIGH | Users import custom work programs from Excel |
| Downloadable Templates | HIGH | System provides standardized template format for download/re-upload |
| Workspace Isolation & Team Access | HIGH | Each audit isolated; only assigned team members + Head of Department see it |
| Local Approvals with Locking | HIGH | Team Lead reviews work, approval locks section from further edits (audit trail) |
| Granular Roles & Permissions Matrix | HIGH | Role-based access control per audit, per action, per screen |
| Template Activation Workflow | MEDIUM | Activate planned audits from Planner calendar as execution begins |
| Approval Hierarchy (configurable) | MEDIUM | Audit Owner assigns Approval Authorities; Board-level approvals external |
| Remove "Department Involved" Field | MEDIUM | Cross-cutting cleanup (no guest auditors in MVP; only audit staff) |
| Canvas Metaphor UX Redesign | MEDIUM | Rename/restructure navigation to reflect canvas vs workspace distinction |
| Workspace: Unified Navigation | MEDIUM | Tie Task manager + Findings + Document library into cohesive workspace |

### Current MVP Screens (19 total)
**Mapped to Brief Requirements:**
- Calendar page → Planner (base, needs template activation flow)
- Task manager / Task view → Workspace component (needs isolation, team access)
- Audit view → Dashboard candidate (needs read-only enforcement)
- Document review and sign off → Local approvals (needs post-approval locking)
- Templates manager / Create template → Template management (needs CSV import/export)
- Users / Edit user → Roles/permissions base (needs granular permission matrix)
- Findings → Workspace output (good, linked to tests)
- CAPA tracker → Findings follow-up (good fit)
- Document library → Evidence repository (good, part of workspace)
- Reports / Analytics → Dashboard supplement (good, overview)
- Others: Auth, Audit history, Notifications, Account user (supporting)

### Gaps Identified (To Close)
1. **Audit Program as first-class entity** — Work programs/checklists and CSV import pipeline not clearly represented
2. **Workspace as cohesive model** — Currently fragmented across task manager, findings, document library screens
3. **Approval locking** — Sign-off exists, but post-approval edit lock not explicit
4. **Granular permissions** — Role matrix not fully implemented; per-audit team access likely missing
5. **Canvas metaphor** — No explicit distinction between creation (canvas) and execution (workspace)
6. **Read-only enforcement** — Dashboard rule ("NOT for data entry") likely not enforced in current Audit view
7. **"Department Involved" removal** — Field likely still exists in forms/reports; needs cross-cutting cleanup

### Top 10 Technical Tickets (Ready for ClickUp)
1. **CSV/Excel Import for Audit Programs** — HIGH | Endpoint accepts uploaded CSV, parses work programs, creates checklist items
2. **Workspace Isolation & Team Access Controls** — HIGH | Query-level isolation per audit; permission checks on all workspace screens
3. **Approval Locking (Post-Sign-Off)** — HIGH | After Team Lead approval, lock approved section; unlock requires new approval
4. **Granular Roles & Permissions Matrix** — HIGH | Define role matrix (Admin, Audit Manager, Team Lead, Auditor, Reviewer); permission enforcement per screen/action
5. **Template Download/Export Endpoints** — HIGH | Download template as CSV; users can customize and re-import
6. **Planner: Template Activation Workflow** — MEDIUM | Calendar view allows "Activate" action on planned audit; creates active audit from template
7. **Remove "Department Involved" Field** — MEDIUM | Remove field from Create audit UI; remove from schema; remove from reports/imports
8. **Dashboard: Enforce Read-Only on Audit View** — MEDIUM | Audit view becomes read-only; all data entry moves to workspace/task flows
9. **Canvas Metaphor UX Redesign** — MEDIUM | Rename/reorder menu items; restructure Audit view as overview; add "Audit Plan" primary nav item
10. **Workspace: Unified Navigation** — MEDIUM | Workspace consolidates task manager, findings, document library, evidence into single cohesive interface

### Questions for Clarification (Before Building)
1. **CSV Import Columns:** What are exact column names in downloadable template?
2. **Approval Hierarchy:** Multi-level (Lead → Senior Lead → Head) or single Team Lead approval?
3. **Evidence Storage:** File size limits? Storage backend (S3, local)?
4. **Audit Statuses:** Planned → Active → In Review → Approved → Closed, or different?
5. **Findings Categories:** Control gaps, observations, recommendations, or custom per client?
6. **Team Assignment:** How many team members per audit? Fixed teams or flexible?
7. **Board Approval:** External document attachment (PDF upload) or in-system workflow?

### Documents Created
- `Orisynx_Brief_2026-03-22.md` — Full meeting brief + 4-layer architecture + detailed requirement breakdown + ticket descriptions
- `memory/orisynx.md` (this file) — Living project memory

### Model Used for Analysis
- **Codex** (openai-codex/gpt-5.4) — Deep technical breakdown of MVP screens vs requirements (2026-03-22 09:32 UTC)

---

## MVP Review Meeting Workflow (Process for Future Meetings)

**Established Process (2026-03-22):**

### Step 1: Capture the Brief
- Meeting discussion → detailed requirements list
- Save to `Orisynx_Brief_YYYY-MM-DD.md` (structured format with sections)
- Include: architecture, feature priorities, gaps, clarifying questions

### Step 2: Analyze with Codex
- Spawn Codex subagent (openai-codex/gpt-5.4)
- Task: Map current MVP screens to brief requirements
- Output: Screen-to-requirement mapping + gap analysis + technical ticket descriptions
- Result: Codex identifies what's built vs what's missing

### Step 3: Save to Orisynx Memory
- Update `memory/orisynx.md` with:
  - Meeting summary
  - Architecture diagram
  - MVP feature priorities table
  - Current screens status
  - Gaps identified
  - Top 10 tickets (copy/paste ready)
  - Clarification questions for team

### Step 4: Create ClickUp Tickets via Zapier MCP
**Setup (one-time):**
- mcporter config at: `/home/claw/.openclaw/workspace/config/mcporter.json`
- Zapier MCP server pre-authenticated with ClickUp token
- Use tool: `mcporter call zapier-mcp.clickup_create_task`

**Batch ticket creation script:**
```bash
#!/bin/bash
CONFIG="/home/claw/.openclaw/workspace/config/mcporter.json"

# Loop through tickets array
for ticket in "${tickets[@]}"; do
  IFS='|' read -r title desc <<< "$ticket"
  mcporter call zapier-mcp.clickup_create_task \
    "instructions=Create MVP ticket for Orisynx audit system" \
    "name=$title" \
    "content=$desc" \
    "priority=$PRIORITY" \
    --config "$CONFIG" --output json > /dev/null 2>&1
  sleep 2
done
```

**Parameters:**
- `name=` — Ticket title
- `content=` — Ticket description/acceptance criteria
- `priority=` — "HIGH" or "MEDIUM" (string, not number)
- `instructions=` — Natural language context for Zapier
- `--config` — Must point to mcporter.json
- `sleep 2` — Rate limiting (avoid Zapier throttling)

**Result:**
- Tickets created in ClickUp Backlogs list
- Status: "to do"
- Priority: Set correctly
- Creator: Kolade Gureje (bot uses authenticated context)
- URL: Each ticket gets a ClickUp link

### Step 5: Team Assignment & Refinement
- Pull up ClickUp Backlogs
- Assign tickets to team (backend, frontend, DevOps)
- Add acceptance criteria from detailed ticket descriptions
- Move to sprint/project folder as needed

---

## For Next MVP Review Meeting (Template)

**Pre-Meeting:**
1. Ensure Zapier MCP is still authenticated (test with one dummy ticket)
2. Prepare brief document template

**During Meeting:**
1. Capture requirements discussion
2. Create `Orisynx_Brief_YYYY-MM-DD.md`

**Post-Meeting (Same Day if Possible):**
1. Spawn Codex for analysis → 1-2 minutes
2. Save to `memory/orisynx.md` → 2-3 minutes
3. Create HIGH priority tickets via mcporter → 15-20 minutes (rate limited)
4. If time allows, create MEDIUM tickets (delegate to Codex for batch creation)
5. Share ClickUp link with team

**Total Time:** ~45-60 minutes from meeting end to tickets ready in ClickUp

---

## ClickUp Tickets Created (2026-03-22)

### HIGH Priority (11 tickets)
1. CSV/Excel Import for Audit Programs
2. Workspace Isolation & Team Access Controls
3. Approval Locking (Post-Sign-Off)
4. Granular Roles & Permissions Matrix
5. Template Download/Export Endpoints
6. Planner: Template Activation Workflow
7. Remove Department Involved Field
8. Dashboard: Enforce Read-Only on Audit View
9. Canvas Metaphor UX Redesign
10. Workspace: Unified Navigation
11. Audit Program as First-Class Entity

### MEDIUM Priority (12 tickets — created by Codex)
1. Approval Hierarchy (Configurable)
2. Board-Level Approval Integration
3. Audit Statuses & Lifecycle
4. Findings Categories & Severity
5. Evidence Attachment & Storage
6. CAPA Tracking Workflow
7. Template Versioning & Activation
8. Audit Team Assignment & Access
9. Dashboard Widgets & Customization
10. Audit Report Export
11. Notifications & Approvals Workflow
12. Permission Enforcement Tests

**Total MVP Tickets:** 23 (11 HIGH + 12 MEDIUM)

---

## Key Decisions & Constraints

- **MVP-first approach** — Ship workflow, template library grows with user feedback
- **Nigerian market focus initially** — Microfinance banks are the beachhead
- **Cost positioning is critical** — Must stay <₦3M/year to be compelling
- **No complex features early** — Automate what orgs do manually, add sophistication incrementally
- **Team coordination is project-critical** — Especially with distributed team (Canada dev)

---

## To Remember

- This is **not an awareness/education product like AdugboInsure** — it's a production SaaS tool with real users/customers
- **Pricing in Naira is a competitive advantage** — foreign competitors quote in USD, making them prohibitively expensive
- **The problem is real and urgent** — orgs are actively looking for local alternatives to expensive foreign GRC tools
- **Early adopters will drive product** — listen to microfinance bank feedback, iterate fast
