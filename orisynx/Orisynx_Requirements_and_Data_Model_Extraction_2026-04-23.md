# Orisynx — Requirements + Data Model Extraction

Date: 2026-04-23
Source docs:
- `ABC_2025_Abridged_Audit_Plan---d90d36fd-5ac6-401e-8059-26b7c91bbe24.docx`
- `2019 TOR for Company Secretariat Department.docx`
- `2019 AUDIT REQUIREMENTS FOR COMPANY SECRETARIAT.docx`
- `TOR for Audit of Legal Department- January 2020.docx`
- `Audit Requirements -Legal Department-JAN.2020.docx`
- `Internal Control Department - Terms of Reference-July 2020.docx`
- `Internal Audit Requirements for review of Internal Control-Appendix A.docx`
- `Sample_Work_Programs_HR---4951bd79-417c-4dc9-adaa-b6ff787b7fbc.xlsx`

---

## 1) Core product insight

The documents consistently describe internal audit operations as a layered system:

1. **Annual risk-based audit planning**
2. **Audit universe / auditable entities**
3. **Per-engagement Terms of Reference (TOR)**
4. **Audit requirements / prepared-by-client request lists**
5. **Detailed work programmes** built from process → risk → control → test
6. **Fieldwork execution and evidence collection**
7. **Findings, management actions, approvals, and follow-up**
8. **Committee / board reporting and plan revision**

This strongly supports Orisynx as a platform with distinct but linked objects, not a single flat “audit” record.

---

## 2) Extracted product requirements

### A. Annual audit planning

The system should support:
- annual audit plans
- plan overview and narrative sections
- linkage to a risk assessment cycle
- allocation of audit resources (staff, duration, frequency)
- plan approval workflow (management + audit committee)
- plan revision workflow with versioning and reason tracking
- quarterly follow-up schedule support
- KPI tracking for the plan

Fields implied by source docs:
- plan year
- organisation / group
- plan status
- approval status
- approved date
- effective date range
- staffing assumptions
- resource allocation percentages
- top enterprise risks included
- methodology reference
- revision triggers/reasons
- key performance metrics

### B. Audit universe management

The system should model the audit universe as a registry of auditable entities:
- divisions / groups / departments / units
- residual risk ranking per entity
- risk category / severity
- audit frequency rules
- default fieldwork duration
- process inventory under each entity
- history of prior audits

Fields implied:
- auditable entity name
- entity type
- parent entity
- risk severity (critical/high/medium/low)
- residual risk score/value
- default frequency
- default duration
- business owner
- regulator / compliance relevance
- active/inactive status

### C. Engagement / audit setup

Each planned audit engagement should support:
- engagement title
- business unit / auditable entity
- audit type (full audit, advisory, investigation, follow-up)
- start/end dates
- opening meeting / entrance meeting
- audit objectives
- rationale
- scope period
- in-scope areas
- out-of-scope areas
- milestones (fieldwork, draft report, final report)
- report distribution list
- team assignment
- auditee cooperation requests
- remote vs onsite execution mode

This maps closely to a structured **TOR object**.

### D. Terms of Reference (TOR)

TORs should be a first-class object, not just an attachment.

The system should support structured TOR sections:
- introduction/background
- objectives
- rationale
- scope/approach
- risk types
- process classifications
- control framework components
- in-scope topics table
- out-of-scope notes
- distribution list
- milestones
- appendix links

### E. Audit requirements / client request lists

The “audit requirements” documents show the need for a separate object for information requests.

The system should support:
- document request lists tied to an engagement or TOR
- categorised request groups (e.g. litigation, administration, collateral, governance)
- request status tracking
- due dates
- upload / shared folder delivery
- received / pending / partial / not applicable statuses
- request source (planned vs ad hoc)
- ability to mark list as non-exhaustive and add requests during fieldwork

### F. Work programme engine

This is the most important data-model clue from the HR spreadsheet.

