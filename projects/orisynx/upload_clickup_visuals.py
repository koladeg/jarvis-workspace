import json
import subprocess
import time
from pathlib import Path

CONFIG = "/home/claw/.openclaw/workspace/config/mcporter.json"
TEAM_ID = "9017801638"
BASE = Path("/home/claw/.openclaw/workspace/projects/orisynx")
SPACE = "GRCS Platform"
WORKSPACE = "Orisynx's Workspace"

shared = ["visual-specification.md"]

mapping = {
    "CSV/Excel Import for Audit Programs": shared,
    "Workspace Isolation & Team Access Controls": shared + ["rbac-visibility.svg", "workspace-wireframe.html"],
    "Approval Locking (Post-Sign-Off)": shared + ["approval-workflow.svg"],
    "Granular Roles & Permissions Matrix": shared + ["rbac-visibility.svg"],
    "Template Download/Export Endpoints": shared,
    "Planner: Template Activation Workflow": shared + ["calendar-planner-wireframe.html"],
    "Remove Department Involved Field": shared + ["create-audit-wireframe.html"],
    "Dashboard: Enforce Read-Only on Audit View": shared + ["audit-view-wireframe.html"],
    "Canvas Metaphor UX Redesign": shared + ["create-audit-wireframe.html", "audit-view-wireframe.html", "workspace-wireframe.html"],
    "Workspace: Unified Navigation": shared + ["workspace-wireframe.html", "workspace-workflow.svg"],
    "Audit Program as First-Class Entity": shared + ["create-audit-wireframe.html", "task-manager-wireframe.html"],
    "Approval Hierarchy (Configurable)": shared + ["approval-workflow.svg"],
    "Board-Level Approval Integration": shared + ["approval-workflow.svg"],
    "Audit Statuses & Lifecycle": shared + ["audit-lifecycle.svg"],
    "Findings Categories & Severity": shared + ["findings-capa-wireframe.html", "audit-lifecycle.svg"],
    "Evidence Attachment & Storage": shared + ["task-manager-wireframe.html", "findings-capa-wireframe.html"],
    "CAPA Tracking Workflow": shared + ["findings-capa-wireframe.html", "approval-workflow.svg", "audit-lifecycle.svg"],
    "Template Versioning & Activation": shared + ["calendar-planner-wireframe.html"],
    "Audit Team Assignment & Access": shared + ["workspace-wireframe.html", "rbac-visibility.svg"],
    "Dashboard Widgets & Customization": shared + ["audit-view-wireframe.html"],
    "Audit Report Export": shared + ["audit-view-wireframe.html"],
    "Notifications & Approvals Workflow": shared + ["approval-workflow.svg"],
    "Permission Enforcement Tests": shared + ["rbac-visibility.svg", "data-model-constraints.svg"],
}

notes = {
    "CSV/Excel Import for Audit Programs": "No standalone CSV data-flow diagram exists in the current asset bundle, so this ticket points to the overview spec's CSV import section.",
    "Workspace Isolation & Team Access Controls": "RBAC visibility diagram + workspace wireframe cover isolation, scope boundaries, and role-based visibility.",
    "Approval Locking (Post-Sign-Off)": "Approval workflow diagram shows review/lock transition points and unlock implications.",
    "Granular Roles & Permissions Matrix": "RBAC visibility diagram is the primary visual for permission boundaries.",
    "Planner: Template Activation Workflow": "Planner wireframe shows activation entry point from the calendar view.",
    "Remove Department Involved Field": "Create Audit wireframe reflects the streamlined creation flow that should exclude the removed field.",
    "Dashboard: Enforce Read-Only on Audit View": "Audit View wireframe is the primary read-only dashboard reference.",
    "Canvas Metaphor UX Redesign": "Combined create, overview, and workspace wireframes show the intended canvas-vs-workspace navigation model.",
    "Workspace: Unified Navigation": "Workspace wireframe + workflow diagram show the target consolidated navigation model.",
    "Audit Program as First-Class Entity": "Create Audit + Task Manager wireframes help anchor program structure and execution layout.",
    "Approval Hierarchy (Configurable)": "Approval workflow diagram is the best-fit visual for stage-based approver design.",
    "Board-Level Approval Integration": "Approval workflow diagram provides the closest flow reference for external approval handoffs.",
    "Audit Statuses & Lifecycle": "Audit lifecycle diagram is the primary state transition reference.",
    "Findings Categories & Severity": "Findings/CAPA wireframe plus lifecycle diagram cover finding state and disposition behavior.",
    "Evidence Attachment & Storage": "Task Manager + Findings/CAPA wireframes show likely attachment/evidence touchpoints.",
    "CAPA Tracking Workflow": "Findings/CAPA wireframe plus approval/lifecycle diagrams show the accountability chain from finding to action.",
    "Template Versioning & Activation": "Planner wireframe covers template activation entry, while the overview spec covers broader behavior.",
    "Audit Team Assignment & Access": "Workspace wireframe + RBAC diagram cover team-scoped access patterns.",
    "Dashboard Widgets & Customization": "Audit View wireframe is the closest current visual reference for dashboard composition.",
    "Audit Report Export": "Audit View wireframe is attached as the closest reporting/summary visual reference.",
    "Notifications & Approvals Workflow": "Approval workflow diagram provides the main notification/approval visual anchor.",
    "Permission Enforcement Tests": "RBAC + data constraint visuals support test coverage design for permission enforcement.",
}


def run(tool, args):
    cmd = [
        "mcporter", "call", tool,
        "--config", CONFIG,
        "--output", "json",
        "--args", json.dumps(args),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = (res.stdout or res.stderr).strip()
    return res.returncode, out

results = []
for task, files in mapping.items():
    abs_files = [str(BASE / f) for f in files]
    comment_lines = [
        "## Visual references",
        "",
        f"Attached visual assets for **{task}**:",
        "",
    ]
    for f in abs_files:
        name = Path(f).name
        if name.endswith('.svg'):
            comment_lines.append(f"- Diagram: `{f}`")
            comment_lines.append(f"  - Embed hint: `![{name}]({f})`")
        elif name.endswith('.html'):
            comment_lines.append(f"- Wireframe: `{f}`")
        else:
            comment_lines.append(f"- Overview spec: `{f}`")
    if task in notes:
        comment_lines.extend(["", f"Note: {notes[task]}"])
    comment = "\n".join(comment_lines)

    c_args = {
        "instructions": f"In workspace {WORKSPACE} and space {SPACE}, post a markdown comment on the ClickUp task named \"{task}\" describing the attached visual references.",
        "comment": comment,
        "team_id": TEAM_ID,
        "output_hint": "Return task id or confirmation only",
    }
    code, out = run("zapier-mcp.clickup_post_a_task_comment", c_args)
    task_result = {"task": task, "comment": {"ok": code == 0, "output": out}, "attachments": []}
    time.sleep(2)
    for f in abs_files:
        a_args = {
            "instructions": f"In workspace {WORKSPACE} and space {SPACE}, attach this file to the ClickUp task named \"{task}\".",
            "file": f,
            "team_id": TEAM_ID,
            "output_hint": "Return attachment confirmation only",
        }
        code, out = run("zapier-mcp.clickup_post_attachment", a_args)
        task_result["attachments"].append({"file": f, "ok": code == 0, "output": out})
        time.sleep(2)
    results.append(task_result)
    print(json.dumps(task_result, ensure_ascii=False))

summary_path = BASE / "clickup_visual_upload_results.json"
summary_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Wrote {summary_path}")
