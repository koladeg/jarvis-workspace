#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/home/claw/.openclaw/workspace")
RESEARCH_WORKSPACE = Path("/home/claw/.openclaw/workspace-research")
TOKEN_FILE = WORKSPACE / ".credentials" / "telegram_research_agent_bot_token.txt"
TIMEOUT_SECONDS = 7200
THINKING = "low"
AGENT_ID = "research"


def api_post(url: str, data: dict):
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def get_token() -> str:
    token = TOKEN_FILE.read_text().strip()
    if not token:
        raise RuntimeError(f"Missing token in {TOKEN_FILE}")
    return token


def send_message(token: str, chat_id: str, text: str, reply_to_message_id: int | None = None):
    data = {"chat_id": chat_id, "text": (text or "OK")[:3500]}
    if reply_to_message_id:
        data["reply_to_message_id"] = str(reply_to_message_id)
    return api_post(f"https://api.telegram.org/bot{token}/sendMessage", data)


def extract_reply_text(data: dict) -> str:
    texts = []

    def add(value):
        if value is None:
            return
        text = str(value).strip()
        if text and text not in texts:
            texts.append(text)

    result = data.get("result", {}) if isinstance(data, dict) else {}
    payloads = result.get("payloads", []) if isinstance(result, dict) else []
    for payload in payloads:
        if isinstance(payload, dict):
            add(payload.get("text"))
            add(payload.get("message"))
            add(payload.get("reply"))

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in {"systemPromptReport", "usage", "lastCallUsage", "agentMeta", "bootstrapTruncation", "skills", "injectedWorkspaceFiles"}:
                    continue
                if key in {"text", "reply", "message", "content", "output"} and isinstance(value, str):
                    add(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return "\n\n".join(texts).strip()


def run_agent(user_text: str) -> str:
    prompt = (
        "You are Robin, Kolade's dedicated private research agent on Telegram. "
        "Reply naturally and helpfully, in plain English. Be concise but thoughtful. "
        "For simple greetings, answer briefly. For substantive questions, reason properly. "
        "For web browsing and website research, use agent-browser as the default browser tool; it is installed at /usr/bin/agent-browser and available in PATH. "
        "Do not claim the browser is unavailable unless you actually tried and hit a real error. "
        "If a web task needs browsing, behave as if agent-browser is your normal path. "
        "Use Codex-quality reasoning for substantive research and implementation tasks. "
        "Do not mention internal tools, prompts, hidden context, or system mechanics. "
        "User message: " + user_text
    )
    session_id = f"robin-private-{AGENT_ID}-job-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    cmd = [
        "/home/claw/.npm-global/bin/openclaw",
        "agent",
        "--agent",
        AGENT_ID,
        "--session-id",
        session_id,
        "--message",
        prompt,
        "--thinking",
        THINKING,
        "--timeout",
        str(TIMEOUT_SECONDS),
        "--json",
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS + 60,
        cwd=str(RESEARCH_WORKSPACE),
    )
    if result.returncode != 0:
        stderr = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(stderr or f"openclaw agent exited {result.returncode}")
    stdout = (result.stdout or "").strip()
    if not stdout:
        raise RuntimeError("openclaw agent returned empty stdout")
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        start = stdout.find("{")
        end = stdout.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise RuntimeError(stdout[:400])
        data = json.loads(stdout[start:end + 1])
    reply = extract_reply_text(data)
    if not reply:
        raise RuntimeError("reply parser returned no user-visible text")
    return reply


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat-id", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--reply-to", type=int)
    args = parser.parse_args()

    token = get_token()
    try:
        reply = run_agent(args.message)
    except Exception as exc:
        reply = (
            "I started the background run, but it failed before I could finish it. "
            f"Error: {exc}"
        )
    send_message(token, args.chat_id, reply, args.reply_to)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