The system should support hierarchical work programmes containing:
- work programme header
- objectives
- process
- sub-process hierarchy
- risk statements
- risk priority and scoring
- controls linked to each risk
- tests linked to each control
- answer scales for controls/tests
- guidance notes to auditor
- evidence references
- exception counts / scoring
- versioning and approval status

The HR sample implies the canonical chain:

**Work Programme → Process → Subprocess → Risk → Control → Test → Evidence / Result**

### G. Risk model and scoring

The documents consistently require:
- risk identification
- risk type classification
- impact and likelihood scoring
- residual risk assessment
- severity/ranking buckets
- premium weighting for special risk classes (e.g. regulatory, fraud, credit)
- enterprise risk to audit-plan linkage

The product should support:
- configurable risk matrices
- severity legends
- residual vs inherent risk
- risk-based audit scheduling
- aggregation of risks from engagement/work-programme level to plan level

### H. Control framework assessment

The sources repeat standard framework dimensions such as:
- control environment
- risk assessment
- control activities
- information & communication
- monitoring
- effectiveness of operational processes

The system should support tagging topics/findings/work steps against control framework components.

### I. Fieldwork execution

The docs imply a real execution layer with:
- auditor working papers
- interviews / observations / document reviews
- sampling notes
- evidence attachments
- issue logging during fieldwork
- communication of control weaknesses during the audit
- supervisory review of working papers

### J. Findings, ratings, and reports

The system should support:
- finding capture during or after fieldwork
- severity rating (high / medium / low / process improvement)
- linkage to risk and control failures
- management response collection
- agreed action plans
- ownership and target dates
- draft report review cycle
- exit meeting / acceptance workflow
- final report sign-off
- permanent audit file archival

The docs also imply a **composite engagement rating** driven by exception distribution.

### K. Follow-up and remediation tracking

The documents explicitly mention quarterly follow-up.

The platform should support:
- follow-up reviews
- recommendation implementation status
- evidence of remediation
- overdue actions
- audit committee updates on critical/high findings
- revalidation testing

### L. Governance / committee reporting

The system should support:
- management review
- audit committee approval of annual plans
- quarterly committee reporting
- distribution-controlled report access
- board / committee packs

### M. Versioning and libraries

Repeated version clues:
- work programme versions (e.g. version 19, version 17, version 11)
- annual plan revisions
- TOR issuance dates
- updated SOPs / SOMs

Orisynx should include:
- template library for TORs, requirements lists, work programmes
- version history
- clone-from-template
- controlled approvals before use

---

## 3) Recommended object model

### Top-level entities

1. **Organisation**
2. **Business Unit / Auditable Entity**
3. **Audit Universe Entry**
4. **Risk Register Item**
5. **Annual Audit Plan**
6. **Plan Audit Project / Planned Engagement**
7. **Audit Engagement**
8. **Terms of Reference**
9. **Audit Requirement Request List**
10. **Work Programme**
11. **Work Programme Step Tree**
12. **Working Paper / Evidence Item**
13. **Finding / Observation**
14. **Management Action / Remediation Item**
15. **Follow-Up Review**
16. **Report**
17. **Approval / Sign-Off**
18. **User / Role / Team Assignment**

---

## 4) Recommended relational structure

### 4.1 Organisation / structure

#### organisations
- id
- name
- short_code
- status
- created_at
- updated_at

#### business_units
- id
- organisation_id
- parent_business_unit_id
- name
- code
- type (group/division/department/unit/process owner area)
- executive_owner_id
- status
- created_at
- updated_at

#### auditable_entities
- id
- organisation_id
- business_unit_id
- name
- description
- entity_type
- default_frequency
- default_fieldwork_days
- residual_risk_rating
- residual_risk_score
- active
- created_at
- updated_at

### 4.2 Risk model

#### risk_register_items
- id
- organisation_id
- business_unit_id
- title
- description
- risk_type
- category
- inherent_impact
- inherent_likelihood
- inherent_score
- residual_impact
- residual_likelihood
- residual_score
- severity
- source_date
- status
- created_at
- updated_at

