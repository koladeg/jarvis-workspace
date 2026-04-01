---
name: adugboinsure-video-pipeline
description: Edit and publish AdugboInsure videos with the approved overlay workflow. Use when a new AdugboInsure source video is available locally or in Drive and the task is to run the full pipeline: download or locate the source MP4, apply the approved replacement image as a full-width centered overlay for the first 3 seconds and last 5 seconds, preserve original audio, verify preview frames and runtime, upload to YouTube, and return the actual video ID/link.
---

# AdugboInsure Video Pipeline

Use the single-run script for the approved production flow:

```bash
bash /home/claw/.openclaw/workspace/skills/adugboinsure-video-pipeline/scripts/run-approved-video-pipeline.sh \
  <input_video> \
  /home/claw/.openclaw/workspace/outputs/assets/adugboinsure_intro_replacement.jpg \
  "<youtube title>" \
  "<youtube description>"
```

## Approved edit spec

- Start from the raw MP4.
- Use the approved replacement image, not the old banner.
- Overlay the image on top of the existing video timeline.
- Scale the image to full video width and center it vertically.
- Show the overlay for the first 3 seconds and the last 5 seconds only.
- Do not append intro/outro clips.
- Do not add new audio; preserve the original audio.
- Before upload, generate preview frames at 2 seconds and 2 seconds before the end.
- Before upload, verify final runtime matches the source runtime.
- Only report success after returning the real YouTube video ID and URL.

## Reporting contract

Always report state in this order:

1. source located/downloaded
2. edit rendered
3. runtime verified
4. upload complete with video ID/link

If any step fails, say exactly which step failed. Never imply upload success without the returned YouTube ID/link.

## Guardrail from the failed run

A previous export became far too long because the image overlay render was not hard-limited to the source duration. Always preserve source duration with an explicit duration cap and verify it before upload.
