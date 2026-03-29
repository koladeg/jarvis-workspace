---
name: adugboinsure-video-pipeline
description: Generate, brand, and publish AdugboInsure education videos from NotebookLM with cookie-based auth. Use when producing weekly or multi-week AdugboInsure video batches, especially when the user provides fresh NotebookLM cookies and expects the full flow: authenticate, generate videos sequentially, confirm completion, add AdugboInsure logo branding, and upload to Kolade's YouTube channel.
---

# AdugboInsure Video Pipeline

## Workflow

1. Authenticate NotebookLM CLI with fresh cookies from `.credentials/notebooklm_cookies.txt`.
2. Verify auth with `nlm login --check` and `nlm notebook list`.
3. Use notebook `Implementing Community-Based Health Insurance Schemes`.
4. Generate videos **sequentially** — never start multiple AdugboInsure videos at once.
5. After each generation, wait for `nlm studio status <notebook-id>` to show `completed` before starting the next.
6. After generation, treat the video as incomplete until branding is added.
7. Add AdugboInsure branding/logo with `scripts/add_adugboinsure_branding.sh` (or `scripts/brand_adugbo_video.sh` if needed).
8. Upload branded output to YouTube with `python3 scripts/youtube_upload.py ...` using stored YouTube OAuth credentials.
9. Record artifact ids, output paths, and uploaded YouTube URLs in the daily memory file.

## Rules

- Never request or accept NotebookLM cookies in a group chat.
- Prefer private/direct credential handoff only.
- Do not parallelize NotebookLM video generations for AdugboInsure.
- Branding + YouTube upload are part of the required workflow, not optional extras.

## Core commands

### Authenticate

```bash
nlm login -m -f /home/claw/.openclaw/workspace/.credentials/notebooklm_cookies.txt --force
nlm login --check
nlm notebook list
```

### Start one video

```bash
nlm create video <notebook-id> --format explainer --style classic --language en --focus "<prompt>" -y
```

### Poll completion

```bash
nlm studio status <notebook-id>
```

### Brand a downloaded video

```bash
bash scripts/add_adugboinsure_branding.sh <input.mp4> <output.mp4>
```

### Upload to YouTube

```bash
python3 scripts/youtube_upload.py <video_path> "<title>" "<description>"
```

## Current known gap

NotebookLM CLI in this workspace can create and status videos, but download/export may still require a separate retrieval step if the generated MP4 is not directly materialized locally. If download is not available via CLI, use the proven browser/cookie workflow or extend the pipeline with a deterministic export step before branding.
