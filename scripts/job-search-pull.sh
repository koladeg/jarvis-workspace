#!/usr/bin/env bash

# Job Search Automation - RemoteOK + Hacker News
# Pulls React/React Native jobs applicable from Nigeria
# Runs headlessly under cron
# Posts to Jarvis-Job-Search Telegram group
# Sends HTML email to jarviskolademail@gmail.com
# Tracking: memory/job-search.md

set -Eeuo pipefail

WORKSPACE="/home/claw/.openclaw/workspace"
export WORKSPACE
export TZ=UTC
TIMESTAMP="$(date -u '+%Y-%m-%d %H:%M UTC')"
PULL_LOG="$WORKSPACE/memory/job-search.md"
SCRIPT_NAME="$(basename "$0")"

mkdir -p "$WORKSPACE/memory"

echo "🚀 Job Search Pull - $TIMESTAMP"

python3 - <<'PY'
import html
import imaplib
import json
import os
import re
import smtplib
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import List, Optional

WORKSPACE = Path(os.environ.get("WORKSPACE", "/home/claw/.openclaw/workspace"))
PULL_LOG = WORKSPACE / "memory" / "job-search.md"
CREDENTIALS_DIR = WORKSPACE / ".credentials"
TELEGRAM_CONFIG = CREDENTIALS_DIR / "telegram_bot_config.txt"
GMAIL_PASSWORD_FILE = CREDENTIALS_DIR / "gmail_app_password.txt"
RECIPIENT_EMAIL = "jarviskolademail@gmail.com"
SENDER_EMAIL = "jarviskolademail@gmail.com"
REMOTEOK_API = "https://remoteok.com/api"
HN_JOBS_URL = "https://news.ycombinator.com/jobs"
MAX_REMOTEOK = 8
MAX_HN = 8

now = datetime.now(timezone.utc)
timestamp = now.strftime("%Y-%m-%d %H:%M UTC")
day_header = now.strftime("%A, %Y-%m-%d")
pull_id = str(int(now.timestamp()))
subject = f"Job Pull {day_header}"

@dataclass
class Job:
    source: str
    title: str
    company: str
    salary: str
    link: str
    location: str = "Remote"
    posted: str = "Unknown"
    tags: Optional[List[str]] = None


