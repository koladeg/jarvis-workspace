#!/usr/bin/env python3
"""Fetch jobs, extract tech stacks, deduplicate, and store them in SQLite.

Sources:
- RemoteOK public JSON feed
- Hacker News "Who is hiring" comments via Algolia API
- Jobberman software/data listings
- MyJobMag information technology listings
- Hot Nigerian Jobs computer/AI listings
- Selected config-driven company career pages when they expose usable HTML listings
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urljoin
from urllib.request import Request, urlopen

from db import DB_PATH, get_connection, initialize_database, upsert_job

USER_AGENT = "Mozilla/5.0 (compatible; JobAutomationBot/1.0)"
REMOTEOK_URL = "https://remoteok.com/api"
HN_SEARCH_URL = (
    "https://hn.algolia.com/api/v1/search_by_date"
    "?tags=comment,author_whoishiring&query={query}&hitsPerPage={limit}"
)
JOBBERMAN_URL = "https://www.jobberman.com/jobs/software-data"
MYJOBMAG_URL = "https://www.myjobmag.com/jobs-by-field/information-technology"
HOT_NIGERIAN_JOBS_URL = "https://www.hotnigerianjobs.com/industry/119/"
MONIEPOINT_GREENHOUSE_URL = "https://boards-api.greenhouse.io/v1/boards/moniepoint/jobs?content=true"
FLUTTERWAVE_VACANCIES_URL = "https://flutterwave.com/us/careers/vacancies"
MIN_NAIRA_SALARY = 500_000
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
JOB_SITES_CONFIG_PATH = WORKSPACE_ROOT / "config" / "job-sites.json"

TECH_KEYWORDS = {
    "Python", "Django", "Flask", "FastAPI", "JavaScript", "TypeScript", "Node.js",
    "React", "React Native", "Next.js", "Vue", "Angular", "Svelte", "HTML", "CSS",
    "Tailwind", "GraphQL", "REST", "AWS", "GCP", "Azure", "Docker", "Kubernetes",
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Firebase", "Supabase",
    "Go", "Golang", "Rust", "Java", "Spring", "C#", ".NET", "PHP", "Laravel",
    "Ruby", "Rails", "Elixir", "Phoenix", "Terraform", "Linux", "Git", "CI/CD",
    "Jenkins", "CircleCI", "GitHub Actions", "Sentry", "Expo", "Redux", "LLM", "OpenAI",
    "Playwright", "Postman", "Flutter", "QA", "UI", "UX"
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

ROLE_INCLUDE_KEYWORDS = (
    "react",
    "frontend",
    "front end",
    "front-end",
    "react native",
    "mobile",
    "flutter",
    "software developer",
    "software engineer",
    "javascript",
    "typescript",
    "node",
    "full stack",
    "full-stack",
    "backend",
    "ui",
    "ux",
    "qa",
    "quality assurance",
    "devops",
    "web developer",
    "app developer",
    "application developer",
    "automation tester",
    "product engineer",
)

ROLE_EXCLUDE_KEYWORDS = (
    "sales",
    "marketing",
    "teacher",
    "instructor",
    "recruiter",
    "driver",
    "chef",
    "cook",
    "mixologist",
    "accounting",
    "accountant",
    "nurse",
)

GERMANY_ROLE_INCLUDE_PATTERNS = (
    r"\bsoftware engineer\b",
    r"\bsoftware developer\b",
    r"\bdeveloper\b",
    r"\bengineer\b",
    r"\bfrontend\b",
    r"\bbackend\b",
    r"\bfront\s*end\b",
    r"\bfull[ -]?stack\b",
    r"\bmobile\b",
    r"\breact\b",
    r"\breact native\b",
    r"\bjavascript\b",
    r"\btypescript\b",
    r"\bnode\.?js\b",
    r"\bdevops\b",
    r"\bplatform engineer\b",
    r"\bcloud engineer\b",
    r"\bsite reliability\b",
    r"\bsre\b",
    r"\bdata engineer\b",
    r"\bdata scientist\b",
    r"\bml engineer\b",
    r"\bai engineer\b",
    r"\bqa\b",
    r"\btest engineer\b",
    r"\bios\b",
    r"\bandroid\b",
    r"\bsecurity engineer\b",
    r"\bproduct engineer\b",
    r"\bentwickler\b",
    r"\bsoftwareentwickler\b",
)

FIT_PRIORITY_PATTERNS = (
    (r"\breact native\b", 24),
    (r"\bmobile\b", 18),
    (r"\bandroid\b", 15),
    (r"\bios\b", 15),
    (r"\bfrontend\b|\bfront\s*end\b", 14),
    (r"\breact\b", 12),
    (r"\btypescript\b", 10),
    (r"\bjavascript\b", 8),
    (r"\bproduct engineer\b", 10),
    (r"\bfull[ -]?stack\b", 6),
    (r"\bnode\.?js\b", 5),
    (r"\bui\b|\bux\b", 4),
    (r"\bberlin\b", 4),
    (r"\bremote\b", 4),
    (r"\bhybrid\b", 2),
    (r"\benglish\b", 4),
    (r"no german required", 5),
    (r"visa sponsorship|relocation|blue card", 5),
    (r"\bstartup\b|vc-funded|product mindset|saas", 5),
)

FIT_PENALTY_PATTERNS = (
    (r"\blead\b|\bmanager\b|\bhead of\b", -8),
    (r"\bhead of technology\b|\bcto\b", -14),
    (r"\bstaff\b|\bprincipal\b|\barchitect\b", -6),
    (r"\bdeveloper advocate\b|\badvocate\b", -10),
    (r"\bforward deployed\b", -8),
    (r"\bit systems?\b|\bsystems engineer\b|\bsystemadministrator\b|\bsysadmin\b", -10),
    (r"\bautomation engineer\b|\bit automation\b", -8),
    (r"\blegal\b|\bcounsel\b|\bgovernance\b", -20),
    (r"\baccount executive\b|\bsales\b|\bmarketing\b|\brecruiter\b", -20),
    (r"\bdevops\b|\bplatform engineer\b|\bsite reliability\b|\bsre\b", -4),
    (r"\bsecurity engineer\b|\bcloud engineer\b", -4),
    (r"\bdata scientist\b|\bmachine learning\b|\bml engineer\b|\bai engineer\b|\bllm\b", -10),
    (r"\bdata engineer\b|\bdata platform\b", -8),
)

SOURCE_FIT_BONUSES = {
    "arbeitnow-english-germany": 4,
    "berlinstartupjobs-engineering": 7,
    "wearedevelopers-germany": 2,
    "pegel-visa-berlin": 3,
}


class FetchError(RuntimeError):
    pass


def load_job_sites_config() -> dict:
    try:
        return json.loads(JOB_SITES_CONFIG_PATH.read_text())
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        raise FetchError(f"Invalid job sites config at {JOB_SITES_CONFIG_PATH}: {exc}") from exc


def fetch_json(url: str) -> object:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise FetchError(f"Failed to fetch {url}: {exc}") from exc


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=30) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise FetchError(f"Failed to fetch {url}: {exc}") from exc


def strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value or "")).strip()


def absolutize_url(url: str, base: str) -> str:
    if not url:
        return base
    if url.startswith("http://") or url.startswith("https://"):
        return url
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return base.rstrip("/") + url
    return base.rstrip("/") + "/" + url


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


def is_target_role(*texts: str) -> bool:
    haystack = " ".join(texts).lower()
    if not any(keyword in haystack for keyword in ROLE_INCLUDE_KEYWORDS):
        return False
    if any(keyword in haystack for keyword in ROLE_EXCLUDE_KEYWORDS):
        return False
    return True


def is_target_germany_role(*texts: str) -> bool:
    haystack = " ".join(texts).lower()
    if any(keyword in haystack for keyword in ROLE_EXCLUDE_KEYWORDS):
        return False
    return any(re.search(pattern, haystack) for pattern in GERMANY_ROLE_INCLUDE_PATTERNS)


def job_fit_score(job: Dict[str, object]) -> int:
    tech_stack = job.get("tech_stack") or []
    if isinstance(tech_stack, str):
        try:
            tech_stack = json.loads(tech_stack)
        except json.JSONDecodeError:
            tech_stack = [tech_stack]

    haystack = " ".join(
        [
            str(job.get("role", "")),
            str(job.get("company", "")),
            str(job.get("location", "")),
            str(job.get("description", "")),
            " ".join(str(item) for item in tech_stack),
        ]
    ).lower()

    score = 0
    score += SOURCE_FIT_BONUSES.get(str(job.get("source", "")), 0)

    for pattern, value in FIT_PRIORITY_PATTERNS:
        if re.search(pattern, haystack):
            score += value

    for pattern, value in FIT_PENALTY_PATTERNS:
        if re.search(pattern, haystack):
            score += value

    if re.search(r"\bsenior\b", haystack):
        score += 1

    if re.search(r"\b(kotlin|java)\b", haystack) and re.search(r"\bbackend\b", haystack) and not re.search(
        r"\bfrontend\b|\bfront\s*end\b|\bmobile\b|\bandroid\b|\bios\b|\bfull[ -]?stack\b",
        haystack,
    ):
        score -= 5

    if re.search(r"\bmobile\b|\breact native\b|\bandroid\b|\bios\b", haystack) and re.search(
        r"relocation|visa sponsorship|no german required|english",
        haystack,
    ):
        score += 4

    if re.search(r"\bstartup\b|vc-funded|product mindset", haystack):
        score += 3

    if re.search(r"\bsoftware engineer\b", haystack) and not re.search(
        r"\breact\b|\bfrontend\b|\bfront\s*end\b|\bmobile\b|\breact native\b|\btypescript\b|\bjavascript\b|\bfull[ -]?stack\b|\bproduct engineer\b",
        haystack,
    ):
        score -= 4

    if re.search(r"\bbackend\b", haystack) and not re.search(r"\bfrontend\b|\bfront\s*end\b|\bfull[ -]?stack\b|\bmobile\b", haystack):
        score -= 3

    return score


def sort_jobs_by_fit(jobs: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
    return sorted(
        jobs,
        key=lambda job: (
            job_fit_score(job),
            len(job.get("tech_stack") or []),
            len(str(job.get("description") or "")),
        ),
        reverse=True,
    )


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


def parse_jobberman(limit: int) -> List[Dict[str, object]]:
    html = fetch_text(JOBBERMAN_URL)
    pull_date = datetime.now(timezone.utc).date().isoformat()
    prerender_links = [
        link for link in re.findall(r'<link rel="prerender" href="([^"]+)"', html)
        if "/listings/" in link
    ]
    item_pattern = re.compile(
        r'\{"item_name":"(?P<title>[^"]+)","item_id":(?P<item_id>\d+),.*?'
        r'"affiliation":"(?P<company>[^"]+)",.*?'
        r'"item_category3":"(?P<job_type>[^"]+)",.*?'
        r'"item_category4":"(?P<seniority>[^"]+)",.*?'
        r'"item_variant":"(?P<salary_state>[^"]+)","location_id":"(?P<location>[^"]+)"',
        re.S,
    )

    jobs: List[Dict[str, object]] = []
    for idx, match in enumerate(item_pattern.finditer(html)):
        title = normalize_whitespace(match.group("title"))
        company = normalize_whitespace(match.group("company"))
        location = normalize_whitespace(match.group("location")) or "Nigeria"
        seniority = normalize_whitespace(match.group("seniority"))
        job_type = normalize_whitespace(match.group("job_type"))
        if not is_target_role(title, company, seniority):
            continue

        url = absolutize_url(prerender_links[idx], "https://www.jobberman.com") if idx < len(prerender_links) else JOBBERMAN_URL
        description = f"{seniority} {job_type} role from Jobberman in {location}."
        salary = extract_jobberman_detail_salary(url)
        if not naira_salary_meets_floor(salary):
            continue
        jobs.append(
            {
                "job_id": make_job_id("jobberman", company, title, url),
                "source": "jobberman",
                "company": company,
                "role": title,
                "url": url,
                "tech_stack": extract_tech_stack(title, description),
                "salary": salary,
                "location": location,
                "description": description,
                "pull_date": pull_date,
                "status": "new",
            }
        )
        if len(jobs) >= limit:
            break
    return jobs


def parse_myjobmag(limit: int) -> List[Dict[str, object]]:
    html = fetch_text(MYJOBMAG_URL)
    pull_date = datetime.now(timezone.utc).date().isoformat()
    pattern = re.compile(
        r'<h2><a href="(?P<link>[^"]+)">(?P<title>.*?)</a></h2>.*?'
        r'<li class="job-desc">\s*(?P<desc>.*?)\s*</li>.*?'
        r'(?:<li class="job_detail_tag"><span class="job-salary">(?P<salary>.*?)</span></li>)?.*?'
        r'<li id="job-date">(?P<date>[^<]+)(?P<date_rest>.*?)</li>',
        re.S,
    )

    jobs: List[Dict[str, object]] = []
    for match in pattern.finditer(html):
        title_line = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("title")))
        desc = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("desc")))
        salary = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("salary") or ""))
        location = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("date_rest") or "")) or "Nigeria"

        role = title_line
        company = "MyJobMag listing"
        if " at " in title_line:
            role, company = [part.strip() for part in title_line.split(" at ", 1)]

        if not is_target_role(role, desc):
            continue

        url = absolutize_url(match.group("link"), "https://www.myjobmag.com")
        detail_salary = extract_myjobmag_detail_salary(url)
        salary = detail_salary or salary
        if not naira_salary_meets_floor(salary):
            continue
        jobs.append(
            {
                "job_id": make_job_id("myjobmag", company, role, url),
                "source": "myjobmag",
                "company": company,
                "role": role,
                "url": url,
                "tech_stack": extract_tech_stack(role, desc),
                "salary": salary,
                "location": location,
                "description": desc[:5000],
                "pull_date": pull_date,
                "status": "new",
            }
        )
        if len(jobs) >= limit:
            break
    return jobs


def parse_hotnigerianjobs(limit: int) -> List[Dict[str, object]]:
    html = fetch_text(HOT_NIGERIAN_JOBS_URL)
    pull_date = datetime.now(timezone.utc).date().isoformat()
    block_pattern = re.compile(
        r"<div class='mycase'>.*?<h1><a href='(?P<link>[^']+)'[^>]*title='Permanent Link: (?P<title_attr>[^']+)'>(?P<title>.*?)</a></h1>.*?"
        r"<span class='semibio'>Posted on (?P<posted>.*?) - </span>.*?<div class='mycase4'>\s*(?P<desc>.*?)\s*<div style='text-align: right;'>",
        re.S,
    )

    jobs: List[Dict[str, object]] = []
    for match in block_pattern.finditer(html):
        title_line = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("title") or match.group("title_attr")))
        desc = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("desc")))
        posted = normalize_whitespace(match.group("posted"))

        role = title_line
        company = "Hot Nigerian Jobs listing"
        if " at " in title_line:
            role, company = [part.strip() for part in title_line.split(" at ", 1)]
        elif " - " in title_line:
            role, company = [part.strip() for part in title_line.split(" - ", 1)]

        if not is_target_role(role):
            continue

        location_match = re.search(r"located in ([^.]+)", desc, re.I)
        location = normalize_whitespace(location_match.group(1)) if location_match else "Nigeria"
        url = absolutize_url(match.group("link"), "https://www.hotnigerianjobs.com")
        salary = extract_hotnigerianjobs_detail_salary(url)
        if not naira_salary_meets_floor(salary):
            continue
        jobs.append(
            {
                "job_id": make_job_id("hotnigerianjobs", company, role, url),
                "source": "hotnigerianjobs",
                "company": company,
                "role": role,
                "url": url,
                "tech_stack": extract_tech_stack(role, desc),
                "salary": salary,
                "location": location,
                "description": f"{posted}. {desc}"[:5000],
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
    match = re.search(r"(₦[\d,]+(?:\s*-\s*₦[\d,]+)?(?:/month)?|N[\d,]+(?:\s*-\s*N[\d,]+)?(?:\s*monthly)?|NGN\s*[\d,]+(?:\s*-\s*NGN\s*[\d,]+)?|\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*/\s*(?:yr|year|hour))?)", text, flags=re.I)
    return match.group(1) if match else ""


def format_naira_range(min_value: int | None, max_value: int | None) -> str:
    if min_value is not None and max_value is not None:
        return f"₦{min_value:,} - ₦{max_value:,}"
    if min_value is not None:
        return f"₦{min_value:,}"
    if max_value is not None:
        return f"₦{max_value:,}"
    return ""


def extract_jobberman_detail_salary(url: str) -> str:
    html = fetch_text(url)
    match = re.search(
        r'"baseSalary"\s*:\s*\{.*?"currency"\s*:\s*"NGN".*?"value"\s*:\s*\{.*?(?:"value"\s*:\s*(\d+))?.*?(?:"minValue"\s*:\s*(\d+))?.*?(?:"maxValue"\s*:\s*(\d+))?.*?\}',
        html,
        re.S,
    )
    if not match:
        return ""
    value = int(match.group(1)) if match.group(1) else None
    min_value = int(match.group(2)) if match.group(2) else value
    max_value = int(match.group(3)) if match.group(3) else value
    return format_naira_range(min_value, max_value)


def extract_myjobmag_detail_salary(url: str) -> str:
    html = fetch_text(url)
    match = re.search(r'Salary Range</span>\s*<span class="jkey-info">(.*?)</span>', html, re.S | re.I)
    if not match:
        return ""
    return normalize_whitespace(re.sub(r"<.*?>", " ", match.group(1)))


def extract_hotnigerianjobs_detail_salary(url: str) -> str:
    html = fetch_text(url)
    match = re.search(
        r'"baseSalary"\s*:\s*\{.*?"currency"\s*:\s*"NGN".*?"minValue"\s*:\s*(\d+).*?"maxValue"\s*:\s*(\d+)',
        html,
        re.S,
    )
    if match:
        return format_naira_range(int(match.group(1)), int(match.group(2)))
    match = re.search(r'Salary\s*(?:N|₦)\s*([\d,]+)\s*-\s*(?:N|₦)\s*([\d,]+)', html, re.I)
    if match:
        return format_naira_range(int(match.group(1).replace(",", "")), int(match.group(2).replace(",", "")))
    return extract_salary(html)


def naira_salary_meets_floor(salary_text: str) -> bool:
    salary_text = (salary_text or "").strip()
    if not salary_text:
        return False
    if "₦" not in salary_text and "NGN" not in salary_text.upper():
        return False
    values = [int(value.replace(",", "")) for value in re.findall(r"(?:₦|NGN\s*)([\d,]+)", salary_text, flags=re.I)]
    if not values:
        return False
    return max(values) >= MIN_NAIRA_SALARY


def build_job_record(
    *,
    source: str,
    company: str,
    role: str,
    url: str,
    description: str,
    salary: str = "",
    location: str = "Nigeria",
    tech_seed: str = "",
) -> Dict[str, object]:
    pull_date = datetime.now(timezone.utc).date().isoformat()
    return {
        "job_id": make_job_id(source, company, role, url),
        "source": source,
        "company": company,
        "role": role,
        "url": url,
        "tech_stack": extract_tech_stack(role, description, tech_seed),
        "salary": salary,
        "location": location,
        "description": description[:5000],
        "pull_date": pull_date,
        "status": "new",
    }


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def render_dynamic_jobs(site_id: str, url: str) -> list[dict]:
    script_path = Path(__file__).resolve().parent / "render_company_jobs.js"
    try:
        result = subprocess.run(
            ["node", str(script_path), site_id, url],
            check=True,
            capture_output=True,
            text=True,
            timeout=90,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise FetchError(f"Failed to render jobs for {site_id}: {exc}") from exc

    try:
        payload = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise FetchError(f"Invalid rendered jobs payload for {site_id}: {exc}") from exc

    if not isinstance(payload, list):
        raise FetchError(f"Unexpected rendered jobs payload for {site_id}")
    return payload


def parse_piggyvest_company(limit: int, site: dict) -> List[Dict[str, object]]:
    html = fetch_text(site["url"])
    pattern = re.compile(
        r'<div class="position-card">\s*<div class="position-card__info">\s*'
        r'<h4>(?P<role>.*?)</h4>\s*<div class="position-card__meta">'
        r'\s*<span>(?P<department>.*?)</span>\s*•\s*<span>(?P<location>.*?)</span>'
        r'\s*•\s*<span>(?P<job_type>.*?)</span>.*?'
        r'<a href="(?P<link>https://piggytech\.seamlesshiring\.com/job/view/\d+)"',
        re.S,
    )

    jobs: List[Dict[str, object]] = []
    for match in pattern.finditer(html):
        role = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("role")))
        department = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("department")))
        location = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("location"))) or "Nigeria"
        job_type = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("job_type")))
        if not is_target_role(role, department, job_type):
            continue

        description = f"{department} role at PiggyVest in {location}. {job_type}."
        jobs.append(
            build_job_record(
                source=site["id"],
                company=site["name"].replace(" Careers", ""),
                role=role,
                url=match.group("link"),
                description=description,
                location=location,
                tech_seed=department,
            )
        )
        if len(jobs) >= limit:
            break
    return jobs


def parse_moniepoint_company(limit: int, site: dict) -> List[Dict[str, object]]:
    payload = fetch_json(MONIEPOINT_GREENHOUSE_URL)
    if not isinstance(payload, dict):
        raise FetchError("Unexpected Moniepoint Greenhouse payload")

    jobs: List[Dict[str, object]] = []
    for item in payload.get("jobs", []):
        if not isinstance(item, dict):
            continue

        role = normalize_whitespace(item.get("title") or "")
        location = normalize_whitespace((item.get("location") or {}).get("name") or "Nigeria")
        departments = ", ".join(
            normalize_whitespace(dept.get("name") or "")
            for dept in item.get("departments") or []
            if isinstance(dept, dict) and dept.get("name")
        )
        offices = ", ".join(
            normalize_whitespace(office.get("name") or "")
            for office in item.get("offices") or []
            if isinstance(office, dict) and office.get("name")
        )
        description = strip_html(item.get("content") or "")
        if not is_target_role(role, departments, offices, description):
            continue

        jobs.append(
            build_job_record(
                source=site["id"],
                company=site["name"].replace(" Careers", ""),
                role=role,
                url=item.get("absolute_url") or site["url"],
                description=description,
                location=location,
                tech_seed=" ".join(part for part in [departments, offices] if part),
            )
        )
        if len(jobs) >= limit:
            break
    return jobs


def parse_flutterwave_company(limit: int, site: dict) -> List[Dict[str, object]]:
    html = fetch_text(FLUTTERWAVE_VACANCIES_URL)
    pattern = re.compile(
        r'<p class="p sm section-roles__role">\s*'
        r'<a href="(?P<link>https://flutterwavego\.bamboohr\.com/careers/\d+)"[^>]*>(?P<role>.*?)</a>\s*'
        r'<span>(?P<department>.*?)</span>\s*'
        r'<span>(?P<location>.*?)</span>',
        re.S,
    )

    jobs: List[Dict[str, object]] = []
    for match in pattern.finditer(html):
        role = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("role")))
        department = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("department")))
        location = normalize_whitespace(re.sub(r"<.*?>", " ", match.group("location"))) or "Nigeria"
        if not is_target_role(role, department, location):
            continue

        description = f"{department} role at Flutterwave in {location}."
        jobs.append(
            build_job_record(
                source=site["id"],
                company=site["name"].replace(" Careers", ""),
                role=role,
                url=match.group("link"),
                description=description,
                location=location,
                tech_seed=department,
            )
        )
        if len(jobs) >= limit:
            break
    return jobs


def parse_kuda_company(limit: int, site: dict) -> List[Dict[str, object]]:
    payload = render_dynamic_jobs(site["id"], site["url"] + "/view-jobs/?location=Nigeria")
    jobs: List[Dict[str, object]] = []
    seen = set()
    for item in payload:
        if not isinstance(item, dict):
            continue
        role = normalize_whitespace(item.get("role") or "")
        location = normalize_whitespace(item.get("location") or "Nigeria")
        job_type = normalize_whitespace(item.get("jobType") or "")
        if not is_target_role(role, location, job_type):
            continue
        dedupe_key = (role.lower(), location.lower(), job_type.lower())
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        synthetic_url = f"{site['url']}/view-jobs/?location=Nigeria#{slugify(role)}-{slugify(location)}"
        jobs.append(
            build_job_record(
                source=site["id"],
                company=site["name"].replace(" Careers", ""),
                role=role,
                url=synthetic_url,
                description=f"{role} role at Kuda in {location}. {job_type}.",
                location=location,
                tech_seed=job_type,
            )
        )
        if len(jobs) >= limit:
            break
    return jobs


def parse_chowdeck_company(limit: int, site: dict) -> List[Dict[str, object]]:
    payload = render_dynamic_jobs(site["id"], site["url"])
    jobs: List[Dict[str, object]] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        role = normalize_whitespace(item.get("role") or "")
        department = normalize_whitespace(item.get("department") or "")
        location = normalize_whitespace(item.get("location") or "Nigeria")
        job_type = normalize_whitespace(item.get("jobType") or "")
        if not is_target_role(role, department, location, job_type):
            continue
        jobs.append(
            build_job_record(
                source=site["id"],
                company=site["name"].replace(" Careers", ""),
                role=role,
                url=item.get("href") or site["url"],
                description=f"{department} role at Chowdeck in {location}. {job_type}.",
                location=location,
                tech_seed=f"{department} {job_type}",
            )
        )
        if len(jobs) >= limit:
            break
    return jobs


def parse_germany_board(limit: int, site: dict) -> List[Dict[str, object]]:
    payload = render_dynamic_jobs(site["id"], site["url"])
    jobs: List[Dict[str, object]] = []
    seen = set()

    for item in payload:
        if not isinstance(item, dict):
            continue

        role = normalize_whitespace(item.get("role") or "")
        company = normalize_whitespace(item.get("company") or site["name"])
        location = normalize_whitespace(item.get("location") or "Germany")
        salary = normalize_whitespace(item.get("salary") or "")
        description = normalize_whitespace(item.get("description") or "")
        href = normalize_whitespace(item.get("href") or site["url"])
        tags = item.get("tags") or []
        tech_seed = " ".join(tag for tag in tags if isinstance(tag, str))

        if not role or not href:
            continue
        if not is_target_germany_role(role, description, tech_seed):
            continue

        dedupe_key = (role.lower(), company.lower(), href.lower())
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        jobs.append(
            build_job_record(
                source=site["id"],
                company=company,
                role=role,
                url=href,
                description=description or f"{role} role at {company} in {location}.",
                salary=salary,
                location=location,
                tech_seed=tech_seed,
            )
        )

    return sort_jobs_by_fit(jobs)[:limit]


def parse_company_sources(limit: int, allowed_ids: set[str] | None = None) -> List[Dict[str, object]]:
    config = load_job_sites_config()
    sites = config.get("sites") or []
    parser_map = {
        "arbeitnow-english-germany": parse_germany_board,
        "berlinstartupjobs-engineering": parse_germany_board,
        "chowdeck-careers": parse_chowdeck_company,
        "kuda-careers": parse_kuda_company,
        "moniepoint-careers": parse_moniepoint_company,
        "jobriver-germany-it": parse_germany_board,
        "pegel-visa-berlin": parse_germany_board,
        "piggyvest-careers": parse_piggyvest_company,
        "flutterwave-careers": parse_flutterwave_company,
        "wearedevelopers-germany": parse_germany_board,
    }

    jobs: List[Dict[str, object]] = []
    per_source_limit = max(3, limit // max(len(parser_map), 1))

    for site in sites:
        site_id = site.get("id")
        if allowed_ids is not None and site_id not in allowed_ids:
            continue
        parser = parser_map.get(site_id)
        if not parser:
            continue
        if site.get("access") != "working":
            continue
        try:
            jobs.extend(parser(per_source_limit, site))
        except FetchError:
            continue
    return jobs[:limit]


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


def balanced_merge(job_lists: List[List[Dict[str, object]]], limit: int) -> List[Dict[str, object]]:
    merged: List[Dict[str, object]] = []
    max_len = max((len(job_list) for job_list in job_lists), default=0)
    for idx in range(max_len):
        for job_list in job_lists:
            if idx < len(job_list):
                merged.append(job_list[idx])
                if len(merged) >= limit:
                    return merged
    return merged


def main(limit: int = 50) -> int:
    initialize_database(DB_PATH)
    remoteok_target = max(12, limit // 4)
    hn_target = max(12, limit // 4)
    nigeria_target = max(8, limit // 6)
    company_target = max(6, limit // 10)
    germany_target = max(10, limit // 5)

    remote_jobs = parse_remoteok(remoteok_target)
    hn_jobs = parse_hn(hn_target)
    jobberman_jobs = parse_jobberman(nigeria_target)
    myjobmag_jobs = parse_myjobmag(nigeria_target)
    hotnigerianjobs_jobs = parse_hotnigerianjobs(nigeria_target)
    germany_jobs = parse_company_sources(
        germany_target,
        allowed_ids={
            "arbeitnow-english-germany",
            "berlinstartupjobs-engineering",
            "pegel-visa-berlin",
            "wearedevelopers-germany",
        },
    )
    company_jobs = parse_company_sources(
        company_target,
        allowed_ids={
            "chowdeck-careers",
            "kuda-careers",
            "moniepoint-careers",
            "piggyvest-careers",
            "flutterwave-careers",
        },
    )
    jobs = deduplicate_jobs(
        balanced_merge(
            [jobberman_jobs, myjobmag_jobs, hotnigerianjobs_jobs, germany_jobs, company_jobs, remote_jobs, hn_jobs],
            limit * 2,
        )
    )
    jobs = sort_jobs_by_fit(jobs)[:limit]

    with get_connection(DB_PATH) as conn:
        for job in jobs:
            upsert_job(conn, job)

    by_source: Dict[str, int] = {}
    for job in jobs:
        source = str(job["source"])
        by_source[source] = by_source.get(source, 0) + 1

    print(f"Stored {len(jobs)} jobs in {DB_PATH}")
    print(json.dumps(by_source, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    requested_limit = 50
    if len(sys.argv) > 1:
        requested_limit = int(sys.argv[1])
    raise SystemExit(main(requested_limit))
