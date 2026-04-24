#!/usr/bin/env python3
import json
import secrets
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REDIRECT_URI = "http://127.0.0.1:8000/"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive.file',
]
CREDENTIALS_PATH = Path('/home/claw/.openclaw/workspace/.credentials/google_slides_oauth_6263.json')
TOKEN_PATH = Path('/home/claw/.openclaw/workspace/.credentials/google_slides_token.json')
STATE_PATH = Path('/home/claw/.openclaw/workspace/.credentials/google_slides_manual_state.json')


creds_payload = json.loads(CREDENTIALS_PATH.read_text())
installed = creds_payload.get('installed', {})
CLIENT_ID = installed['client_id']
CLIENT_SECRET = installed['client_secret']


def build_auth_url():
    state = secrets.token_urlsafe(24)
    payload = {
        'state': state,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
        'prompt': 'consent',
    }
    STATE_PATH.write_text(json.dumps({'state': state}))
    print(AUTH_URI + '?' + urllib.parse.urlencode(payload))


def exchange(callback_url: str):
    saved = json.loads(STATE_PATH.read_text())
    parsed = urllib.parse.urlparse(callback_url.strip())
    qs = urllib.parse.parse_qs(parsed.query)
    state = qs.get('state', [''])[0]
    code = qs.get('code', [''])[0]
    if not code:
        raise SystemExit('No code found in callback URL')
    if state != saved.get('state'):
        raise SystemExit('State mismatch; generate a fresh auth URL and retry')
    data = urllib.parse.urlencode({
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }).encode('utf-8')
    req = urllib.request.Request(TOKEN_URI, data=data, method='POST')
    with urllib.request.urlopen(req) as resp:
        token = json.loads(resp.read().decode('utf-8'))
    TOKEN_PATH.write_text(json.dumps(token, indent=2))
    print(f'SAVED_TOKEN={TOKEN_PATH}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('Usage: google_slides_manual_oauth.py auth-url | exchange <callback_url>')
    if sys.argv[1] == 'auth-url':
        build_auth_url()
    elif sys.argv[1] == 'exchange':
        if len(sys.argv) < 3:
            raise SystemExit('Provide callback URL')
        exchange(sys.argv[2])
    else:
        raise SystemExit('Unknown command')
