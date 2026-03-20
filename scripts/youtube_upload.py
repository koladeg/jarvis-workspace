#!/usr/bin/env python3
"""
YouTube Video Upload
Uploads branded video to YouTube with metadata
"""

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import time

CREDENTIALS_FILE = Path.home() / ".openclaw" / "workspace" / ".credentials" / "youtube_oauth.json"
TOKEN_FILE = Path.home() / ".openclaw" / "workspace" / ".credentials" / "youtube_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """Get authenticated YouTube service"""
    creds = None
    
    # Load token if exists
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    # Refresh if needed
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    if not creds or not creds.valid:
        print("❌ Not authorized. Run: python3 scripts/youtube_auth.py")
        exit(1)
    
    return build("youtube", "v3", credentials=creds)

def upload_video(video_path, title, description, tags, category_id="27"):
    """
    Upload video to YouTube
    
    Args:
        video_path: Path to video file
        title: Video title
        description: Video description
        tags: List of tags
        category_id: YouTube category (27 = Education, 22 = People & Blogs, etc.)
    """
    
    video_file = Path(video_path)
    if not video_file.exists():
        print(f"❌ Video not found: {video_path}")
        return None
    
    print(f"🎬 Uploading: {title}")
    print(f"   File: {video_file.name} ({video_file.stat().st_size / 1024 / 1024:.1f} MB)")
    
    youtube = get_authenticated_service()
    
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": "unlisted",  # Unlisted as per requirement
            "madeForKids": False
        }
    }
    
    media = MediaFileUpload(str(video_file), chunksize=1024*1024, resumable=True)
    
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    
    # Upload with resume capability
    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"   Upload progress: {progress}%")
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    video_id = response["id"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    print(f"✓ Upload complete!")
    print(f"✓ Video ID: {video_id}")
    print(f"✓ URL: {video_url}")
    
    return {
        "video_id": video_id,
        "url": video_url,
        "title": title,
        "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_upload.py <video_path> [title] [description]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "AdugboInsure Video"
    description = sys.argv[3] if len(sys.argv) > 3 else "Learn about health insurance"
    
    result = upload_video(
        video_path,
        title=title,
        description=description,
        tags=["health insurance", "nigeria", "adugboinsure", "health", "community"]
    )
    
    if result:
        print(json.dumps(result, indent=2))