#### risk_matrix_schemes
- id
- organisation_id
- name
- version
- definition_json
- active

### 4.3 Planning

#### audit_plans
- id
- organisation_id
- year
- title
- overview
- methodology_summary
- staffing_assumptions
- resource_allocation_notes
- status
- approved_by_id
- approved_at
- effective_from
- effective_to
- created_at
- updated_at

#### audit_plan_projects
- id
- audit_plan_id
- auditable_entity_id
- title
- planned_quarter
- planned_start_date
- planned_end_date
- planned_fieldwork_days
- risk_rating
- status
- rationale
- created_at
- updated_at

#### audit_plan_revisions
- id
- audit_plan_id
- version
- revision_reason
- requested_by_id
- approved_by_id
- approved_at
- notes

### 4.4 Engagement execution

#### audit_engagements
- id
- audit_plan_project_id nullable
- organisation_id
- auditable_entity_id
- title
- audit_type
- engagement_mode (onsite/remote/hybrid)
- scope_start_date
- scope_end_date
- start_date
- end_date
- opening_meeting_at
- exit_meeting_at
- status
- overall_rating
- created_at
- updated_at

#### engagement_team_members
- id
- audit_engagement_id
- user_id
- role (engagement_manager/team_lead/team_member/reviewer/approver)
- assigned_at

### 4.5 TOR

#### terms_of_reference
- id
- audit_engagement_id
- issued_date
- background
- objectives
- rationale
- scope_approach
- risk_types_json
- process_classifications_json
- control_framework_components_json
- out_of_scope
- fieldwork_start_date
- fieldwork_end_date
- draft_report_due_date
- final_report_due_date
- version
- status
- created_at
- updated_at

#### tor_scope_topics
- id
- terms_of_reference_id
- ref_no
- topic
- scope_area
- risk_description
- risk_type
- process_category
- notes

#### tor_distribution_list
- id
- terms_of_reference_id
- user_id nullable
- external_name
- title
- business_unit
- receives_draft
- receives_final

### 4.6 Audit requests / PBC lists

#### audit_request_lists
- id
- audit_engagement_id
- terms_of_reference_id nullable
- title
- description
- version
- status
- due_date
- created_at
- updated_at

#### audit_request_items
- id
- audit_request_list_id
- category
- item_text
- required_format
- priority
- status
- requested_at
- due_at
- received_at
- received_by_id
- notes

### 4.7 Work programmes

#### work_programmes
- id
- organisation_id
- auditable_entity_id nullable
- audit_engagement_id nullable
- title
- notes
- objectives
- status
- version
- inherent_risk_score
- process_name
- sub_process_name
- created_from_template_id nullable
- approved_by_id nullable
- approved_at nullable
- created_at
- updated_at

#### work_programme_risks
- id
- work_programme_id
- process
- sub_process
- sub_sub_process
- sub_sub_sub_process
- risk_statement
- risk_priority
- inherent_risk
- impact
- likelihood
- weighting
- exception_count
- text_field_caption nullable
- created_at
- updated_at

#### work_programme_controls
- id
- work_programme_risk_id
- control_statement
- control_type
- answer_scale_json
- weighting
- exception_count
- created_at
- updated_at

#### work_programme_tests
- id
- work_programme_control_id
- test_statement
- answer_scale_json
- auditor_guidance
- evidential_reference_prompt
- weighting
- exception_count
- created_at
- updated_at

#### work_programme_test_results
- id
- work_programme_test_id
- audit_engagement_id
- sample_reference
- result_value
- result_notes
- exception_flag
- completed_by_id
- reviewed_by_id
- completed_at
- reviewed_at

### 4.8 Evidence / working papers

#### evidence_items
- id
- audit_engagement_id
- work_programme_test_result_id nullable
- audit_request_item_id nullable
- file_name
- file_url
- evidence_type
- source
- uploaded_by_id
- uploaded_at
- notes

