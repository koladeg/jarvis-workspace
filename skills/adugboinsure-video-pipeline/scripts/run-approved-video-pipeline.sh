#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash skills/adugboinsure-video-pipeline/scripts/run-approved-video-pipeline.sh \
#     <input_video> <overlay_image> <title> [description]

INPUT_VIDEO="${1:-}"
OVERLAY_IMAGE="${2:-}"
TITLE="${3:-}"
DESCRIPTION="${4:-Learn how POS agents can help communities understand and access health insurance through AdugboInsure.}"

if [[ -z "$INPUT_VIDEO" || -z "$OVERLAY_IMAGE" || -z "$TITLE" ]]; then
  echo "Usage: bash skills/adugboinsure-video-pipeline/scripts/run-approved-video-pipeline.sh <input_video> <overlay_image> <title> [description]" >&2
  exit 1
fi

if [[ ! -f "$INPUT_VIDEO" ]]; then
  echo "❌ Missing input video: $INPUT_VIDEO" >&2
  exit 1
fi

if [[ ! -f "$OVERLAY_IMAGE" ]]; then
  echo "❌ Missing overlay image: $OVERLAY_IMAGE" >&2
  exit 1
fi

WORKSPACE="/home/claw/.openclaw/workspace"
BASENAME="$(basename "$INPUT_VIDEO")"
STEM="${BASENAME%.*}"
OUT_DIR="$WORKSPACE/outputs/videos/branded"
PREVIEW_DIR="$WORKSPACE/outputs/previews"
FINAL_VIDEO="$OUT_DIR/${STEM}__approved.mp4"
PREVIEW_2S="$PREVIEW_DIR/${STEM}__approved_at_2s.png"
PREVIEW_END="$PREVIEW_DIR/${STEM}__approved_2s_before_end.png"

mkdir -p "$OUT_DIR" "$PREVIEW_DIR"

DURATION="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$INPUT_VIDEO")"
END_START="$(python3 - <<'PY' "$DURATION"
import sys
print(max(0, float(sys.argv[1]) - 5))
PY
)"
END_PREVIEW="$(python3 - <<'PY' "$DURATION"
import sys
print(max(0, float(sys.argv[1]) - 2))
PY
)"

ffmpeg -y -i "$INPUT_VIDEO" -loop 1 -i "$OVERLAY_IMAGE" \
  -filter_complex "[1:v]scale=1280:-2[ov];[0:v][ov]overlay=(W-w)/2:(H-h)/2:enable='between(t,0,3)+between(t,${END_START},${DURATION})',format=yuv420p[v]" \
  -map '[v]' -map 0:a? -t "$DURATION" -shortest \
  -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k \
  "$FINAL_VIDEO"

RAW_DUR="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$INPUT_VIDEO")"
FINAL_DUR="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$FINAL_VIDEO")"

python3 - <<'PY' "$RAW_DUR" "$FINAL_DUR"
import sys
raw = float(sys.argv[1])
final = float(sys.argv[2])
if abs(raw - final) > 1.0:
    raise SystemExit(f"❌ Duration mismatch: raw={raw:.3f}s final={final:.3f}s")
print(f"✓ Duration verified: raw={raw:.3f}s final={final:.3f}s")
PY

ffmpeg -y -ss 2 -i "$FINAL_VIDEO" -frames:v 1 "$PREVIEW_2S" >/dev/null 2>&1
ffmpeg -y -ss "$END_PREVIEW" -i "$FINAL_VIDEO" -frames:v 1 "$PREVIEW_END" >/dev/null 2>&1

UPLOAD_LOG="$(mktemp)"
python3 "$WORKSPACE/scripts/youtube_upload.py" "$FINAL_VIDEO" "$TITLE" "$DESCRIPTION" | tee "$UPLOAD_LOG"

UPLOAD_JSON="$(python3 - <<'PY' "$UPLOAD_LOG"
import sys, json
from pathlib import Path
text = Path(sys.argv[1]).read_text()
start = text.rfind('{')
if start == -1:
    raise SystemExit('❌ Upload did not return JSON')
obj = json.loads(text[start:])
print(json.dumps(obj))
PY
)"

rm -f "$UPLOAD_LOG"

printf 'FINAL_VIDEO=%s\nPREVIEW_2S=%s\nPREVIEW_END=%s\nUPLOAD=%s\n' "$FINAL_VIDEO" "$PREVIEW_2S" "$PREVIEW_END" "$UPLOAD_JSON"
