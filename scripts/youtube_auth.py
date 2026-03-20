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
    
    # Create flow for manual auth code entry
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE), SCOPES
    )
    
    # Generate auth URL
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print("\n🔐 YouTube Authorization Required")
    print("=" * 60)
    print("1. Open this URL on your LOCAL MACHINE (not on the server):")
    print(f"\n{auth_url}\n")
    print("2. Click 'Allow'")
    print("3. You'll get an auth code (or be redirected)")
    print("4. Copy the code and paste it below")
    print("=" * 60)
    
    auth_code = input("\nPaste auth code here: ").strip()
    
    try:
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        # Save token for future use
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        
        print(f"\n✓ Authorization complete!")
        print(f"✓ Token saved to: {TOKEN_FILE}")
        return creds
    except Exception as e:
        print(f"❌ Authorization failed: {e}")
        return None

if __name__ == "__main__":
    try:
        creds = authorize()
        print(f"✓ Ready to upload videos!")
    except Exception as e:
        print(f"❌ Authorization failed: {e}")
        exit(1)
