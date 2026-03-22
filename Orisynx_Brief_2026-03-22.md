# Orisynx: Audit System Development Brief
**Meeting Date:** Sunday, March 22, 2026  
**Document:** Strategic Requirements for MVP Implementation

---

## Executive Summary

Transition from high-level audit planning to granular execution within MVP framework.

**Core Distinction:** Audit Plan (board-approved annual schedule) ≠ Audit Program (specific checklists & procedures)

**Key Principle:** *"Our work starts from the audit plan because that's what we do... The board has to approve your audit plan because that's to say this is my plan of activity."*

---

## 1. Audit Planning & Scheduling

### The Annual Audit Plan
- **Definition:** Schedule of work auditors perform year-round
- **Scope:** Department + start/end dates (objectives optional unless board-requested)
- **Board Approval:** External approval pre-loaded into system (not a UI approval workflow)
- **Flexibility:** Plans subject to change mid-year (cancellations, additions via emerging risks)

### Planner Module
- **Function:** Calendar/timeline view (similar to Google Calendar)
- **Records:** Hold audit templates in "inactive" state
- **Activation:** Users "execute" or "activate" specific audits as needed (not bulk-create upfront)
- **UI Location:** Primary navigation menu, immediately after Dashboard

---

## 2. Audit Execution: Workspace Model

### Workspace Structure
- **Isolation:** Each audit has its own workspace visible only to assigned team
- **Example:** 3-person team assigned to finance audit works in isolated workspace

### Process Flow
1. **Select** work program/checklist
2. **Perform** specific tests (e.g., verify monthly reconciliations)
3. **Attach** evidence (files/documentation)
4. **Document** findings:
   - Control gaps (missing evidence, e.g., only 2/5 months provided)
   - Specific test outcomes
5. **Raise** Exceptions/Findings → flows to dedicated Findings area

### Workspace vs. Dashboard
- **Canvas Metaphor:** Creation menu = canvas (where you design); workspace = where you paint (actual audit work)
- **Dashboard:** Read-only snapshot/overview, NOT for data entry or testing
- **Task Manager Refinement:**
  - Tasks must link directly to audit work program
  - No generic, unlinked task items
  - Full context visibility per audit

---

## 3. Template Management & Data Ingestion

### Flexibility Requirement
Audit requirements vary by industry/jurisdiction → cannot force single global template

### User Workflow
1. **Import:** Clients create custom work programs in Excel
2. **Upload:** CSV/Excel endpoints ingest programs
3. **Template:** System provides downloadable template with required columns:
   - Test Name
   - Expected Outcome
   - (other industry-specific fields)
4. **Ingestion:** Checklist items added either manually (unique cases) or via import (recurring audits)

### MVP Feature Priorities
| Feature | Priority | Purpose |
|---------|----------|---------|
| Excel/CSV Import | **High** | Ingest existing checklists |
| Downloadable Templates | **High** | Provide standardized format |
| Custom Checklist Items | Medium | On-the-fly additions to active audits |

---

## 4. Governance, Roles & Approvals

### Approval Hierarchy
- **Board Level:** ❌ Excluded from MVP (one-time annual approvals, unlikely to onboard)
- **Internal Team Level:** ✅ **Critical** — "Local Approvals"
  - Team Lead reviews work performed by junior staff
  - Configurable per audit
  - Audit Owner assigns Approval Authorities

### Roles & Permissions
- **Audit Integrity:** Approved sections become non-editable (audit trail preservation)
- **Visibility:** Only assigned team members + Head of Department see audit work-in-progress
- **Granularity:** Role-based access control required

---

## 5. UX Refinements

### Remove from MVP
- **"Department Involved" Field:** Not necessary; only audit personnel perform audits (guest auditors rare)

### Improve
- **Pre-loaded Data:** Remove ISO standards/department defaults → blank, customizable lists preferred
- **Menu Navigation:** Add "Audit Plan" as primary menu item (right after Dashboard)

### Keep
- Workspace-centric design
- Evidence attachment workflow
- Exception/Findings documentation

---

## Architecture Layers (Visual)

```
┌─────────────────────────────────────────┐
│        PLANNER (Calendar View)          │
│  - Annual audit schedule (templates)    │
│  - Activate/execute as needed           │
│  - Board-approved document attachment   │
└─────────────────────────────────────────┘
           ↓ (Activation)
┌─────────────────────────────────────────┐
│    AUDIT PROGRAM (Work Program)         │
│  - Specific checklists & procedures     │
│  - Imported from CSV/Excel or custom    │
│  - Assigned to team                     │
└─────────────────────────────────────────┘
           ↓ (Execution)
┌─────────────────────────────────────────┐
│    WORKSPACE (Isolated Environment)     │
│  - Team performs tests                  │
│  - Attaches evidence                    │
│  - Documents findings/control gaps      │
│  - Raises exceptions                    │
│  - Local approvals (Team Lead review)   │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  DASHBOARD (Read-Only Snapshot)         │
│  - Overview of all audits               │
│  - Status indicators                    │
│  - No data entry                        │
└─────────────────────────────────────────┘
```

---

## Next Steps (Implementation)

### Phase 1: Data Models & Schemas
- [ ] Define Planner schema (calendar, audit templates)
- [ ] Define Audit Program schema (work program, checklist items)
- [ ] Define Workspace schema (tests, evidence, findings)
- [ ] Define Approval schema (approval authorities, audit trail)

### Phase 2: Backend Features
- [ ] CSV/Excel import endpoint
- [ ] Downloadable template endpoint
- [ ] Workspace isolation (permission checks)
- [ ] Approval workflow (Team Lead review, lock on approval)

### Phase 3: Frontend Components
- [ ] Planner calendar UI
- [ ] Workspace editor (tests, evidence attachment, findings)
- [ ] Audit Program selector
- [ ] Exception/Findings display

### Phase 4: Integration
- [ ] Menu navigation restructuring
- [ ] Role-based access control
- [ ] Audit trail logging

---

## Questions for Clarification

1. **CSV Import Columns:** What are the exact expected columns in the downloadable template?
2. **Approval Workflow:** Multi-level approvals (e.g., Lead → Senior Lead → Head) or just one level?
3. **Evidence Storage:** File size limits? Storage backend (S3, local)?
4. **Audit Statuses:** Planned → Active → In Review → Approved → Closed?
5. **Findings Categories:** Control gaps, observations, recommendations, or custom?

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-22 07:14 UTC  
**Owner:** Kolade (Orisynx)