def http_get(url: str, headers: Optional[dict] = None) -> str:
    req = urllib.request.Request(
        url,
        headers=headers or {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def load_kv_file(path: Path) -> dict:
    data = {}
    if not path.exists():
        return data
    for line in path.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return data


def normalize_link(link: str) -> str:
    if not link:
        return ""
    if link.startswith("//"):
        return "https:" + link
    if link.startswith("/"):
        return "https://remoteok.com" + link
    return link


def salary_from_remoteok(item: dict) -> str:
    min_salary = item.get("salary_min")
    max_salary = item.get("salary_max")
    salary_raw = item.get("salary_estimate") or item.get("salary")
    if min_salary and max_salary:
        return f"${int(min_salary):,} - ${int(max_salary):,}"
    if salary_raw:
        return str(salary_raw)
    return "Not listed"


def fetch_remoteok_jobs() -> List[Job]:
    raw = http_get(REMOTEOK_API, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    })
    payload = json.loads(raw)
    jobs: List[Job] = []
    seen = set()
    for item in payload[1:]:
        title = (item.get("position") or "").strip()
        company = (item.get("company") or "").strip()
        text = " ".join([
            title.lower(),
            company.lower(),
            " ".join((item.get("tags") or [] )).lower(),
            (item.get("description") or "").lower(),
        ])
        if not title or not company:
            continue
        if "react" not in text:
            continue
        if any(bad in text for bad in ["vue", "angular only"]):
            pass
        key = (title, company)
        if key in seen:
            continue
        seen.add(key)
        jobs.append(Job(
            source="RemoteOK",
            title=title,
            company=company,
            salary=salary_from_remoteok(item),
            link=normalize_link(item.get("url") or item.get("apply_url") or ""),
            location=item.get("location") or ("Worldwide" if item.get("worldwide") else "Remote"),
            posted=item.get("date") or "Unknown",
            tags=item.get("tags") or [],
        ))
        if len(jobs) >= MAX_REMOTEOK:
            break
    return jobs


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_hn_title(title: str):
    clean = clean_text(title)
    salary_match = re.search(r"(\$[\d,.]+k?(?:\s*-\s*\$[\d,.]+k?)?(?:\s*(?:\+\s*equity|and\s+[\d.%-]+\s*equity))?)", clean, re.I)
    salary = salary_match.group(1) if salary_match else "Not listed"

    company = clean
    role = "General role"
    patterns = [
        r"^(.*?)\s*\((YC[^)]*)\)\s*[:\-–]\s*(.*)$",
        r"^(.*?)\s*\((YC[^)]*)\)\s+is hiring\s+(.*)$",
        r"^(.*?)\s*\((YC[^)]*)\)\s+Is Hiring\s+(.*)$",
        r"^(.*?)\s*[:\-–]\s*(.*)$",
    ]
    for pattern in patterns:
        m = re.match(pattern, clean, re.I)
        if m:
            company = clean_text(m.group(1))
            tail = clean_text(m.group(len(m.groups())))
            role = tail or role
            break
    company = re.sub(r"\s*\((YC[^)]*)\)", r" (\1)", company).strip()
    if role.lower().startswith("is hiring"):
        role = re.sub(r"^is hiring\s*", "", role, flags=re.I).strip() or "General role"
    return company, role, salary


HN_ENTRY_RE = re.compile(
    r'<tr class="athing submission" id="(?P<id>\d+)">.*?<span class="titleline"><a href="(?P<link>[^"]+)"[^>]*>(?P<title>.*?)</a>.*?</tr>\s*<tr><td colspan="2"></td><td class="subtext"><span class="age" title="(?P<iso>[^"]+) [^"]*"><a href="item\?id=\d+">(?P<age>.*?)</a>',
    re.S,
)


def fetch_hn_jobs() -> List[Job]:
    html_doc = http_get(HN_JOBS_URL)
    jobs: List[Job] = []
    for match in HN_ENTRY_RE.finditer(html_doc):
        raw_title = re.sub(r"<.*?>", "", match.group("title"))
        company, role, salary = parse_hn_title(raw_title)
        jobs.append(Job(
            source="Hacker News",
            title=role,
            company=company,
            salary=salary,
            link=clean_text(match.group("link")),
            location="See listing",
            posted=clean_text(match.group("age")),
            tags=["YC startup"],
        ))
        if len(jobs) >= MAX_HN:
            break
    return jobs


def build_telegram_message(remoteok_jobs: List[Job], hn_jobs: List[Job]) -> str:
    lines = [
        f"🚀 WEEKLY JOB PULL - {day_header}",
        "",
        f"RemoteOK React/React Native: {len(remoteok_jobs)} roles",
    ]
    for idx, job in enumerate(remoteok_jobs[:4], 1):
        lines.extend([
            f"{idx}. {job.title} — {job.company}",
            f"   Salary: {job.salary}",
            f"   Link: {job.link}",
        ])
    lines.extend([
        "",
        f"Hacker News YC jobs: {len(hn_jobs)} roles",
    ])
    for idx, job in enumerate(hn_jobs[:4], 1):
        lines.extend([
            f"{idx}. {job.company}",
            f"   Role: {job.title}",
            f"   Salary: {job.salary}",
            f"   Link: {job.link}",
        ])
    lines.extend([
        "",
        "✅ Filter: remote-friendly roles worth reviewing from Nigeria",
        "📊 Full tracking updated in memory/job-search.md",
    ])
    return "\n".join(lines)


def build_email_html(remoteok_jobs: List[Job], hn_jobs: List[Job]) -> str:
    def job_li(job: Job) -> str:
        return (
            f"<li><strong>{html.escape(job.title)}</strong> — {html.escape(job.company)}"
            f"<br>Salary: {html.escape(job.salary)}"
            f"<br>Location: {html.escape(job.location)}"
            f"<br>Posted: {html.escape(job.posted)}"
            f"<br><a href=\"{html.escape(job.link, quote=True)}\">Open listing</a></li>"
        )

    remote_list = "\n".join(job_li(job) for job in remoteok_jobs) or "<li>No matching RemoteOK jobs found.</li>"
    hn_list = "\n".join(job_li(job) for job in hn_jobs) or "<li>No matching Hacker News jobs found.</li>"

    return f"""
    <html>
      <body style="font-family:Arial,sans-serif;line-height:1.5;color:#222;">
        <h2>🚀 Weekly Job Pull — {html.escape(day_header)}</h2>
        <p>Fresh React / React Native / startup roles pulled for review.</p>
        <h3>RemoteOK</h3>
        <ol>{remote_list}</ol>
        <h3>Hacker News / YC Startups</h3>
        <ol>{hn_list}</ol>
        <p><strong>Tracking:</strong> memory/job-search.md</p>
      </body>
    </html>
    """.strip()


def build_email_text(remoteok_jobs: List[Job], hn_jobs: List[Job]) -> str:
    lines = [f"Weekly Job Pull - {day_header}", "", "RemoteOK:"]
    for job in remoteok_jobs:
        lines.extend([
            f"- {job.title} — {job.company}",
            f"  Salary: {job.salary}",
            f"  Link: {job.link}",
        ])
    lines.extend(["", "Hacker News / YC:"])
    for job in hn_jobs:
        lines.extend([
            f"- {job.company}: {job.title}",
            f"  Salary: {job.salary}",
            f"  Link: {job.link}",
        ])
    return "\n".join(lines)


def send_telegram(message_text: str) -> str:
    cfg = load_kv_file(TELEGRAM_CONFIG)
    token = cfg.get("TELEGRAM_BOT_TOKEN")
    chat_id = cfg.get("TELEGRAM_CHAT_ID_JOB_SEARCH")
    if not token or not chat_id:
        return "SKIPPED - missing Telegram bot token/chat ID"
    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message_text,
        "disable_web_page_preview": "true",
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        if data.get("ok"):
            msg_id = data.get("result", {}).get("message_id")
            return f"OK - message_id={msg_id}"
        return f"FAILED - Telegram API response: {data}"
    except Exception as exc:
        return f"FAILED - {exc}"


def send_email(subject: str, html_body: str, text_body: str) -> str:
    if not GMAIL_PASSWORD_FILE.exists():
        return "SKIPPED - missing Gmail app password"
    password = GMAIL_PASSWORD_FILE.read_text().strip()
    if not password:
        return "SKIPPED - empty Gmail app password"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=30) as smtp:
            smtp.login(SENDER_EMAIL, password)
            smtp.send_message(msg)
        return "OK - SMTP accepted message"
    except Exception as exc:
        return f"FAILED - {exc}"


