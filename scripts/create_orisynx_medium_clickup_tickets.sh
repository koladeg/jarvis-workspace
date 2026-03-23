#!/usr/bin/env bash
set -euo pipefail

CONFIG="/home/claw/.openclaw/workspace/config/mcporter.json"
export CONFIG

python3 <<'PY'
import json
import os
import subprocess
import time

config = os.environ["CONFIG"]
workspace = "Orisynx's Workspace"
space = "GRCS Platform"
folder = "No Folder"
output_hint = "Return created task id, name, url, and priority only."

tickets = [
    ("Approval Hierarchy (Configurable)", "Audit Owner assigns Approval Authorities per audit. Support multi-level approvals if needed. Configuration at audit creation stage."),
    ("Board-Level Approval Integration", "Support external board approval document attachment (PDF upload). Does not require in-system workflow, just document storage link."),
    ("Audit Statuses & Lifecycle", "Define audit statuses: Planned → Active → In Review → Approved → Closed. Implement status transitions with validation rules."),
    ("Findings Categories & Severity", "Support finding categories (control gaps, observations, recommendations, custom). Allow severity/impact levels. Track status (open, resolved, closed)."),
    ("Evidence Attachment & Storage", "Files can be attached to tests/tasks. Define file size limits, storage backend (S3 vs local), file type restrictions. Link evidence directly to specific tests."),
    ("CAPA Tracking Workflow", "Link CAPAs to findings. Track owner, due date, status. Support follow-up/remediation tracking. Integration with findings lifecycle."),
    ("Template Versioning & Activation", "Templates can have versions. Audits created from specific template versions. Support template updates without affecting active audits."),
    ("Audit Team Assignment & Access", "Assign multiple team members to audit. Define roles per team member (Lead, Auditor, Reviewer). Team-level permissions."),
    ("Dashboard Widgets & Customization", "Dashboard shows audit status, findings summary, CAPA status, timeline. Allow users to customize widget visibility per user."),
    ("Audit Report Export", "Generate audit reports (PDF/Word) with findings, evidence links, approvals history. Support custom templates."),
    ("Notifications & Approvals Workflow", "Notify Team Leads when work awaits approval. Notify Audit Owner when findings raised. Email notifications on status changes."),
    ("Permission Enforcement Tests", "Unit/integration tests for granular permissions. Test cross-audit isolation. Test role-based UI visibility."),
]

for name, content in tickets:
    instructions = (
        f"Create a ClickUp task in workspace {workspace}, space {space}, folder {folder}. "
        f"Task name: {name}. Task description: {content} "
        f"Set priority to Normal to represent MEDIUM priority in the backlog."
    )
    args = {
        "instructions": instructions,
        "output_hint": output_hint,
    }
    print(f"=== Creating: {name} ===", flush=True)
    proc = subprocess.run(
        [
            "mcporter", "call", "zapier-mcp.clickup_create_task",
            "--config", config,
            "--output", "json",
            "--args", json.dumps(args),
        ],
        capture_output=True,
        text=True,
    )
    if proc.stdout:
        print(proc.stdout.rstrip())
    if proc.stderr:
        print(proc.stderr.rstrip())
    print("__SUCCESS__" if proc.returncode == 0 else f"__FAILURE__:{proc.returncode}")
    print()
    time.sleep(1)
PY
