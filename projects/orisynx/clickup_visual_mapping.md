# Orisynx ClickUp Visual Asset Mapping

Base directory: `/home/claw/.openclaw/workspace/projects/orisynx`

## Shared asset attached to all 23 tickets
- `visual-specification.md` — comprehensive visual/UX overview and ticket cross-reference

## Ticket → asset mapping

| Ticket | Assets |
|---|---|
| CSV/Excel Import for Audit Programs | `visual-specification.md` *(overview; CSV section)* |
| Workspace Isolation & Team Access Controls | `visual-specification.md`, `rbac-visibility.svg`, `workspace-wireframe.html` |
| Approval Locking (Post-Sign-Off) | `visual-specification.md`, `approval-workflow.svg` |
| Granular Roles & Permissions Matrix | `visual-specification.md`, `rbac-visibility.svg` |
| Template Download/Export Endpoints | `visual-specification.md` |
| Planner: Template Activation Workflow | `visual-specification.md`, `calendar-planner-wireframe.html` |
| Remove Department Involved Field | `visual-specification.md`, `create-audit-wireframe.html` |
| Dashboard: Enforce Read-Only on Audit View | `visual-specification.md`, `audit-view-wireframe.html` |
| Canvas Metaphor UX Redesign | `visual-specification.md`, `create-audit-wireframe.html`, `audit-view-wireframe.html`, `workspace-wireframe.html` |
| Workspace: Unified Navigation | `visual-specification.md`, `workspace-wireframe.html`, `workspace-workflow.svg` |
| Audit Program as First-Class Entity | `visual-specification.md`, `create-audit-wireframe.html`, `task-manager-wireframe.html` |
| Approval Hierarchy (Configurable) | `visual-specification.md`, `approval-workflow.svg` |
| Board-Level Approval Integration | `visual-specification.md`, `approval-workflow.svg` |
| Audit Statuses & Lifecycle | `visual-specification.md`, `audit-lifecycle.svg` |
| Findings Categories & Severity | `visual-specification.md`, `findings-capa-wireframe.html`, `audit-lifecycle.svg` |
| Evidence Attachment & Storage | `visual-specification.md`, `task-manager-wireframe.html`, `findings-capa-wireframe.html` |
| CAPA Tracking Workflow | `visual-specification.md`, `findings-capa-wireframe.html`, `approval-workflow.svg`, `audit-lifecycle.svg` |
| Template Versioning & Activation | `visual-specification.md`, `calendar-planner-wireframe.html` |
| Audit Team Assignment & Access | `visual-specification.md`, `workspace-wireframe.html`, `rbac-visibility.svg` |
| Dashboard Widgets & Customization | `visual-specification.md`, `audit-view-wireframe.html` |
| Audit Report Export | `visual-specification.md`, `audit-view-wireframe.html` |
| Notifications & Approvals Workflow | `visual-specification.md`, `approval-workflow.svg` |
| Permission Enforcement Tests | `visual-specification.md`, `rbac-visibility.svg`, `data-model-constraints.svg` |

## Notes
- No standalone `data-flow` SVG/file was present in the asset bundle. For the CSV import ticket, I referenced the overview specification section covering CSV import.
- Data model references are primarily covered by `data-model-erd.svg` and `data-model-constraints.svg`; these are especially relevant to implementation/testing tickets even when not explicitly requested in the original mapping.
