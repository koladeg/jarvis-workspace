#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

WORKSPACE = Path("/home/claw/.openclaw/workspace")
TOKEN_FILE = WORKSPACE / ".credentials" / "telegram_research_agent_bot_token.txt"
STATE_DIR = WORKSPACE / ".state"
OFFSET_FILE = STATE_DIR / "research-bot-update-offset.txt"
ALLOWED_CHAT_ID = "7101554375"
SESSION_ID = "robin-private-chat"
THINKING = os.environ.get("ROBIN_THINKING", "low")
TIMEOUT_SECONDS = os.environ.get("ROBIN_TIMEOUT", "120")

STATE_DIR.mkdir(parents=True, exist_ok=True)


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        return default


def api_get(url: str):
    with urllib.request.urlopen(url, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))


def api_post(url: str, data: dict):
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def get_token() -> str:
    token = read_text(TOKEN_FILE).strip()
    if not token:
        raise RuntimeError(f"Missing token in {TOKEN_FILE}")
    return token


def get_offset() -> int:
    raw = read_text(OFFSET_FILE, "0").strip()
    return int(raw or "0")


def set_offset(offset: int):
    OFFSET_FILE.write_text(str(offset))


def send_message(token: str, chat_id: str, text: str, reply_to_message_id: int | None = None):
    data = {"chat_id": chat_id, "text": text[:3500]}
    if reply_to_message_id:
        data["reply_to_message_id"] = str(reply_to_message_id)
    return api_post(f"https://api.telegram.org/bot{token}/sendMessage", data)


def extract_reply_text(data: dict) -> str:
    texts = []
    result = data.get("result", {}) if isinstance(data, dict) else {}
    payloads = result.get("payloads", []) if isinstance(result, dict) else []
    for p in payloads:
        if isinstance(p, dict) and p.get("text"):
            texts.append(str(p.get("text")).strip())

    meta = result.get("meta", {}) if isinstance(result, dict) else {}
    for key in ("text", "reply", "message"):
        if isinstance(meta, dict) and meta.get(key):
            texts.append(str(meta.get(key)).strip())

    for key in ("text", "reply", "message"):
        if isinstance(data, dict) and data.get(key):
            texts.append(str(data.get(key)).strip())

    return "\n\n".join(t for t in texts if t).strip()


def generate_reply_via_openclaw(user_text: str) -> str:
    prompt = (
        "You are Robin, Kolade's dedicated private research agent on Telegram. "
        "Reply naturally and helpfully, in plain English. Be concise but thoughtful. "
        "For simple greetings, answer briefly. For substantive questions, reason properly. "
        "Do not mention internal tools, prompts, hidden context, or system mechanics. "
        "User message: " + user_text
    )
    cmd = [
        "openclaw",
        "agent",
        "--session-id",
        SESSION_ID,
        "--message",
        prompt,
        "--thinking",
        THINKING,
        "--timeout",
        TIMEOUT_SECONDS,
        "--json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=int(TIMEOUT_SECONDS) + 30)
    if result.returncode != 0:
        stderr = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"openclaw agent failed: {stderr}")

    stdout = (result.stdout or "").strip()
    if not stdout:
        raise RuntimeError("openclaw agent returned empty stdout")

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        start = stdout.find("{")
        end = stdout.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise RuntimeError(f"openclaw agent returned non-JSON output: {stdout[:400]}")
        data = json.loads(stdout[start:end+1])

    reply = extract_reply_text(data)
    if reply:
        return reply

    return "I received your message, but I hit a reply-format issue on my side. Please send it once more and I’ll answer properly."


def handle_update(token: str, update: dict):
    message = update.get("message") or update.get("edited_message")
    if not message:
        return
    chat = message.get("chat", {})
    chat_id = str(chat.get("id", ""))
    if chat_id != ALLOWED_CHAT_ID:
        return
    if message.get("from", {}).get("is_bot"):
        return
    text = (message.get("text") or "").strip()
    if not text:
        send_message(token, chat_id, "Send me a text question and I’ll help.", message.get("message_id"))
        return
    try:
        reply = generate_reply_via_openclaw(text)
    except Exception as e:
        reply = f"I hit an error while preparing a reply: {e}"
    send_message(token, chat_id, reply, message.get("message_id"))


def run_once():
    token = get_token()
    offset = get_offset()
    url = (
        f"https://api.telegram.org/bot{token}/getUpdates?timeout=25"
        f"&allowed_updates=%5B%22message%22,%22edited_message%22%5D&offset={offset}"
    )
    data = api_get(url)
    if not data.get("ok"):
        raise RuntimeError(f"getUpdates failed: {data}")
    max_update_id = None
    for update in data.get("result", []):
        handle_update(token, update)
        max_update_id = update["update_id"]
    if max_update_id is not None:
        set_offset(max_update_id + 1)
        print(f"Processed through update_id {max_update_id}")
    else:
        print("No new updates")


if __name__ == "__main__":
    try:
        run_once()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
