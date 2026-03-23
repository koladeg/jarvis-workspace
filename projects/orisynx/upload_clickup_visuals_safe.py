import json, subprocess, time
from pathlib import Path
CONFIG='/home/claw/.openclaw/workspace/config/mcporter.json'
TEAM_ID='9017801638'
BASE=Path('/home/claw/.openclaw/workspace/projects/orisynx')
WORKSPACE="Orisynx's Workspace"
SPACE='GRCS Platform'

mapping={
'CSV/Excel Import for Audit Programs':['visual-specification.md'],
'Workspace Isolation & Team Access Controls':['visual-specification.md','rbac-visibility.svg','workspace-wireframe.html'],
'Template Download/Export Endpoints':['visual-specification.md'],
'Workspace: Unified Navigation':['visual-specification.md','workspace-wireframe.html','workspace-workflow.svg'],
'Audit Program as First-Class Entity':['visual-specification.md','create-audit-wireframe.html','task-manager-wireframe.html'],
'Approval Hierarchy (Configurable)':['visual-specification.md','approval-workflow.svg'],
'Board-Level Approval Integration':['visual-specification.md','approval-workflow.svg'],
'Audit Statuses & Lifecycle':['visual-specification.md','audit-lifecycle.svg'],
'Findings Categories & Severity':['visual-specification.md','findings-capa-wireframe.html','audit-lifecycle.svg'],
'Evidence Attachment & Storage':['visual-specification.md','task-manager-wireframe.html','findings-capa-wireframe.html'],
'CAPA Tracking Workflow':['visual-specification.md','findings-capa-wireframe.html','approval-workflow.svg','audit-lifecycle.svg'],
'Template Versioning & Activation':['visual-specification.md','calendar-planner-wireframe.html'],
'Audit Team Assignment & Access':['visual-specification.md','workspace-wireframe.html','rbac-visibility.svg'],
'Dashboard Widgets & Customization':['visual-specification.md','audit-view-wireframe.html'],
'Audit Report Export':['visual-specification.md','audit-view-wireframe.html'],
'Notifications & Approvals Workflow':['visual-specification.md','approval-workflow.svg'],
'Permission Enforcement Tests':['visual-specification.md','rbac-visibility.svg','data-model-constraints.svg'],
}


def call(tool,args):
    cmd=['mcporter','call',tool,'--config',CONFIG,'--output','json','--args',json.dumps(args)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    return (r.stdout or r.stderr).strip()

rows=[]
for task, files in mapping.items():
    paths=[str(BASE/f) for f in files]
    comment='## Visual references\n\n' + '\n'.join(f'- `{p}`' for p in paths)
    cargs={
      'instructions': f'In workspace {WORKSPACE} and space {SPACE}, post a markdown comment on the ClickUp task named "{task}" describing the attached visual references.',
      'comment': comment,
      'team_id': TEAM_ID,
      'output_hint': 'Return task id only'
    }
    c=call('zapier-mcp.clickup_post_a_task_comment',cargs)
    row={'task':task,'comment':c,'attachments':[]}
    time.sleep(1)
    for p in paths:
        aargs={
          'instructions': f'In workspace {WORKSPACE} and space {SPACE}, attach this file to the ClickUp task named "{task}".',
          'file': p,
          'team_id': TEAM_ID,
          'output_hint': 'Return attachment confirmation only'
        }
        row['attachments'].append({'file':p,'result':call('zapier-mcp.clickup_post_attachment',aargs)})
        time.sleep(1)
    print(json.dumps(row))
    rows.append(row)

out=BASE/'clickup_visual_upload_results_safe.json'
out.write_text(json.dumps(rows,indent=2))
print(f'WROTE {out}')
