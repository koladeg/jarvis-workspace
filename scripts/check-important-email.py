#!/usr/bin/env python3
import email
import email.utils
import imaplib
import json
import os
import re
from datetime import datetime, timedelta, timezone
from email.header import decode_header, make_header
from pathlib import Path

WORKSPACE = Path('/home/claw/.openclaw/workspace')
ENV_PATH = WORKSPACE / 'job_automation' / '.env'
PASSWORD_PATH = WORKSPACE / '.credentials' / 'gmail_app_password.txt'
STATE_PATH = WORKSPACE / 'memory' / 'email-check-state.json'

IMPORTANT_KEYWORDS = [
    'urgent', 'deadline', 'interview', 'meeting', 'payment', 'invoice', 'action required',
    'verify', 'verification', 'security alert', 'login', 'application', 'offer', 'contract',
    'approval', 'approve', 'due today', 'due tomorrow', 'response needed', 'important'
]
NOISY_HINTS = [
    'unsubscribe', 'newsletter', 'digest', 'promotion', 'promotions', 'no-reply', 'noreply',
    'notification', 'alerts@', 'mailer-daemon'
]


def load_env(path: Path):
    data = {}
    if not path.exists():
        return data
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        data[k.strip()] = v.strip()
    return data


def decode_text(value: str) -> str:
    if not value:
        return ''
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def extract_text_from_message(msg) -> str:
    texts = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get('Content-Disposition', ''))
            if ctype == 'text/plain' and 'attachment' not in disp.lower():
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or 'utf-8'
                    texts.append(payload.decode(charset, errors='replace'))
                except Exception:
                    pass
    else:
        if msg.get_content_type() == 'text/plain':
            try:
                payload = msg.get_payload(decode=True)
                charset = msg.get_content_charset() or 'utf-8'
                texts.append(payload.decode(charset, errors='replace'))
            except Exception:
                pass
    return '\n'.join(texts)


def score_message(subject: str, sender: str, snippet: str, flags: list[str]) -> tuple[int, list[str]]:
    haystack = ' '.join([subject, sender, snippet]).lower()
    reasons = []
    score = 0

    for kw in IMPORTANT_KEYWORDS:
        if kw in haystack:
            score += 2
            reasons.append(f'keyword:{kw}')

    if '\\Flagged' in flags:
        score += 4
        reasons.append('flagged')
    if '\\Seen' not in flags:
        score += 2
        reasons.append('unread')

    noisy = any(h in haystack for h in NOISY_HINTS)
    if noisy:
        score -= 2
        reasons.append('likely-newsletter')

    if re.search(r'(reply|re:|fwd:)', subject.lower()):
        score += 1
        reasons.append('threaded-conversation')

    return score, reasons


def main():
    env = load_env(ENV_PATH)
    account = env.get('JOB_AUTOMATION_EMAIL_FROM', 'jarviskolademail@gmail.com')
    password = os.environ.get('GMAIL_APP_PASSWORD')
    if not password and PASSWORD_PATH.exists():
        password = PASSWORD_PATH.read_text().strip()
    if not password:
        print(json.dumps({'ok': False, 'error': f'Missing Gmail app password at {PASSWORD_PATH}'}))
        raise SystemExit(1)

    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    cutoff_imap = cutoff.strftime('%d-%b-%Y')

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(account, password)
    mail.select('INBOX')

    status, data = mail.search(None, f'(SINCE "{cutoff_imap}")')
    if status != 'OK':
        print(json.dumps({'ok': False, 'error': 'IMAP search failed'}))
        raise SystemExit(1)

    ids = data[0].split()
    summaries = []
    for msg_id in ids[-50:]:  # cap for weekly scan
        status, meta = mail.fetch(msg_id, '(RFC822 FLAGS)')
        if status != 'OK' or not meta or meta[0] is None:
            continue

        raw = None
        flags = []
        for part in meta:
            if isinstance(part, tuple):
                raw = part[1]
                header = part[0].decode(errors='ignore') if isinstance(part[0], bytes) else str(part[0])
                m = re.search(r'FLAGS \((.*?)\)', header)
                if m:
                    flags = m.group(1).split()
        if not raw:
            continue

        msg = email.message_from_bytes(raw)
        subject = decode_text(msg.get('Subject', ''))
        sender = decode_text(msg.get('From', ''))
        date_hdr = msg.get('Date')
        try:
            dt = email.utils.parsedate_to_datetime(date_hdr)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dt = dt.astimezone(timezone.utc)
        except Exception:
            dt = None

        body = extract_text_from_message(msg)
        snippet = re.sub(r'\s+', ' ', body).strip()[:240]
        score, reasons = score_message(subject, sender, snippet, flags)

        summaries.append({
            'subject': subject,
            'from': sender,
            'date': dt.isoformat() if dt else date_hdr,
            'flags': flags,
            'score': score,
            'reasons': reasons,
            'snippet': snippet,
        })

    mail.logout()

    important = [m for m in summaries if m['score'] >= 3]
    important.sort(key=lambda x: (x['score'], x['date']), reverse=True)
    summaries.sort(key=lambda x: x['date'], reverse=True)

    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state = {
        'last_run': datetime.now(timezone.utc).isoformat(),
        'account': account,
        'checked_count': len(summaries),
        'important_count': len(important),
    }
    STATE_PATH.write_text(json.dumps(state, indent=2))

    result = {
        'ok': True,
        'account': account,
        'window_days': 7,
        'checked_count': len(summaries),
        'important_count': len(important),
        'important': important[:10],
        'recent': summaries[:10],
        'state_file': str(STATE_PATH),
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