def verify_email_delivery(subject: str) -> str:
    if not GMAIL_PASSWORD_FILE.exists():
        return "SKIPPED - missing Gmail app password"
    password = GMAIL_PASSWORD_FILE.read_text().strip()
    if not password:
        return "SKIPPED - empty Gmail app password"
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com", 993) as imap:
            imap.login(SENDER_EMAIL, password)
            imap.select("INBOX")
            status, data = imap.search(None, 'FROM', f'"{SENDER_EMAIL}"', 'TO', f'"{RECIPIENT_EMAIL}"', 'SUBJECT', f'"{subject}"')
            if status == "OK" and data and data[0]:
                ids = data[0].split()
                return f"OK - inbox match count={len(ids)}"
            imap.select('"[Gmail]/Sent Mail"')
            status, data = imap.search(None, 'TO', f'"{RECIPIENT_EMAIL}"', 'SUBJECT', f'"{subject}"')
            if status == "OK" and data and data[0]:
                ids = data[0].split()
                return f"PARTIAL - found in Sent Mail count={len(ids)}"
            return "FAILED - message not found in Inbox/Sent search"
    except Exception as exc:
        return f"FAILED - {exc}"


def markdown_job_block(job: Job) -> str:
    tags = ", ".join(job.tags or []) if job.tags else ""
    lines = [
        f"**{job.title}** — {job.company}",
        f"- Salary: {job.salary}",
        f"- Location: {job.location}",
        f"- Posted: {job.posted}",
        f"- Link: {job.link}",
    ]
    if tags:
        lines.append(f"- Tags: {tags}")
    return "\n".join(lines)


def append_tracking(remoteok_jobs: List[Job], hn_jobs: List[Job], telegram_status: str, email_status: str, email_verify_status: str):
    entry = [
        "",
        f"## Pull #{pull_id} - {timestamp} - AUTOMATED CRON",
        "",
        "**Sources:**",
        f"- RemoteOK React/React Native: ✅ Pulled ({len(remoteok_jobs)} listings)",
        f"- Hacker News Jobs: ✅ Pulled ({len(hn_jobs)} listings)",
        "",
        "**Delivery Status:**",
        f"- Telegram: {telegram_status}",
        f"- Email send: {email_status}",
        f"- Email verify: {email_verify_status}",
        "",
        "### RemoteOK Listings",
    ]
    if remoteok_jobs:
        for idx, job in enumerate(remoteok_jobs, 1):
            entry.extend(["", f"#### RemoteOK #{idx}", markdown_job_block(job)])
    else:
        entry.append("- No matching RemoteOK listings found.")

    entry.extend(["", "### Hacker News Listings"])
    if hn_jobs:
        for idx, job in enumerate(hn_jobs, 1):
            entry.extend(["", f"#### Hacker News #{idx}", markdown_job_block(job)])
    else:
        entry.append("- No matching Hacker News listings found.")

    entry.extend(["", "**Status:** Automated pull completed with tracked delivery results.", ""])
    with PULL_LOG.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(entry))


try:
    remoteok_jobs = fetch_remoteok_jobs()
    hn_jobs = fetch_hn_jobs()
    telegram_message = build_telegram_message(remoteok_jobs, hn_jobs)
    email_html = build_email_html(remoteok_jobs, hn_jobs)
    email_text = build_email_text(remoteok_jobs, hn_jobs)

    telegram_status = send_telegram(telegram_message)
    email_status = send_email(subject, email_html, email_text)
    email_verify_status = verify_email_delivery(subject) if email_status.startswith("OK") else "SKIPPED - email send failed"

    append_tracking(remoteok_jobs, hn_jobs, telegram_status, email_status, email_verify_status)

    print(json.dumps({
        "timestamp": timestamp,
        "pull_id": pull_id,
        "remoteok_count": len(remoteok_jobs),
        "hn_count": len(hn_jobs),
        "telegram_status": telegram_status,
        "email_status": email_status,
        "email_verify_status": email_verify_status,
        "subject": subject,
    }, indent=2))
except Exception as exc:
    error_entry = f"\n## Pull #{pull_id} - {timestamp} - AUTOMATED CRON\n\n**Status:** FAILED - {exc}\n"
    with PULL_LOG.open("a", encoding="utf-8") as fh:
        fh.write(error_entry)
    print(f"ERROR: {exc}", file=sys.stderr)
    raise
PY

echo "✅ Job search pull complete at $TIMESTAMP"
echo "📊 Tracking: $PULL_LOG"