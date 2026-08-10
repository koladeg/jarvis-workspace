#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_STATES = {"active", "watched", "stale", "rejected", "unknown"}
STRONG_METHODS = {"agent-browser", "official-fetch", "manual-official"}
STALE_OK_METHODS = STRONG_METHODS | {"historical-record"}
SUSPICIOUS_PATTERNS = [
    r"\b404\b",
    r"not found",
    r"application has been closed",
    r"applications close",
    r"error occurred",
    r"page not found",
    r"sorry",
]
ACTIVE_PATTERNS = [
    r"apply now",
    r"applications open",
    r"invites applications",
    r"submit your application",
    r"register",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fail(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 1


def read_tracker(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def validate_tracker(path: Path) -> int:
    data = read_tracker(path)
    meta = data.get("meta") or {}
    items = data.get("items")
    errors: list[str] = []

    if not isinstance(items, list):
        errors.append("tracker items must be a list")
        items = []

    for rule in (
        "Use states active, watched, stale, rejected, unknown.",
        "If shallow search/fetch results look thin, contradictory, or claim 404/closed, verify the official page with agent-browser before retaining or rejecting the opportunity.",
    ):
        if rule not in (meta.get("rules") or []):
            errors.append(f"missing meta rule: {rule}")

    for idx, item in enumerate(items):
        label = item.get("name") or f"items[{idx}]"
        state = item.get("state")
        source = item.get("source")
        last_verified = item.get("last_verified")
        method = item.get("verification_method")
        evidence = item.get("verification_evidence")
        verified_url = item.get("verified_url")
        verified_at = item.get("verified_at")

        if state not in ALLOWED_STATES:
            errors.append(f"{label}: invalid state {state!r}")
        if not source:
            errors.append(f"{label}: missing source")
        if not last_verified:
            errors.append(f"{label}: missing last_verified")
        if "deadline" not in item:
            errors.append(f"{label}: deadline key must exist (use null when unknown)")

        if state == "active":
            if method not in STRONG_METHODS:
                errors.append(f"{label}: active items require strong verification_method, got {method!r}")
        elif state == "stale":
            if method not in STALE_OK_METHODS:
                errors.append(f"{label}: stale items require official or historical verification_method, got {method!r}")
        elif state == "rejected":
            if method not in STRONG_METHODS:
                errors.append(f"{label}: rejected items require strong verification_method, got {method!r}")
        elif state == "unknown":
            if method and method not in {"shallow_only", *STRONG_METHODS, "historical-record"}:
                errors.append(f"{label}: unknown items have unsupported verification_method {method!r}")

        if state in {"active", "stale", "rejected"}:
            if not evidence:
                errors.append(f"{label}: missing verification_evidence")
            if not verified_url:
                errors.append(f"{label}: missing verified_url")
            if not verified_at:
                errors.append(f"{label}: missing verified_at")

        if method == "shallow_only" and state not in {"watched", "unknown"}:
            errors.append(f"{label}: shallow_only cannot be used for state {state}")

    if errors:
        for err in errors:
            print(f"VALIDATION_ERROR: {err}", file=sys.stderr)
        return 1

    print(json.dumps({
        "ok": True,
        "items": len(items),
        "validatedAt": utc_now(),
        "tracker": str(path),
    }, indent=2))
    return 0


def browser_text(url: str) -> tuple[str, str, str]:
    def run(cmd: list[str]) -> str:
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return proc.stdout.strip()

    run(["agent-browser", "open", url])
    final_url = run(["agent-browser", "get", "url"])
    title = run(["agent-browser", "get", "title"])
    text = run([
        "agent-browser",
        "eval",
        "document.body.innerText.slice(0,4000)",
    ])
    return final_url, title, text


def classify_text(text: str) -> tuple[str, str]:
    lower = text.lower()
    if any(re.search(p, lower) for p in ACTIVE_PATTERNS) and not any(re.search(p, lower) for p in [r"application has been closed", r"deadline"]):
        return "active", "Official page text shows an active application/apply signal."
    if "application has been closed" in lower or "applications close" in lower or re.search(r"deadline", lower):
        return "stale", "Official page text shows a closed/deadline-style signal; review exact text."
    if any(re.search(p, lower) for p in SUSPICIOUS_PATTERNS):
        return "unknown", "Shallow-style suspicious/negative signal found; browser verification needed before conclusions."
    return "watched", "Official page did not show a clear open/closed signal in the captured text."


def probe_url(url: str) -> int:
    final_url, title, text = browser_text(url)
    state, evidence = classify_text(text)
    print(json.dumps({
        "url": url,
        "verified_url": final_url,
        "title": title,
        "state": state,
        "verification_method": "agent-browser",
        "verification_evidence": evidence,
        "verified_at": utc_now(),
        "text_excerpt": text[:800],
    }, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Funding-source verification helpers")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_validate = sub.add_parser("validate-tracker", help="validate tracker verification fields")
    p_validate.add_argument("tracker")

    p_probe = sub.add_parser("probe-url", help="probe a URL with agent-browser and emit a starter classification")
    p_probe.add_argument("url")

    args = parser.parse_args()
    if args.cmd == "validate-tracker":
        return validate_tracker(Path(args.tracker))
    if args.cmd == "probe-url":
        return probe_url(args.url)
    return fail("unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
