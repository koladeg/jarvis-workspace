#!/usr/bin/env python3
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import sys

CREDENTIALS_FILE = Path.home() / '.openclaw' / 'workspace' / '.credentials' / 'youtube_oauth.json'
TOKEN_FILE = Path.home() / '.openclaw' / 'workspace' / '.credentials' / 'youtube_token.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']


def get_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        raise SystemExit('❌ Not authorized. Refresh YouTube auth/token first.')
    return build('youtube', 'v3', credentials=creds)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 scripts/youtube_delete.py <video_id>')
    video_id = sys.argv[1]
    youtube = get_service()
    youtube.videos().delete(id=video_id).execute()
    print(f'✓ Deleted video: {video_id}')
