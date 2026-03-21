# Job Automation System

Files included:

- `db.py` — creates SQLite schema for jobs + application tracking
- `parse_jobs.py` — fetches up to 50 jobs from RemoteOK and Hacker News, extracts tech stack, deduplicates, stores in SQLite
- `generate_documents.py` — creates tailored CV and cover letter PDFs for each job
- `package_and_email.py` — zips all job packages and emails them via SMTP
- `weekly_workflow.py` — runs the full workflow end-to-end for weekly automation

## Quick start

```bash
cd /home/claw/.openclaw/workspace/job_automation
python3 db.py
python3 parse_jobs.py 50
python3 generate_documents.py
python3 package_and_email.py
```

Or run everything:

```bash
python3 weekly_workflow.py
```

## SMTP environment variables

```bash
export JOB_AUTOMATION_EMAIL_FROM="you@example.com"
export JOB_AUTOMATION_EMAIL_TO="you@example.com"
export JOB_AUTOMATION_SMTP_HOST="smtp.example.com"
export JOB_AUTOMATION_SMTP_PORT="587"
export JOB_AUTOMATION_SMTP_USERNAME="smtp-user"
export JOB_AUTOMATION_SMTP_PASSWORD="smtp-password"
export JOB_AUTOMATION_SMTP_TLS="true"
```

## Output

Generated files are placed under:

- `data/jobs.sqlite3`
- `output/packages/...`
- `output/bundles/job_application_packages.zip`

## Notes

- PDF generation is dependency-free and uses a lightweight internal writer.
- Tech stack extraction is keyword-based and easy to extend in `parse_jobs.py`.
- Candidate data is currently embedded in `generate_documents.py`; move it to a JSON/YAML config if you want easier editing later.
