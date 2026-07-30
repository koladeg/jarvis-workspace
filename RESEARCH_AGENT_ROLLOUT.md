# RESEARCH_AGENT_ROLLOUT.md

## Purpose
Daily source of truth for the research-agent rollout status.

## Current Status
- **Overall status:** stale / needs restart
- **Current phase:** Phase 2.5 — credibility rebuild
- **Last updated (UTC):** 2026-07-30 18:20

## Phases

### Phase 0 — Foundation
- Status: complete
- Notes:
  - Secondary research workspace created
  - Basic end-to-end response confirmed

### Phase 1 — Capability wiring
- Status: complete
- Notes:
  - Apify MCP configured via local stdio launcher
  - Credentials saved and verified
  - Durable guidance added for jobs, funding, and school/MBA research

### Phase 2 — First live execution
- Status: partial
- Notes:
  - First real research pass executed
  - Funding results surfaced
  - Strong-fit job outputs not yet consistently landing

### Phase 3 — Operational rollout
- Status: blocked
- Notes:
  - Approved lane cadence is defined, but cadence markers have outperformed the research itself
  - A lane only counts as active if it runs on schedule, is logged the same day, and produces a visible update when due
  - Reporting must reflect real lane activity, not just setup/automation changes
  - Truck lane was removed from the active pipeline on 2026-07-30 by user request
  - Funding, immigration, community sponsors, and school/MBA are not yet operational by that standard

### Phase 4 — Stable automation
- Status: pending
- Exit criteria:
  - Daily updates arrive reliably without prompting
  - Research runs consistently produce usable outputs
  - Blockers and next actions are reported clearly

## Completed Since Last Update
- Recorded the 2026-07-30 pipeline review and closed the review-gap
- Marked the rollout state honestly based on current evidence instead of leaving it labeled active
- Started credibility repairs on the scheduler logging path and the funding lane
- Removed the truck lane from the active pipeline, scheduler cadence, and activity summaries by user request

## Current Blockers
- Execution, logging, and delivery still need to stay in sync consistently over time
- Duplicate scheduler log lines have reduced trust in the cron evidence trail
- Funding was previously generating a static template with stale assumptions instead of live, last-verified tracking
- Several lanes still lack minimum viable output structures, so they should not be reported as operational

## Next Action
- Rebuild credibility first: keep rollout status conservative, remove misleading funding output, verify scheduler evidence, and only move back to operational status after fresh lane passes in the remaining lanes produce useful outputs consistently

## Daily Update Template Inputs
- **Today status:** Rollout credibility rebuild started; status downgraded from active to stale / needs restart
- **What completed today:** fresh review logged, rollout state corrected, funding-lane cleanup started, scheduler logging fix started, truck lane removed from active scope
- **Main blocker:** most lanes still are not producing current decision-quality outputs consistently
- **Next action:** verify the repaired scheduler path and replace placeholder lane output with real tracked findings