#### working_papers
- id
- audit_engagement_id
- title
- description
- linked_risk_id nullable
- linked_control_id nullable
- linked_test_id nullable
- prepared_by_id
- reviewed_by_id
- status
- created_at
- updated_at

### 4.9 Findings and remediation

#### audit_findings
- id
- audit_engagement_id
- tor_scope_topic_id nullable
- work_programme_test_result_id nullable
- title
- description
- risk_type
- severity
- likelihood
- impact
- rating_score
- control_framework_component
- root_cause
- recommendation
- management_response
- owner_user_id nullable
- owner_business_unit_id nullable
- due_date
- status
- created_at
- updated_at

#### management_actions
- id
- audit_finding_id
- action_text
- owner_user_id
- target_date
- completion_date nullable
- status
- evidence_summary
- created_at
- updated_at

#### follow_up_reviews
- id
- audit_engagement_id nullable
- audit_finding_id nullable
- review_date
- reviewer_id
- status
- validation_result
- notes

### 4.10 Reports and sign-off

#### audit_reports
- id
- audit_engagement_id
- type (draft/final/follow_up/committee_pack)
- title
- issued_at
- overall_rating
- summary
- file_url nullable
- status

#### approvals
- id
- object_type
- object_id
- stage
- approver_id
- decision
- comments
- approved_at

---

## 5) Key workflow derived from the source materials

### Workflow A — Annual planning
1. Maintain audit universe
2. Pull latest risk assessment / risk register
3. Rank auditable entities by residual risk
4. Generate annual audit plan
5. Allocate timing, frequency, and duration
6. Submit for management review
7. Submit to audit committee for approval
8. Revise as needed during the year with version history

### Workflow B — Audit execution
1. Convert planned project into engagement
2. Generate TOR from template
3. Create request list / required documents list
4. Assign team and milestones
5. Prepare or clone work programme
6. Perform fieldwork and upload evidence
7. Capture findings and management responses
8. Hold exit meeting and finalize report
9. Launch follow-up items
10. Report critical/high findings to committee

### Workflow C — Work programme execution
1. Select process/sub-process
2. Define risk
3. link control
4. define test
5. provide auditor guidance
6. capture evidence and result
7. count exceptions
8. roll up to findings and report ratings

---

## 6) Important design decisions for Orisynx

1. **Separate annual plan from engagement execution**
   - planning and execution are linked but not the same object.

2. **Make TOR structured, not just uploaded**
   - the source docs are highly structured and should be queryable.

3. **Make request lists first-class**
   - “audit requirements” recur across every engagement.

4. **Use a hierarchical work-programme model**
   - a flat checklist will be too weak.

5. **Support reusable templates and versioning**
   - repeated department audits clearly reuse and revise templates.

6. **Separate evidence, findings, and actions**
   - evidence proves testing, findings describe breakdowns, actions track remediation.

7. **Include configurable risk matrices**
   - different clients may score differently.

8. **Preserve audit-trail and sign-off history**
   - approvals and report distribution are core governance requirements.

---

## 7) MVP recommendation

If Orisynx is still narrowing scope, MVP should include:
- Audit Universe
- Annual Audit Plan
- Audit Engagement
- TOR Builder
- Audit Request List
- Work Programme Builder
- Evidence Upload
- Findings + Management Actions
- Follow-up Tracker
- Role-based access and approvals

Can wait until phase 2:
- advanced analytics
- committee deck automation
- complex scoring engines
- cross-engagement benchmarking
- external auditor collaboration

---

## 8) Frontend IA suggestion

Recommended top nav:
- Dashboard
- Plans
- Universe
- Engagements
- Work Programmes
- Findings
- Follow-ups
- Reports
- Templates
- Admin

Inside each engagement:
- Overview
- TOR
- Request List
- Work Programme
- Fieldwork / Working Papers
- Findings
- Report
- Follow-up

---

## 9) Immediate next artifacts to generate

Best next outputs from this extraction:
1. ERD / schema diagram
2. API resource design
3. backend ticket breakdown
4. frontend screen map
5. migration of current product screens into this model
