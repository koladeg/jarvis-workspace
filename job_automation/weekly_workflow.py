#!/usr/bin/env python3
"""Orchestrate the full weekly job search workflow.

Suggested cron entry (runs every Monday at 08:00 UTC):
0 8 * * 1 /usr/bin/python3 /home/claw/.openclaw/workspace/job_automation/weekly_workflow.py >> /home/claw/.openclaw/workspace/job_automation/output/weekly_workflow.log 2>&1
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "db.py",
    "parse_jobs.py",
    "generate_documents.py",
    "package_and_email.py",
]



def run_script(script_name: str) -> None:
    script_path = BASE_DIR / script_name
    print(f"\n>>> Running {script_path.name}")
    subprocess.run([sys.executable, str(script_path)], check=True)



def main() -> int:
    for script in SCRIPTS:
        run_script(script)
    print("\nWeekly workflow completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
