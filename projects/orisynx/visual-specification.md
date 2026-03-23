# Orisynx MVP Visual Specification

This package translates the earlier MVP screen analysis into developer-facing visual documentation.
It is intended to be attached to ClickUp tickets and used during design, frontend build, and acceptance testing.

## Deliverable Index

### Wireframes
- [Create Audit](./create-audit-wireframe.html)
- [Audit View](./audit-view-wireframe.html)
- [Workspace](./workspace-wireframe.html)
- [Task Manager](./task-manager-wireframe.html)
- [Calendar / Planner](./calendar-planner-wireframe.html)
- [Findings & CAPA](./findings-capa-wireframe.html)

### Flowcharts
- [Audit lifecycle](./audit-lifecycle.svg)
- [Workspace workflow](./workspace-workflow.svg)
- [Approval and locking workflow](./approval-workflow.svg)
- [Role-based access control](./rbac-visibility.svg)

### Data model visuals
- [Entity relationship diagram](./data-model-erd.svg)
- [Relationships and constraints](./data-model-constraints.svg)

---

## 1) Wireframe Intent by Screen

### Create Audit
**Goal:** Replace linear form setup with a planning canvas that makes scope, timeline, resources, import sources, and approval dependencies visible before activation.

**Visual priorities:**
- Canvas-based planning instead of stacked forms
- Live task generation preview
- CSV import visibility and mapping alerts
- Explicit approval gate before audit activation

### Audit View
**Goal:** Give stakeholders a read-only dashboard after approval/lock.

**Visual priorities:**
- Approved state is obvious
- Progress, evidence health, and finding posture shown at a glance
- Export and unlock request actions are visible
- No silent edits in approved state

### Workspace
**Goal:** Consolidate execution activities into one interface.

**Visual priorities:**
- Task execution, evidence capture, finding drafting, and exception escalation coexist
- Workspace isolation rules are visible and enforceable
- Current task remains central

### Task Manager
**Goal:** Show operational task status with evidence and finding linkage.

**Visual priorities:**
- Status-oriented task board
- Required evidence visible per task
- Direct path from failed task to finding
- Dependencies and blockers exposed

### Calendar / Planner
**Goal:** Make recurring templates and audit scheduling operationally clear.

**Visual priorities:**
- Calendar-based scheduling surface
- Template activation preview
- Resource conflict visibility
- Validation rules before activation

### Findings & CAPA
**Goal:** Present findings and corrective actions as one accountability chain.

**Visual priorities:**
- Findings register with decision state
- Detailed finding panel with evidence linkage
- CAPA progression board tied to approved findings

---

## 2) Before / After Comparison

| Screen | Current state (from analysis) | Required state per brief | Change required |
|---|---|---|---|
| Create Audit | Form-heavy setup, limited dependency visibility, planning spread across tabs | Visual planning canvas with scope, dates, owners, generation preview, approval readiness | Redesign IA around node/canvas metaphor with validation side panel |
| Audit View | Mixed edit/view behavior, weak lock cues | Clearly read-only approved dashboard with metrics, evidence health, and unlock request | Separate read-only mode and show lock/version state prominently |
| Workspace | Fragmented across task, evidence, findings, and comments screens | Unified working surface for execution and issue escalation | Merge modules into contextual workspace shell |
| Task Manager | Task list lacks strong evidence/finding connection | Task-centric operating board with evidence requirements and failure escalation | Extend task cards and detail view with related objects |
| Calendar / Planner | Scheduling exists but template activation impact is opaque | Calendar + activation preview + conflict detection | Add preview panel and validation rules before create/activate |
| Findings & CAPA | Findings and CAPA feel like separate modules | Single accountability chain from observation to action verification | Connect finding approval to CAPA generation and tracking |

---

## 3) Flow Definitions

### Audit lifecycle
**States:** Planned → Active → In Review → Approved → Closed

**Rules:**
- Planned: fully editable, pre-activation
- Active: task execution and evidence collection allowed
- In Review: lead review and revision loop
- Approved: record locked; edits only by unlock workflow
- Closed: final archival state

### Workspace workflow
**Path:** Select program → Perform tests → Attach evidence → Document findings → Raise exceptions

**Rules:**
- Evidence should be attachable without leaving the workspace
- Failures should prefill finding data from the originating task
- Exceptions notify the lead when risk or blockers require intervention

### Approval workflow
**Path:** Submit for review → Team Lead review → Approval lock → Unlock for revision (if needed)

**Rules:**
- Approval creates version snapshot
- Unlock must create an audit trail event and working version
- Re-approval required after any unlocked changes

### RBAC
**Roles modeled:** Auditor, Team Lead, Approver, Admin

**Rules:**
- Auditor access is assignment-scoped
- Team Lead access is team-scoped
- Approver sees approved scope and can lock/unlock
- Admin has full override visibility

