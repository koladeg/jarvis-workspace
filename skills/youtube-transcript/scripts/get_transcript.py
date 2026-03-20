#!/usr/bin/env python3
"""
YouTube Transcript Extractor
Fetches transcripts from YouTube videos using yt-dlp
"""

import sys
import subprocess
import json
import os
from pathlib import Path

def get_youtube_id(url):
    """Extract video ID from YouTube URL"""
    if "youtube.com" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    return None

def get_transcript(url):
    """Fetch transcript from YouTube video"""
    video_id = get_youtube_id(url)
    if not video_id:
        print(f"❌ Invalid YouTube URL: {url}")
        sys.exit(1)
    
    # Create transcripts directory
    transcripts_dir = Path.home() / ".openclaw" / "workspace" / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = transcripts_dir / f"{video_id}.txt"
    
    # Use yt-dlp to fetch subtitles
    cmd = [
        "yt-dlp",
        "--write-sub",
        "--sub-lang", "en",
        "--skip-download",
        "-o", str(transcripts_dir / f"{video_id}"),
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"❌ Failed to fetch transcript: {result.stderr}")
            sys.exit(1)
        
        # Find subtitle file (yt-dlp creates .vtt or .srt)
        subtitle_files = list(transcripts_dir.glob(f"{video_id}*.vtt")) + \
                        list(transcripts_dir.glob(f"{video_id}*.srt"))
        
        if not subtitle_files:
            print(f"❌ No subtitles found for video {video_id}")
            sys.exit(1)
        
        subtitle_file = subtitle_files[0]
        
        # Parse transcript from subtitle file
        transcript_text = parse_subtitles(subtitle_file)
        
        # Save clean transcript
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
        
        print(f"✓ Transcript saved: {output_file}")
        print(f"\n--- Transcript Preview ---\n{transcript_text[:500]}...\n")
        print(f"Full transcript length: {len(transcript_text)} characters")
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout fetching transcript")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def parse_subtitles(subtitle_file):
    """Parse VTT or SRT subtitle file into plain text"""
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove VTT/SRT headers and timestamps
    lines = content.split('\n')
    transcript_lines = []
    
    for line in lines:
        # Skip empty lines, timestamps, and headers
        if line.strip() and not '-->' in line and 'WEBVTT' not in line:
            transcript_lines.append(line.strip())
    
    return '\n'.join(transcript_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 get_transcript.py <youtube_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    get_transcript(url)
