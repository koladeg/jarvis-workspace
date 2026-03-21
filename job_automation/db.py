#!/usr/bin/env python3
"""SQLite helpers for the job automation workflow.

This module owns the database schema and common insert/update helpers.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "jobs.sqlite3"

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    url TEXT NOT NULL,
    tech_stack TEXT,
    salary TEXT,
    location TEXT,
    description TEXT,
    pull_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    applied_at TEXT,
    application_status TEXT NOT NULL DEFAULT 'not_started',
    cv_path TEXT,
    cover_letter_path TEXT,
    package_dir TEXT,
    notes TEXT,
    email_status TEXT NOT NULL DEFAULT 'pending',
    email_sent_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE,
    UNIQUE(job_id)
);

CREATE TRIGGER IF NOT EXISTS jobs_updated_at
AFTER UPDATE ON jobs
FOR EACH ROW
BEGIN
    UPDATE jobs SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS applications_updated_at
AFTER UPDATE ON applications
FOR EACH ROW
BEGIN
    UPDATE applications SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;
"""


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection(db_path: Path = DB_PATH):
    ensure_dirs()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()



def initialize_database(db_path: Path = DB_PATH) -> Path:
    """Create the database and schema if they do not exist."""
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
    return db_path



def upsert_job(conn: sqlite3.Connection, job: Dict[str, Any]) -> None:
    tech_stack = job.get("tech_stack") or []
    if isinstance(tech_stack, (list, tuple, set)):
        tech_stack = json.dumps(sorted(set(tech_stack)))

    conn.execute(
        """
        INSERT INTO jobs (
            job_id, source, company, role, url, tech_stack, salary,
            location, description, pull_date, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(job_id) DO UPDATE SET
            source = excluded.source,
            company = excluded.company,
            role = excluded.role,
            url = excluded.url,
            tech_stack = excluded.tech_stack,
            salary = excluded.salary,
            location = excluded.location,
            description = excluded.description,
            pull_date = excluded.pull_date,
            status = excluded.status
        """,
        (
            job["job_id"],
            job["source"],
            job["company"],
            job["role"],
            job["url"],
            tech_stack,
            job.get("salary"),
            job.get("location"),
            job.get("description"),
            job["pull_date"],
            job.get("status", "new"),
        ),
    )

    conn.execute(
        """
        INSERT INTO applications (job_id)
        VALUES (?)
        ON CONFLICT(job_id) DO NOTHING
        """,
        (job["job_id"],),
    )



def fetch_jobs(conn: sqlite3.Connection, limit: Optional[int] = None, status: Optional[str] = None) -> List[sqlite3.Row]:
    query = """
        SELECT j.*, a.application_status, a.cv_path, a.cover_letter_path, a.package_dir
        FROM jobs j
        LEFT JOIN applications a ON a.job_id = j.job_id
    """
    clauses = []
    params: List[Any] = []

    if status:
        clauses.append("j.status = ?")
        params.append(status)

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY j.pull_date DESC, j.created_at DESC"

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    return list(conn.execute(query, params).fetchall())



def update_application_paths(
    conn: sqlite3.Connection,
    job_id: str,
    cv_path: str,
    cover_letter_path: str,
    package_dir: str,
    application_status: str = "documents_ready",
) -> None:
    conn.execute(
        """
        UPDATE applications
        SET cv_path = ?, cover_letter_path = ?, package_dir = ?, application_status = ?
        WHERE job_id = ?
        """,
        (cv_path, cover_letter_path, package_dir, application_status, job_id),
    )



def mark_email_sent(conn: sqlite3.Connection, job_ids: Iterable[str]) -> None:
    conn.executemany(
        """
        UPDATE applications
        SET email_status = 'sent', email_sent_at = CURRENT_TIMESTAMP
        WHERE job_id = ?
        """,
        [(job_id,) for job_id in job_ids],
    )


if __name__ == "__main__":
    path = initialize_database()
    print(f"Database ready: {path}")
