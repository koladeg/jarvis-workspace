import json, subprocess, time
from pathlib import Path

CONFIG='/home/claw/.openclaw/workspace/config/mcporter.json'
TEAM_ID='9017801638'
BASE=Path('/home/claw/.openclaw/workspace/projects/orisynx')
WORKSPACE="Orisynx's Workspace"
SPACE='GRCS Platform'
FOLDER='No Folder'
LIST='Backlogs'

mapping={
'CSV/Excel Import for Audit Programs':['visual-specification.md'],
'Workspace Isolation & Team Access Controls':['visual-specification.md','rbac-visibility.svg','workspace-wireframe.html'],
'Approval Locking (Post-Sign-Off)':['visual-specification.md','approval-workflow.svg'],
'Granular Roles & Permissions Matrix':['visual-specification.md','rbac-visibility.svg'],
'Template Download/Export Endpoints':['visual-specification.md'],
'Planner: Template Activation Workflow':['visual-specification.md','calendar-planner-wireframe.html'],
'Remove Department Involved Field':['visual-specification.md','create-audit-wireframe.html'],
'Dashboard: Enforce Read-Only on Audit View':['visual-specification.md','audit-view-wireframe.html'],
'Canvas Metaphor UX Redesign':['visual-specification.md','create-audit-wireframe.html','audit-view-wireframe.html','workspace-wireframe.html'],
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

# discovered IDs from ClickUp list / prior executions
ids={
'CSV/Excel Import for Audit Programs':'86e0gkbx1',
'Workspace Isolation & Team Access Controls':'86e0gkc0g',
'Template Download/Export Endpoints':'86e0gkc5n',
'Workspace: Unified Navigation':'86e0gkcec',
'Audit Program as First-Class Entity':'86e0gkck4',
'Approval Hierarchy (Configurable)':'86e0gkd42',
'Board-Level Approval Integration':'86e0gkd4t',
'Audit Statuses & Lifecycle':'86e0gkd5b',
'CAPA Tracking Workflow':'86e0gkd6x',
'Template Versioning & Activation':'86e0gkd73',
'Audit Team Assignment & Access':'86e0gkd81',
'Audit Report Export':'86e0gkdc4',
'Notifications & Approvals Workflow':'86e0gkdd8',
'Permission Enforcement Tests':'86e0gkddq',
# names from list used 'and' instead of '&' for these
'Findings Categories & Severity':'86e0gkdpa',
'Evidence Attachment & Storage':'86e0gkdpp',
'Dashboard Widgets & Customization':'86e0gkdpu',
}

alias={
'Findings Categories & Severity':'Findings Categories and Severity',
'Evidence Attachment & Storage':'Evidence Attachment and Storage',
'Dashboard Widgets & Customization':'Dashboard Widgets and Customization',
'Notifications & Approvals Workflow':'Notifications and Approvals Workflow',
}

def call(tool,args):
    cmd=['mcporter','call',tool,'--config',CONFIG,'--output','json','--args',json.dumps(args)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    return r.returncode, (r.stdout or r.stderr).strip()

rows=[]
for task, files in mapping.items():
    tname=alias.get(task,task)
    task_id=ids.get(task)
    comment='## Visual references\n\n' + '\n'.join(f'- `{BASE/f}`' for f in files)
    cargs={
      'instructions': f'In workspace {WORKSPACE}, space {SPACE}, folder {FOLDER}, list {LIST}, post a markdown comment on the ClickUp task named "{tname}"' + (f' (task id {task_id})' if task_id else '') + ' describing the attached visual references.',
      'comment': comment,
      'team_id': TEAM_ID,
      'output_hint': 'Return task id only'
    }
    ccode, cout = call('zapier-mcp.clickup_post_a_task_comment',cargs)
    row={'task':task,'lookup_name':tname,'task_id':task_id,'comment_code':ccode,'comment_result':cout,'attachments':[]}
    time.sleep(2)
    for f in files:
        p=str(BASE/f)
        aargs={
          'instructions': f'In workspace {WORKSPACE}, space {SPACE}, folder {FOLDER}, list {LIST}, attach this file to the ClickUp task named "{tname}"' + (f' (task id {task_id})' if task_id else '') + '.',
          'file': p,
          'team_id': TEAM_ID,
          'output_hint': 'Return attachment confirmation only'
        }
        code, out = call('zapier-mcp.clickup_post_attachment',aargs)
        row['attachments'].append({'file':p,'code':code,'result':out})
        time.sleep(2)
    print(json.dumps(row), flush=True)
    rows.append(row)

out=BASE/'clickup_visual_upload_results_batch.json'
out.write_text(json.dumps(rows,indent=2))
print(f'WROTE {out}')
