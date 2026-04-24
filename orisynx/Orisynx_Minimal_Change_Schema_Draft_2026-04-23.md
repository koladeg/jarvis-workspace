# Orisynx — Minimal-Change Schema Draft

Date: 2026-04-23
Purpose: integrate the newly shared audit documents into the current Orisynx MVP with the least disruptive product/schema changes.

---

## 1) Principle

Do **not** redesign the MVP.

Instead:
- reuse current screens
- extend current entities carefully
- introduce only a few missing first-class objects
- align additions with the already identified ClickUp backlog

---

## 2) Current MVP foundation to preserve

Existing screen foundation already maps reasonably well:

- **Calendar page** → planner base
- **Task manager / Task view** → workspace execution base
- **Audit view** → audit overview / dashboard base
- **Document review and sign off** → approval base
- **Templates manager / Create template** → template base
- **Users / Edit user** → roles base
- **Findings** → observation/finding base
- **CAPA tracker** → follow-up / remediation base
- **Document library** → evidence/doc repository base
- **Reports / Analytics** → reporting base

So the schema should bend toward these screens instead of replacing them.

---

## 3) Minimal new/extended object model

### Keep existing core audit object
Assume current MVP already has some kind of `audit` or `engagement` entity.

Do not split this too aggressively yet.

### Add only these missing first-class concepts
1. **audit_plan**
2. **audit_program**
3. **audit_request_item**
4. **approval_lock**
5. **audit_team_assignment**

Everything else should be extensions of likely-existing structures.

---

## 4) Recommended schema changes

## A. Extend existing `audits` table/entity

Add fields to support what the docs require without creating a totally separate TOR engine yet.

### audits
Add fields like:
- id
- title
- audit_type
- business_unit_id
- planned_from
- planned_to
- scope_start_date
- scope_end_date
- status
- risk_rating
- objective_summary
- rationale
- audit_view_mode (`overview` default)
- is_read_only_overview (`true` after new rule)
- created_from_template_id nullable
- audit_plan_id nullable
- lead_user_id nullable
- approval_status
- approved_at nullable
- created_at
- updated_at

### Why
This preserves current "Create audit / Audit view" flows while letting each audit carry more TOR-style information.

---

## B. Add `audit_plans`

Use this to back the planner/calendar more properly, but keep it simple.

### audit_plans
- id
- year
- title
- overview
- methodology_notes
- status
- approved_by_id nullable
- approved_at nullable
- version
- created_at
- updated_at

### audit_plan_items
- id
- audit_plan_id
- business_unit_id
- title
- quarter nullable
- scheduled_start nullable
- scheduled_end nullable
- risk_rating nullable
- expected_duration_days nullable
- template_id nullable
- activation_status (`planned`, `activated`, `completed`)
- linked_audit_id nullable
- created_at
- updated_at

### Why
This supports the already-planned **template activation from calendar** without restructuring the whole product.

---

## C. Add `audit_programs`

This is the most important missing concept.

Do **not** create a huge enterprise GRC hierarchy yet.

Instead, make one practical work-program object that can connect to templates, tasks, findings, and uploads.

### audit_programs
- id
- audit_id
- template_id nullable
- name
- notes
- objectives
- process_name nullable
- sub_process_name nullable
- version
- status
- imported_from_file nullable
- created_at
- updated_at

### audit_program_steps
- id
- audit_program_id
- parent_step_id nullable
- step_type (`risk`, `control`, `test`, `section`)
- title
- description nullable
- risk_priority nullable
- impact_score nullable
- likelihood_score nullable
- weighting nullable
- answer_options_json nullable
- guidance_notes nullable
- evidence_prompt nullable
- sort_order
- created_at
- updated_at

### audit_program_step_results
- id
- audit_program_step_id
- audit_id
- assigned_to_id nullable
- result_status nullable
- score nullable
- notes nullable
- exception_count default 0
- completed_at nullable
- reviewed_at nullable
- created_at
- updated_at

### Why
This is enough to support the HR-style structure:
- process
- risk
- control
- test
- notes to auditor
- evidence reference

without forcing a very complex normalized design in MVP.

---

## D. Add `audit_request_items`

The documents clearly show pre-fieldwork requirement lists.

You do not need a separate giant request module. Just make request items belong to an audit.

