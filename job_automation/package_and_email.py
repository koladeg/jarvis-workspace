#!/usr/bin/env python3
"""Bundle job application packages and send a summary email.

Environment variables used:
- JOB_AUTOMATION_EMAIL_FROM
- JOB_AUTOMATION_EMAIL_TO
- JOB_AUTOMATION_SMTP_HOST
- JOB_AUTOMATION_SMTP_PORT (default: 587)
- JOB_AUTOMATION_SMTP_USERNAME
- JOB_AUTOMATION_SMTP_PASSWORD
- JOB_AUTOMATION_SMTP_TLS (default: true)
"""

from __future__ import annotations

import os
import smtplib
import zipfile
from email.message import EmailMessage
from pathlib import Path
from typing import List

from db import DB_PATH, fetch_jobs, get_connection, initialize_database, mark_email_sent

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
BUNDLE_DIR = OUTPUT_DIR / "bundles"
BUNDLE_PATH = BUNDLE_DIR / "job_application_packages.zip"



def create_bundle() -> tuple[Path, List[dict]]:
    initialize_database(DB_PATH)
    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    with get_connection(DB_PATH) as conn:
        jobs = [dict(row) for row in fetch_jobs(conn, limit=200)]

    package_jobs = [job for job in jobs if job.get("package_dir")]
    with zipfile.ZipFile(BUNDLE_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for job in package_jobs:
            package_dir = Path(job["package_dir"])
            if not package_dir.exists():
                continue
            for file_path in package_dir.rglob("*"):
                if file_path.is_file():
                    archive.write(file_path, arcname=file_path.relative_to(OUTPUT_DIR))
    return BUNDLE_PATH, package_jobs



def build_email(bundle_path: Path, jobs: List[dict]) -> EmailMessage:
    sender = os.environ["JOB_AUTOMATION_EMAIL_FROM"]
    recipient = os.environ["JOB_AUTOMATION_EMAIL_TO"]

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"Weekly job application package bundle ({len(jobs)} jobs)"

    lines = [
        "Hi,",
        "",
        f"Attached is the latest application bundle containing {len(jobs)} tailored job packages.",
        "",
        "Included jobs:",
    ]
    for job in jobs[:50]:
        lines.append(f"- {job['company']} | {job['role']} | {job['url']}")
    lines.extend(["", "Regards,", "Job Automation Bot"])
    msg.set_content("\n".join(lines))

    msg.add_attachment(
        bundle_path.read_bytes(),
        maintype="application",
        subtype="zip",
        filename=bundle_path.name,
    )
    return msg



def send_email(msg: EmailMessage) -> None:
    host = os.environ["JOB_AUTOMATION_SMTP_HOST"]
    port = int(os.environ.get("JOB_AUTOMATION_SMTP_PORT", "587"))
    username = os.environ.get("JOB_AUTOMATION_SMTP_USERNAME")
    password = os.environ.get("JOB_AUTOMATION_SMTP_PASSWORD")
    use_tls = os.environ.get("JOB_AUTOMATION_SMTP_TLS", "true").lower() != "false"

    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.ehlo()
        if use_tls:
            smtp.starttls()
            smtp.ehlo()
        if username and password:
            smtp.login(username, password)
        smtp.send_message(msg)



def main() -> int:
    bundle_path, jobs = create_bundle()
    if not jobs:
        print("No packaged jobs found. Run generate_documents.py first.")
        return 1

    msg = build_email(bundle_path, jobs)
    send_email(msg)

    with get_connection(DB_PATH) as conn:
        mark_email_sent(conn, [job["job_id"] for job in jobs])

    print(f"Sent email with {len(jobs)} job packages attached: {bundle_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
