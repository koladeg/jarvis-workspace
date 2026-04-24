# Orisynx — ClickUp-Friendly Minimal Implementation Breakdown

Date: 2026-04-23
Goal: convert the minimal-change schema proposal into practical implementation work that fits the current MVP and avoids major redesign.

---

## Guiding Rule

Do not rebuild the MVP.

Ship the smallest additions that make the current screens more faithful to real audit workflows:
- planning
- audit programs
- request lists
- team isolation
- sign-off locking

---

# EPIC 1 — Audit Planning Layer

## Outcome
The existing Calendar page becomes a real planning layer without replacing the current audit flow.

### Backend Tasks

#### 1. Create `audit_plans` table + API
**Priority:** HIGH
**Why:** Needed to support annual/period planning without overloading `audits`.

**Scope:**
- create `audit_plans` table
- create CRUD endpoints
- support status, year, title, overview, methodology notes, version
- support approval fields

**Acceptance Criteria:**
- backend can create/update/list audit plans
- one plan can hold multiple planned audit items
- plan status can be draft or approved

---

#### 2. Create `audit_plan_items` table + API
**Priority:** HIGH
**Why:** Needed for calendar-planned audits and template activation.

**Scope:**
- create `audit_plan_items` table
- link items to business unit and optional template
- support quarter/date/risk/duration fields
- support `activation_status`
- support linking activated item to created audit

**Acceptance Criteria:**
- a plan item can be created from backend
- plan item can be marked planned/activated/completed
- activated plan item can link to an actual audit record

---

### Frontend Tasks

#### 3. Wire Calendar page to real plan items
**Priority:** MEDIUM
**Why:** The page already exists; just make it data-backed.

**Scope:**
- fetch audit plan items
- display plan items in calendar/timeline form
- show risk rating and planned period
- add activation action

**Acceptance Criteria:**
- calendar shows real plan items from backend
- user can open a plan item and see summary data
- activation button is visible for eligible plan items

---

#### 4. Add “Activate Audit” flow from Calendar
**Priority:** MEDIUM
**Why:** Already identified in prior MVP mapping.

**Scope:**
- user activates plan item
- frontend calls backend to create audit from plan item
- plan item updates to activated
- new audit becomes accessible in current audit flow

**Acceptance Criteria:**
- activating a plan item creates an audit
- audit is linked back to the plan item
- activated item no longer appears as plain unscheduled work

---

# EPIC 2 — Audit Program / Work Programme Layer

## Outcome
The MVP gets a structured audit-program object without replacing current task screens.

### Backend Tasks

#### 5. Create `audit_programs` table + API
**Priority:** HIGH
**Why:** This is the biggest current gap and aligns directly with the source documents.

**Scope:**
- create `audit_programs` table
- link program to audit
- allow name, notes, objectives, process/sub-process, version, status
- support template linkage

**Acceptance Criteria:**
- one audit can have one or more audit programs
- audit program can be created manually
- audit program can be created from template later

---

#### 6. Create `audit_program_steps` table + API
**Priority:** HIGH
**Why:** Needed to model risk/control/test structure while staying lightweight.

**Scope:**
- hierarchical step table using parent-child structure
- support step types: section, risk, control, test
- include priority/scoring/guidance/evidence prompt/answer options
- include sort order

**Acceptance Criteria:**
- backend can store nested steps for a program
- step types are validated
- steps can be returned in ordered tree form

---

#### 7. Create `audit_program_step_results` table + API
**Priority:** HIGH
**Why:** Needed to connect tasks/execution to a structured audit program.

**Scope:**
- store execution result per step
- support assigned user, status, notes, score, exception count, completion/review timestamps

**Acceptance Criteria:**
- a program step can receive an execution result
- step result can be updated by assigned team member
- result can later link to findings/evidence

---

### Frontend Tasks

#### 8. Add Audit Program tab/section inside Audit
**Priority:** MEDIUM
**Why:** Minimal UI change with high value.

**Scope:**
- add an “Audit Program” section inside the existing audit interface
- list audit programs linked to the current audit
- allow open/view/create

**Acceptance Criteria:**
- user can view audit programs inside an audit
- user can create at least one audit program for an audit
- UI does not require a new major navigation pattern

---

#### 9. Reuse Task Manager for audit-program execution
**Priority:** HIGH
**Why:** Avoids building a second execution UI.

**Scope:**
- map tasks/task items to `audit_program_steps` or `audit_program_step_results`
- show status, assignee, notes, evidence prompt
- distinguish test/control/risk steps visually

**Acceptance Criteria:**
- audit-program execution happens through current task-oriented UI
- assigned users can update step result status/notes
- users can tell what kind of step they are working on

---

# EPIC 3 — Audit Request List Layer

## Outcome
The MVP can track “audit requirements” / pre-fieldwork document requests using the current document flow.

### Backend Tasks

#### 10. Create `audit_request_items` table + API
**Priority:** HIGH
**Why:** Source docs repeatedly show structured request lists as part of every engagement.

**Scope:**
- create `audit_request_items`
- support category, title, description, required format, due date, status, notes
- support optional uploaded document link

**Acceptance Criteria:**
- an audit can hold many request items
- request items can move through pending/received/partial/not applicable
- request item can link to an uploaded document

---

### Frontend Tasks

#### 11. Add Request List view inside current audit/documents area
**Priority:** MEDIUM
**Why:** Best fit is to extend current document library, not create a whole new module.

**Scope:**
- show request items by status/category
- allow creation/editing of request items
- allow attaching uploaded files as responses