### audit_request_items
- id
- audit_id
- category nullable
- title
- description nullable
- required_format nullable
- status (`pending`, `received`, `partial`, `not_applicable`)
- due_date nullable
- uploaded_document_id nullable
- notes nullable
- created_at
- updated_at

### Why
This fits naturally into current document library / audit setup flows.

---

## E. Add `audit_team_assignments`

This supports workspace isolation and per-audit access without overhauling auth.

### audit_team_assignments
- id
- audit_id
- user_id
- role (`audit_manager`, `team_lead`, `auditor`, `reviewer`)
- created_at
- updated_at

### Why
This directly supports the existing ClickUp item around workspace/team isolation.

---

## F. Add `approval_locks`

This is the smallest reliable way to implement sign-off locking.

### approval_locks
- id
- audit_id
- lock_scope (`audit`, `program_step`, `finding`, `report_section`)
- scoped_id nullable
- locked_by_id
- locked_at
- unlock_requested_by_id nullable
- unlocked_by_id nullable
- unlocked_at nullable
- status (`locked`, `unlocked`)
- notes nullable

### Why
It gives you post-signoff edit control without rewriting the whole approval system.

---

## G. Reuse existing likely entities with small extensions

### findings
Add if missing:
- audit_program_step_result_id nullable
- severity
- root_cause nullable
- recommendation nullable
- management_response nullable
- owner_user_id nullable
- due_date nullable
- status

### capa_actions
Add if missing:
- finding_id
- action_text
- owner_user_id
- target_date
- completion_date nullable
- validation_notes nullable
- status

### documents
Add if missing:
- audit_id nullable
- audit_request_item_id nullable
- audit_program_step_result_id nullable
- document_type (`evidence`, `request_response`, `report_attachment`, `template`)

---

## 5) How this maps to current screens

## Calendar page
No redesign.
Just power it with:
- `audit_plans`
- `audit_plan_items`
- activate audit from plan item

## Audit view
Keep it.
But reposition as:
- overview / dashboard / summary screen
- read-only for approved or structured summary data
- no heavy data entry here

## Task manager / Task view
Use it as the execution face of:
- `audit_program_steps`
- `audit_program_step_results`
- assigned work

## Templates manager
Reuse for:
- audit templates
- audit program templates
- downloadable/importable CSV templates later

## Document library
Reuse for:
- audit requests fulfilled
- evidence uploads
- report attachments

## Document review and sign off
Enhance with:
- `approval_locks`

## Findings / CAPA
Keep structure.
Just link them back to program step results.

---

## 6) What NOT to introduce yet

To avoid blowing up the MVP, do **not** add all of these now:
- separate TOR microservice/module
- deeply normalized risk register engine
- committee governance workflow engine
- advanced multi-level board approval routing
- complex scoring/rules engine
- highly abstract control framework taxonomy tables
- full enterprise audit universe management tree beyond what current org/unit structure can support

These can come later.

---

## 7) Minimal implementation sequence

### Phase 1 — smallest useful schema additions
1. add `audit_plans`
2. add `audit_plan_items`
3. add `audit_programs`
4. add `audit_program_steps`
5. add `audit_request_items`

### Phase 2 — execution hardening
6. add `audit_team_assignments`
7. add `approval_locks`
8. link findings/documents to program results

### Phase 3 — UX tightening
9. make audit view read-only overview
10. unify workspace navigation across task manager/findings/documents
11. add CSV import/export for audit programs

---

## 8) Updated MVP interpretation

With minimal change, Orisynx MVP becomes:

- **Planner** = Calendar + Audit Plans
- **Audit** = main engagement record
- **Audit Program** = structured checklist/work-program inside an audit
- **Workspace** = task manager + documents + findings + CAPA
- **Approvals** = signoff + lock

That is close to the current product and close to the source documents.

---

## 9) Recommendation to team

Pitch this internally as:

> “We are not changing the MVP direction. We are only formalizing three weak spots the source documents exposed: planning, audit programs, and request lists.”

That framing should reduce resistance and keep ClickUp execution aligned.

---

## 10) Next best artifact

Next useful deliverable:
- a **field-by-field migration checklist** mapped to current backend/frontend screens
- or a **ClickUp-friendly implementation breakdown** grouped into backend/frontend tickets