---

## 4) Data Model Definition

### Core entities and fields

#### AuditProgram
- `id`
- `name`
- `version`
- `status`
- `default_task_template_set`

#### Audit
- `id`
- `audit_program_id`
- `name`
- `site`
- `area`
- `planned_start`
- `planned_end`
- `status`
- `lock_version`
- `owner_user_id`
- `approver_user_id`
- `created_from_template`
- `csv_import_batch_id`

#### Task
- `id`
- `audit_id`
- `program_test_ref`
- `status`
- `risk_band`
- `assignee_id`
- `result`
- `due_at`
- `requires_evidence`

#### Evidence
- `id`
- `task_id`
- `audit_id`
- `file_url`
- `mime_type`
- `ocr_text`
- `captured_by`
- `captured_at`
- `classification`
- `metadata_json`

#### Finding
- `id`
- `audit_id`
- `task_id`
- `severity`
- `status`
- `observation`
- `criterion`
- `risk_statement`
- `owner_id`
- `due_at`
- `approved_at`
- `approved_by`

#### CAPA
- `id`
- `finding_id`
- `action_type`
- `owner_id`
- `target_date`
- `status`
- `effectiveness_check`

#### Approval
- `id`
- `audit_id`
- `approval_type`
- `decision`
- `decided_by`
- `decided_at`
- `comment`
- `unlock_reason`

### Relationship summary
- One AuditProgram creates many Audits
- One Audit contains many Tasks
- One Task can have many Evidence items
- A failed Task may generate one or more Findings
- One Finding can produce many CAPAs
- One Audit can have many Approval events

### Constraints summary
- Approved audit state is immutable without unlock
- Closed audits reject new operational data
- Findings require evidence and criterion before approval
- CAPA target date cannot precede finding approval
- Unlock must increment working version and require re-approval
- Access control applies to audits, evidence, findings, and approvals separately

---

## 5) Visual Acceptance Criteria by Ticket Theme

### A. CSV Import
**Visual story:** Excel → Upload → Parse → Mapping validation → Create tasks

**Acceptance criteria:**
- User can upload a spreadsheet from Create Audit
- System shows parsed row count, matched templates, and unmatched rows
- Invalid mappings are shown before task creation
- Preview shows how many tasks will be created per section
- Created tasks retain traceability to the import batch

### B. Workspace Isolation
**Visual story:** Role logs in → Sees only assigned audit/program/task/evidence scope

**Acceptance criteria:**
- Auditor sees only own assignments and own/allowed evidence
- Team Lead sees team scope but not unrestricted global data
- Approver can review approved scope and execute lock/unlock actions
- Admin has full access
- No screen leaks restricted records through search, counters, or side panels

### C. Approval Locking
**Visual story:** In Review → Approved → Locked → Unlock request → Working version → Re-approve

**Acceptance criteria:**
- Approved audits display a lock/version banner
- Editing controls are removed or disabled in approved state
- Unlock requires explicit authorized action and a reason
- Unlock creates audit trail + new working version
- Re-approval is mandatory after unlocked edits

### D. Unified Workspace
**Visual story:** Open task → Perform test → Attach evidence → Fail task → Raise finding

**Acceptance criteria:**
- User does not need to navigate to a separate module to attach evidence
- Fail outcome exposes finding draft flow in context
- Related evidence is available while drafting finding
- Exception raise action is available for blockers or critical issues

### E. Calendar / Template Activation
**Visual story:** Choose template → Pick dates → Validate resources → Preview load → Activate

**Acceptance criteria:**
- Planner shows scheduled audits in calendar form
- Activation preview includes generated task count and milestone count
- Resource conflicts and overlaps are shown before activation
- Template cannot activate if required approver/coverage is missing

### F. Findings & CAPA
**Visual story:** Finding approved → CAPA created → Action progresses → Effectiveness verified

**Acceptance criteria:**
- Findings show severity, status, source task, evidence, and owner
- CAPA can be linked directly from an approved finding
- CAPA board shows lifecycle from proposed to verified
- Action ownership and due dates are visible

---

## 6) Notes for Engineering

- The wireframes are intentionally structural rather than pixel-perfect.
- Approval lock state should be enforced server-side, not only visually.
- CSV import, RBAC, and unlock actions need auditable events.
- The unified workspace should preserve deep links to task, evidence, and finding records.
- Consider version snapshots for approved audits so exports remain reproducible.

---

## 7) Recommended Ticket Attachments

Attach this file plus the linked HTML/SVG assets to the relevant ClickUp tickets:
- Create Audit redesign
- Audit View read-only dashboard
- Unified Workspace
- Task Manager overhaul
- Planner / template activation
- Findings & CAPA chain
- CSV import traceability
- Workspace isolation / RBAC
- Approval locking and unlock flow
