#!/usr/bin/env python3
"""Fetch remote jobs, extract tech stacks, deduplicate, and store them in SQLite.

Sources:
- RemoteOK public JSON feed
- Hacker News "Who is hiring" comments via Algolia API
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from db import DB_PATH, get_connection, initialize_database, upsert_job

USER_AGENT = "Mozilla/5.0 (compatible; JobAutomationBot/1.0)"
REMOTEOK_URL = "https://remoteok.com/api"
HN_SEARCH_URL = (
    "https://hn.algolia.com/api/v1/search_by_date"
    "?tags=comment,author_whoishiring&query={query}&hitsPerPage={limit}"
)

TECH_KEYWORDS = {
    "Python", "Django", "Flask", "FastAPI", "JavaScript", "TypeScript", "Node.js",
    "React", "React Native", "Next.js", "Vue", "Angular", "Svelte", "HTML", "CSS",
    "Tailwind", "GraphQL", "REST", "AWS", "GCP", "Azure", "Docker", "Kubernetes",
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Firebase", "Supabase",
    "Go", "Golang", "Rust", "Java", "Spring", "C#", ".NET", "PHP", "Laravel",
    "Ruby", "Rails", "Elixir", "Phoenix", "Terraform", "Linux", "Git", "CI/CD",
    "Jenkins", "CircleCI", "GitHub Actions", "Sentry", "Expo", "Redux", "LLM", "OpenAI"
}

NORMALIZED_MAP = {
    "node": "Node.js",
    "nodejs": "Node.js",
    "reactnative": "React Native",
    "react.js": "React",
    "nextjs": "Next.js",
    "golang": "Go",
    "postgres": "PostgreSQL",
    "k8s": "Kubernetes",
    "dotnet": ".NET",
}


class FetchError(RuntimeError):
    pass



def fetch_json(url: str) -> object:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise FetchError(f"Failed to fetch {url}: {exc}") from exc



def strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()



def normalize_keyword(token: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9.+#-]", "", token.lower())
    if cleaned in NORMALIZED_MAP:
        return NORMALIZED_MAP[cleaned]

    for keyword in TECH_KEYWORDS:
        if cleaned == re.sub(r"[^a-zA-Z0-9.+#-]", "", keyword.lower()):
            return keyword
    return ""



def extract_tech_stack(*texts: str) -> List[str]:
    joined = " ".join(texts)
    lower_text = joined.lower()
    found = set()

    for keyword in TECH_KEYWORDS:
        pattern = re.escape(keyword.lower())
        if re.search(rf"(?<![a-z0-9]){pattern}(?![a-z0-9])", lower_text):
            found.add(keyword)

    for raw_token in re.findall(r"[A-Za-z0-9.+#-]{2,}", joined):
        normalized = normalize_keyword(raw_token)
        if normalized:
            found.add(normalized)

    return sorted(found)



def make_job_id(source: str, company: str, role: str, url: str) -> str:
    base = f"{source}|{company}|{role}|{url}".encode("utf-8")
    return hashlib.sha1(base).hexdigest()[:16]



def parse_remoteok(limit: int) -> List[Dict[str, object]]:
    payload = fetch_json(REMOTEOK_URL)
    if not isinstance(payload, list):
        raise FetchError("Unexpected RemoteOK payload")

    pull_date = datetime.now(timezone.utc).date().isoformat()
    jobs: List[Dict[str, object]] = []

    for item in payload:
        if not isinstance(item, dict) or not item.get("position"):
            continue
        description = strip_html(item.get("description") or "")
        tags = item.get("tags") or []
        tech_stack = extract_tech_stack(item.get("position", ""), description, " ".join(tags))
        url = item.get("url") or item.get("apply_url") or ""
        company = item.get("company") or "Unknown"
        role = item.get("position") or "Unknown"
        jobs.append(
            {
                "job_id": make_job_id("remoteok", company, role, url),
                "source": "remoteok",
                "company": company,
                "role": role,
                "url": url,
                "tech_stack": tech_stack,
                "salary": item.get("salary") or item.get("salary_min") or "",
                "location": item.get("location") or "Remote",
                "description": description[:5000],
                "pull_date": pull_date,
                "status": "new",
            }
        )
        if len(jobs) >= limit:
            break
    return jobs



def parse_hn(limit: int) -> List[Dict[str, object]]:
    query = quote_plus('"remote" AND (engineer OR developer)')
    payload = fetch_json(HN_SEARCH_URL.format(query=query, limit=max(limit * 2, 100)))
    if not isinstance(payload, dict):
        raise FetchError("Unexpected HN payload")

    pull_date = datetime.now(timezone.utc).date().isoformat()
    jobs: List[Dict[str, object]] = []

    for hit in payload.get("hits", []):
        text = strip_html(hit.get("comment_text") or "")
        if not text or "remote" not in text.lower():
            continue

        first_line = text.split(".")[0][:180]
        company, role = extract_company_role(first_line)
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        tech_stack = extract_tech_stack(first_line, text)
        jobs.append(
            {
                "job_id": make_job_id("hn", company, role, url),
                "source": "hackernews",
                "company": company,
                "role": role,
                "url": url,
                "tech_stack": tech_stack,
                "salary": extract_salary(text),
                "location": "Remote",
                "description": text[:5000],
                "pull_date": pull_date,
                "status": "new",
            }
        )
        if len(jobs) >= limit:
            break
    return jobs



def extract_company_role(first_line: str) -> tuple[str, str]:
    cleaned = first_line.replace("|", "-").replace(":", " - ")
    parts = [part.strip(" -") for part in cleaned.split("-") if part.strip(" -")]

    if len(parts) >= 2:
        company = parts[0][:120]
        role = parts[1][:160]
    else:
        words = first_line.split()
        company = " ".join(words[:3])[:120] or "Unknown Company"
        role = "Software Engineer"

    role_keywords = ["engineer", "developer", "frontend", "backend", "full stack", "product"]
    if not any(keyword in role.lower() for keyword in role_keywords):
        role = "Software Engineer"
    return company, role



def extract_salary(text: str) -> str:
    match = re.search(r"(\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*/\s*(?:yr|year|hour))?)", text, flags=re.I)
    return match.group(1) if match else ""



def deduplicate_jobs(jobs: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
    seen = set()
    unique_jobs = []
    for job in jobs:
        dedupe_key = (
            str(job.get("company", "")).strip().lower(),
            str(job.get("role", "")).strip().lower(),
            str(job.get("url", "")).strip().lower(),
        )
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        unique_jobs.append(job)
    return unique_jobs



def main(limit: int = 50) -> int:
    initialize_database(DB_PATH)
    remoteok_target = max(25, limit // 2)
    hn_target = max(25, limit - remoteok_target)

    remote_jobs = parse_remoteok(remoteok_target)
    hn_jobs = parse_hn(hn_target)
    jobs = deduplicate_jobs((remote_jobs + hn_jobs))[:limit]

    with get_connection(DB_PATH) as conn:
        for job in jobs:
            upsert_job(conn, job)

    print(f"Stored {len(jobs)} jobs in {DB_PATH}")
    return 0


if __name__ == "__main__":
    requested_limit = 50
    if len(sys.argv) > 1:
        requested_limit = int(sys.argv[1])
    raise SystemExit(main(requested_limit))
