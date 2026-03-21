#!/usr/bin/env python3
"""Generate tailored CV and cover letter PDFs for jobs stored in SQLite.

This script uses simple text templates and a lightweight built-in PDF writer,
so it can run without third-party dependencies.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Iterable, List, Sequence

from db import DB_PATH, fetch_jobs, get_connection, initialize_database, update_application_paths

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
PACKAGES_DIR = OUTPUT_DIR / "packages"

CANDIDATE = {
    "name": "Kolade Gureje",
    "phone": "+234 8079366207",
    "email": "koladegureje@gmail.com",
    "location": "Lagos, Nigeria",
    "portfolio": "https://koladeg.github.io/",
    "linkedin": "linkedin.com/in/kolade-gureje",
    "github": "github.com/koladeg",
    "summary": (
        "Software developer with 4+ years building mobile and web applications "
        "across healthcare, logistics, and fintech. Strong in React Native, React, "
        "TypeScript, Python, and API integrations, with hands-on delivery experience "
        "in both startup and enterprise environments."
    ),
    "experience": [
        "Founder, AdugboInsure (2024-Present): building health-insurance growth software for state agencies.",
        "Software Developer / Deputy Manager, SIFAX (2020-Present): shipped React Native apps, backend integrations, and production support workflows.",
        "Project Lead Developer, University College Hospital (2024): led mhGAP mobile app delivery for clinical use, supporting 250+ patient visits.",
        "Front-End Developer, NeighborTailor (2019-2022): built UI features for a distributed remote team.",
    ],
    "core_skills": [
        "React Native", "React", "TypeScript", "JavaScript", "Python", "Node.js",
        "REST APIs", "Redux", "Firebase", "Expo", "AWS", "Git", "Docker"
    ],
}


class SimplePDF:
    """Very small PDF writer for plain-text content."""

    def __init__(self, title: str):
        self.title = title

    def write_text_pdf(self, path: Path, lines: Sequence[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        page_height = 792
        left_margin = 50
        top_margin = 760
        line_height = 15
        max_lines_per_page = 45

        pages = [list(lines[i:i + max_lines_per_page]) for i in range(0, len(lines), max_lines_per_page)] or [[]]
        objects: List[bytes] = []

        def add_object(payload: bytes) -> int:
            objects.append(payload)
            return len(objects)

        font_obj = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

        page_obj_ids = []
        content_obj_ids = []
        pages_obj_placeholder = len(objects) + 1

        for page_lines in pages:
            commands = [b"BT", b"/F1 11 Tf"]
            y = top_margin
            for line in page_lines:
                safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
                commands.append(f"1 0 0 1 {left_margin} {y} Tm ({safe}) Tj".encode("latin-1", errors="replace"))
                y -= line_height
            commands.append(b"ET")
            content_stream = b"\n".join(commands)
            content_obj_ids.append(add_object(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(content_stream), content_stream)))

        pages_obj_id = add_object(b"")
        for content_id in content_obj_ids:
            page_payload = (
                f"<< /Type /Page /Parent {pages_obj_id} 0 R /MediaBox [0 0 612 {page_height}] "
                f"/Resources << /Font << /F1 {font_obj} 0 R >> >> /Contents {content_id} 0 R >>"
            ).encode("ascii")
            page_obj_ids.append(add_object(page_payload))

        kids = " ".join(f"{page_id} 0 R" for page_id in page_obj_ids)
        objects[pages_obj_id - 1] = f"<< /Type /Pages /Kids [ {kids} ] /Count {len(page_obj_ids)} >>".encode("ascii")
        catalog_obj = add_object(f"<< /Type /Catalog /Pages {pages_obj_id} 0 R >>".encode("ascii"))

        pdf = bytearray(b"%PDF-1.4\n")
        offsets = [0]
        for index, obj in enumerate(objects, start=1):
            offsets.append(len(pdf))
            pdf.extend(f"{index} 0 obj\n".encode("ascii"))
            pdf.extend(obj)
            pdf.extend(b"\nendobj\n")

        xref_offset = len(pdf)
        pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        pdf.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        pdf.extend(
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_obj} 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
        )
        path.write_bytes(pdf)



def slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")



def parse_stack(raw: str) -> List[str]:
    if not raw:
        return []
    try:
        value = json.loads(raw)
        if isinstance(value, list):
            return value
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in raw.split(",") if item.strip()]



def select_relevant_skills(job_stack: Iterable[str]) -> List[str]:
    stack = list(job_stack)
    matched = [skill for skill in stack if skill in CANDIDATE["core_skills"]]
    remainder = [skill for skill in CANDIDATE["core_skills"] if skill not in matched]
    return matched + remainder[: max(0, 10 - len(matched))]



def build_cv_lines(job: dict, skills: Sequence[str]) -> List[str]:
    lines = [
        CANDIDATE["name"],
        f"{CANDIDATE['phone']} | {CANDIDATE['email']} | {CANDIDATE['location']}",
        f"Portfolio: {CANDIDATE['portfolio']} | GitHub: {CANDIDATE['github']}",
        "",
        f"Target Role: {job['role']} at {job['company']}",
        "Professional Summary",
    ]
    lines.extend(textwrap.wrap(
        f"{CANDIDATE['summary']} Tailored for roles requiring {', '.join(skills[:6]) or 'modern product engineering'}.",
        width=90,
    ))
    lines.extend(["", "Relevant Skills"])
    lines.extend(textwrap.wrap(", ".join(skills), width=90))
    lines.extend(["", "Selected Experience"])
    for item in CANDIDATE["experience"]:
        lines.extend(textwrap.wrap(f"- {item}", width=90))
    lines.extend(["", "Why This Role Fits"])
    lines.extend(textwrap.wrap(
        f"This opportunity highlights {', '.join(parse_stack(job['tech_stack'])[:6]) or 'remote product development'}, "
        f"which aligns with Kolade's recent delivery work across production mobile/web products.",
        width=90,
    ))
    lines.extend(["", f"Job URL: {job['url']}"])
    return lines



def build_cover_letter_lines(job: dict, skills: Sequence[str]) -> List[str]:
    stack = parse_stack(job["tech_stack"])
    lines = [
        f"Cover Letter - {job['company']}",
        "",
        f"Dear {job['company']} Hiring Team,",
        "",
    ]
    intro = (
        f"I am excited to apply for the {job['role']} role. My background in React Native, React, "
        f"TypeScript, Python, and API-driven product delivery maps well to the technical needs in this opening."
    )
    lines.extend(textwrap.wrap(intro, width=90))
    lines.append("")
    body = (
        f"From shipping production apps at SIFAX to leading the mhGAP healthcare app rollout at University College Hospital, "
        f"I have built software in environments where reliability, speed, and collaboration matter. "
        f"For this role, I would especially bring value around {', '.join(skills[:5])}."
    )
    lines.extend(textwrap.wrap(body, width=90))
    lines.append("")
    if stack:
        stack_para = f"The technologies mentioned in your posting — {', '.join(stack[:8])} — overlap strongly with my recent work and learning priorities."
        lines.extend(textwrap.wrap(stack_para, width=90))
        lines.append("")
    closing = (
        f"I would welcome the chance to discuss how I can contribute to {job['company']}. "
        f"Thank you for your time and consideration."
    )
    lines.extend(textwrap.wrap(closing, width=90))
    lines.extend([
        "",
        "Sincerely,",
        CANDIDATE["name"],
        CANDIDATE["email"],
        CANDIDATE["phone"],
        f"Job URL: {job['url']}",
    ])
    return lines



def main(limit: int = 50) -> int:
    initialize_database(DB_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    pdf_writer = SimplePDF("Job Application Package")

    with get_connection(DB_PATH) as conn:
        jobs = [dict(row) for row in fetch_jobs(conn, limit=limit)]
        for job in jobs:
            package_name = f"{slugify(job['company'])}_{slugify(job['role'])}_{job['job_id']}"
            package_dir = PACKAGES_DIR / package_name
            package_dir.mkdir(parents=True, exist_ok=True)

            stack = parse_stack(job.get("tech_stack") or "")
            skills = select_relevant_skills(stack)

            cv_path = package_dir / "cv.pdf"
            cover_path = package_dir / "cover_letter.pdf"
            link_path = package_dir / "job_link.txt"

            pdf_writer.write_text_pdf(cv_path, build_cv_lines(job, skills))
            pdf_writer.write_text_pdf(cover_path, build_cover_letter_lines(job, skills))
            link_path.write_text(f"{job['role']} at {job['company']}\n{job['url']}\n", encoding="utf-8")

            update_application_paths(
                conn,
                job_id=job["job_id"],
                cv_path=str(cv_path),
                cover_letter_path=str(cover_path),
                package_dir=str(package_dir),
            )

    print(f"Generated packages for {len(jobs)} jobs in {PACKAGES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
