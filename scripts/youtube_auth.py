#!/usr/bin/env python3
"""
YouTube OAuth Authorization
Run once to authorize OpenClaw to access your YouTube channel
"""

import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = Path.home() / ".openclaw" / "workspace" / ".credentials" / "youtube_oauth.json"
TOKEN_FILE = Path.home() / ".openclaw" / "workspace" / ".credentials" / "youtube_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authorize():
    """Get authorization from user"""
    creds = None
    
    # Load existing token if available
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        print("✓ Using existing authorization")
        return creds
    
    # Create new authorization
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE), SCOPES
    )
    
    creds = flow.run_local_server(port=0)
    
    # Save token for future use
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())
    
    print(f"✓ Authorization complete!")
    print(f"✓ Token saved to: {TOKEN_FILE}")
    return creds

if __name__ == "__main__":
    try:
        creds = authorize()
        print(f"✓ Ready to upload videos!")
    except Exception as e:
        print(f"❌ Authorization failed: {e}")
        exit(1)
