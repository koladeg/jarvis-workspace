#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import urllib.error
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
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            payload = e.read().decode("utf-8", errors="replace")
            detail = f" | body={payload}"
        except Exception:
            pass
        raise RuntimeError(f"telegram api POST failed: HTTP {e.code} {e.reason}{detail}") from e


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


def strip_reply_tag(text: str) -> str:
    return re.sub(r"^\[\[\s*reply_to[^\]]*\]\]\s*", "", text, count=1, flags=re.IGNORECASE).strip()


def send_message(token: str, chat_id: str, text: str, reply_to_message_id: int | None = None):
    clean_text = strip_reply_tag(text)[:3500] or "OK"
    data = {"chat_id": chat_id, "text": clean_text}
    if reply_to_message_id:
        data["reply_to_message_id"] = str(reply_to_message_id)
    try:
        return api_post(f"https://api.telegram.org/bot{token}/sendMessage", data)
    except Exception as e:
        if reply_to_message_id:
            fallback = {"chat_id": chat_id, "text": clean_text}
            try:
                return api_post(f"https://api.telegram.org/bot{token}/sendMessage", fallback)
            except Exception:
                pass
        raise e


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
    for p in payloads:
        if isinstance(p, dict):
            add(p.get("text"))
            add(p.get("message"))
            add(p.get("reply"))

    meta = result.get("meta", {}) if isinstance(result, dict) else {}
    for key in ("text", "reply", "message"):
        if isinstance(meta, dict):
            add(meta.get(key))

    for key in ("text", "reply", "message"):
        if isinstance(data, dict):
            add(data.get(key))

    # Some CLI responses can nest user-visible text deeper than the normal result/payloads shape.
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
    return "\n\n".join(t for t in texts if t).strip()


def generate_reply_via_openclaw(user_text: str) -> str:
    prompt = (
        "You are Robin, Kolade's dedicated private research agent on Telegram. "
        "Reply naturally and helpfully, in plain English. Be concise but thoughtful. "
        "For simple greetings, answer briefly. For substantive questions, reason properly. "
        "For web browsing and website research, use agent-browser as the default browser tool; it is installed at /usr/bin/agent-browser and available in PATH. "
        "Do not claim the browser is unavailable unless you actually tried and hit a real error. "
        "If a web task needs browsing, behave as if agent-browser is your normal path. "
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

    # Last-resort fallback: avoid asking the user to resend when the model likely already replied.
    return "I got your message, but my reply parser glitched. Ask me again in one line and I should answer normally."


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