**Acceptance Criteria:**
- request items are visible inside current audit experience
- users can mark items received or partial
- users can attach response documents to request items

---

# EPIC 4 — Access Control and Workspace Isolation

## Outcome
The workspace behaves per audit team instead of as a broad shared area.

### Backend Tasks

#### 12. Create `audit_team_assignments` table + API
**Priority:** HIGH
**Why:** Already identified as a major gap in the MVP review.

**Scope:**
- create per-audit team assignments
- roles: audit_manager, team_lead, auditor, reviewer
- expose endpoints to assign/remove/list users on an audit

**Acceptance Criteria:**
- an audit can have multiple assigned team members
- user role is stored per audit
- backend can return only team members for an audit

---

#### 13. Enforce audit-level access checks
**Priority:** HIGH
**Why:** Team assignment is not useful without enforcement.

**Scope:**
- permission checks on audit workspace endpoints
- restrict task, findings, request list, and program access based on assignment/role

**Acceptance Criteria:**
- non-assigned users cannot access restricted audit workspace data
- assigned users can access only what their role permits
- access enforcement works consistently across key endpoints

---

### Frontend Tasks

#### 14. Add Team Assignment UI to Audit
**Priority:** MEDIUM
**Why:** Needed so the feature is actually usable.

**Scope:**
- add team members section to audit
- allow adding/removing users with role
- show current team

**Acceptance Criteria:**
- user with proper permission can assign team members to audit
- assigned roles are visible in audit UI
- team changes reflect immediately in audit workspace access

---

# EPIC 5 — Sign-off Locking and Read-Only Audit View

## Outcome
Approvals become meaningful and the audit overview stops acting like a mixed data-entry screen.

### Backend Tasks

#### 15. Create `approval_locks` table + service logic
**Priority:** HIGH
**Why:** Smallest clean implementation for post-signoff locking.

**Scope:**
- create `approval_locks`
- support audit/program step/finding/report section scope
- support lock/unlock metadata

**Acceptance Criteria:**
- approved scope can be marked locked
- locked scope blocks edits until unlocked
- lock history is stored

---

#### 16. Enforce lock-aware update rules
**Priority:** HIGH
**Why:** Table alone is not enough.

**Scope:**
- update endpoints for audits/findings/program results must check lock state
- return clear error when edit is blocked

**Acceptance Criteria:**
- locked records cannot be edited through normal endpoints
- unlock restores edit access
- blocked edit returns readable error message

---

### Frontend Tasks

#### 17. Improve existing sign-off screen to show lock state
**Priority:** MEDIUM
**Why:** Reuse current screen instead of building a new approval module.

**Scope:**
- show whether audit/section is locked
- show lock owner/time
- expose unlock request flow if permitted

**Acceptance Criteria:**
- user can see when a section is locked
- lock state is visible in sign-off flow
- UI prevents editing of locked content

---

#### 18. Make Audit View read-only overview by default
**Priority:** MEDIUM
**Why:** This aligns with the earlier MVP review and keeps execution in workspace/task screens.

**Scope:**
- reduce or remove direct edit affordances in Audit view
- keep summary cards, timeline, status, metrics, linked sections
- push editing to task/workspace/request/program screens

**Acceptance Criteria:**
- audit view acts as summary/overview page
- primary data entry happens elsewhere
- user can still navigate easily from overview to editable modules

---

# EPIC 6 — Findings / CAPA / Documents Linkage

## Outcome
Existing findings/CAPA/document features become properly connected to audit-program execution.

### Backend Tasks

#### 19. Extend `findings` to link to audit-program execution
**Priority:** MEDIUM
**Why:** Current findings are useful, but linkage is needed.

**Scope:**
- add optional link to `audit_program_step_result`
- add severity, recommendation, management response, owner, due date if missing

**Acceptance Criteria:**
- finding can be linked to a program step result
- finding retains severity and ownership metadata
- findings can still exist without program linkage if needed

---

#### 20. Extend documents/evidence linkage
**Priority:** MEDIUM
**Why:** Current document library should serve evidence and request responses.

**Scope:**
- add optional links from documents to audit, request item, and program step result
- add document type classification

**Acceptance Criteria:**
- uploaded file can be tagged as evidence or request response
- file can be linked to request item or program result
- document library can filter by document type

---

### Frontend Tasks

#### 21. Add “Create Finding from Step Result” flow
**Priority:** MEDIUM
**Why:** Simple UX bridge between execution and reporting.

**Scope:**
- from task/program result, allow create finding
- prefill relevant context

**Acceptance Criteria:**
- user can create finding directly from execution result
- finding inherits audit context automatically
- finding appears in current findings module

---

# OPTIONAL / LATER (Do Not Force Into Current Sprint)

These are useful but should not block the minimal-change MVP alignment:
- CSV import/export for audit programs
- template versioning improvements
- configurable approval hierarchy
- board-level approval workflow
- advanced risk scoring engine
- dashboard customization
- report export improvements
- notification workflow hardening

---

# Suggested Sprint Grouping

## Sprint A — Foundation
- audit_plans
- audit_plan_items
- audit_programs
- audit_program_steps
- audit_request_items

## Sprint B — Execution + access
- audit_program_step_results
- audit_team_assignments
- access enforcement
- audit program UI inside audit
- request list UI

## Sprint C — governance hardening
- approval_locks
- lock enforcement
- read-only audit view
- findings/documents linkage

---

# Short Team Message

Use this internally:

> We are not changing the MVP direction. We are only strengthening the existing screens with a small planning layer, a real audit-program layer, and a lightweight request-list layer. Execution stays in the current workspace/task flow.
