---
name: google-slides-safe
description: Create, edit, and export Google Slides decks with explicit credentials, layout presets, and least-privilege Google scopes. Use when you need a safer alternative to ad-hoc Slides automation for pitch decks, reports, client presentations, or reusable deck generation workflows, especially when you want no hardcoded account, no hidden credential path, optional Google Drive image support, and no broad Gmail/Calendar scopes.
---

# google-slides-safe

Build Google Slides decks through the official Google Slides + Drive APIs with explicit auth and minimal scope.

## Overview

Use this skill when you want to automate slide creation safely. The bundled CLI requires an explicit auth mode and explicit credential path every time. It never assumes a default Google account, never reads hidden CLI state, and limits scopes to Slides + Drive file access.

## Workflow

1. Prepare a JSON deck spec.
2. Verify auth with `auth-check`.
3. Create the deck with `create-from-spec`.
4. Optionally export the deck to PDF.

## Guardrails

- Always pass `--auth-mode` explicitly.
- Always pass `--credentials` explicitly.
- Prefer `service-account` for isolated automation where a shared Drive folder is available.
- Prefer `oauth` only when the deck must live in a personal Google account.
- Use only these scopes:
  - `https://www.googleapis.com/auth/presentations`
  - `https://www.googleapis.com/auth/drive.file`
- Do not add Gmail, Calendar, Contacts, People, or Tasks scopes unless the task truly requires them.
- Do not hardcode email addresses, token paths, or credential paths inside the script.
- Use `--publish-drive-images` only when you intentionally want referenced Drive image files to become link-readable for Slides ingestion.

## Quick start

### 1) Verify auth

```bash
python3 skills/google-slides-safe/scripts/slides_cli.py auth-check \
  --auth-mode service-account \
  --credentials /path/to/service-account.json
```

### 2) Create a deck from spec

```bash
python3 skills/google-slides-safe/scripts/slides_cli.py create-from-spec \
  --auth-mode service-account \
  --credentials /path/to/service-account.json \
  --spec skills/google-slides-safe/references/pitch_deck_spec.example.json \
  --export-pdf outputs/adugboinsure-pitch-deck.pdf
```

### 3) Use Drive image ids when needed

If a slide references a Google Drive image file with `drive_file_id`, run with:

```bash
python3 skills/google-slides-safe/scripts/slides_cli.py create-from-spec \
  --auth-mode service-account \
  --credentials /path/to/service-account.json \
  --spec my-deck.json \
  --publish-drive-images
```

## JSON spec format

Top-level fields:
- `title` — deck title
- `slides` — array of slides

Per-slide fields:
- `layout` — one of `cover`, `problem`, `solution`, `market`, `traction`, `team`, or `default`
- `title` — slide heading
- `body` — plain body text
- `bullets` — array of bullet items
- `image_url` — optional image URL
- `drive_file_id` — optional Drive image file id
- `image2_url` — optional second image URL for supported layouts
- `drive_file_id_2` — optional second Drive image file id for supported layouts

See `references/pitch_deck_spec.example.json` for a working example.

## Resources

### scripts/
- `slides_cli.py` — safe CLI for auth checking, deck creation, Drive image support, and PDF export.

### references/
- `pitch_deck_spec.example.json` — starter deck spec example.
- `auth-notes.md` — auth mode guidance and safety notes.

## Limitations

- Current v2 creates clean pitch-deck style layouts; it is not a full visual design engine.
- Drive-image support depends on image files being reachable by Slides after URL resolution.
- `--publish-drive-images` changes sharing for referenced images; use it intentionally.

## Best use

Use this skill first for:
- pitch deck generation
- simple programmatic deck creation
- safer Google Slides automation

If a task needs heavy visual polish, use this skill to generate the draft deck first, then refine manually in Slides.
