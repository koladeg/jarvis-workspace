#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a structured lesson to memory/mistakes-log.md")
    parser.add_argument("--mistake", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--root-cause", required=True)
    parser.add_argument("--guardrail", required=True)
    parser.add_argument("--pattern", default="TBD")
    parser.add_argument("--status", default="logged")
    args = parser.parse_args()

    workspace = Path("/home/claw/.openclaw/workspace")
    log_path = workspace / "memory" / "mistakes-log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if not log_path.exists():
        log_path.write_text("# Mistakes Log\n\n")

    now = datetime.now(timezone.utc)
    title = args.mistake.strip().replace("\n", " ")
    entry = (
        f"## {now:%Y-%m-%d %H:%M UTC}: {title}\n"
        f"- **What**: {args.mistake.strip()}\n"
        f"- **Context**: {args.context.strip()}\n"
        f"- **Root cause**: {args.root_cause.strip()}\n"
        f"- **Pattern**: {args.pattern.strip()}\n"
        f"- **Guardrail**: {args.guardrail.strip()}\n"
        f"- **Status**: {args.status.strip()}\n\n"
    )

    with log_path.open("a", encoding="utf-8") as f:
        f.write(entry)

    print(log_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
