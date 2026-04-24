#!/usr/bin/env python3
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive.file',
]
CREDENTIALS = Path('/home/claw/.openclaw/workspace/.credentials/google_slides_oauth_6263.json')
TOKEN = Path('/home/claw/.openclaw/workspace/.credentials/google_slides_token.json')

flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS), SCOPES)
creds = flow.run_local_server(host='127.0.0.1', port=8000, open_browser=False, prompt='consent', authorization_prompt_message='Open this URL in your browser: {url}', success_message='Google Slides auth complete. You can close this tab.')
TOKEN.write_text(creds.to_json())
print(f'SAVED_TOKEN={TOKEN}')
