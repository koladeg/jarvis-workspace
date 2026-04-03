#!/usr/bin/env bash
set -euo pipefail

INPUT_VIDEO="${1:-}"
OUTPUT_VIDEO="${2:-}"
LOGO_PATH="${3:-/home/claw/.openclaw/workspace/assets/adugboinsure_logo.jpg}"
INTRO_TEXT_1="${INTRO_TEXT_1:-AdugboInsure}"
INTRO_TEXT_2="${INTRO_TEXT_2:-Practical health support for everyday families}"
OUTRO_TEXT_1="${OUTRO_TEXT_1:-AdugboInsure}"
OUTRO_TEXT_2="${OUTRO_TEXT_2:-Ready for YouTube upload}"
DURATION=4
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

if [[ -z "$INPUT_VIDEO" || -z "$OUTPUT_VIDEO" ]]; then
  echo "Usage: $0 <input_video> <output_video> [logo_path]"
  exit 1
fi

if [[ ! -f "$INPUT_VIDEO" ]]; then
  echo "Input video not found: $INPUT_VIDEO"
  exit 1
fi

if [[ ! -f "$LOGO_PATH" ]]; then
  echo "Logo not found: $LOGO_PATH"
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_VIDEO")"

WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$INPUT_VIDEO")
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$INPUT_VIDEO")
FPS_RAW=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$INPUT_VIDEO")
if [[ "$FPS_RAW" == *"/"* ]]; then
  FPS=$(python3 - <<'PY' "$FPS_RAW"
from fractions import Fraction
import sys
print(float(Fraction(sys.argv[1])))
PY
)
else
  FPS="$FPS_RAW"
fi

if [[ -z "$FPS" || "$FPS" == "0" || "$FPS" == "0.0" ]]; then
  FPS=30
fi

if ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$INPUT_VIDEO" | grep -q audio; then
  ffmpeg -y -i "$INPUT_VIDEO" -vf "fps=${FPS},format=yuv420p" -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 128k "$TEMP_DIR/main.mp4" >/dev/null 2>&1
else
  DURATION_MAIN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT_VIDEO")
  ffmpeg -y -i "$INPUT_VIDEO" -f lavfi -i "anullsrc=r=48000:cl=stereo:d=${DURATION_MAIN}" -shortest -vf "fps=${FPS},format=yuv420p" -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 128k "$TEMP_DIR/main.mp4" >/dev/null 2>&1
fi

LOGO_W=$(( WIDTH * 30 / 100 ))
if (( LOGO_W < 180 )); then LOGO_W=180; fi

make_card() {
  local out="$1"
  local line1="$2"
  local line2="$3"
  ffmpeg -y \
    -f lavfi -i "color=c=#FFD54F:s=${WIDTH}x${HEIGHT}:d=${DURATION}:r=${FPS}" \
    -i "$LOGO_PATH" \
    -f lavfi -i "anullsrc=r=48000:cl=stereo:d=${DURATION}" \
    -filter_complex "[1:v]scale=${LOGO_W}:-1[logo];[0:v][logo]overlay=(W-w)/2:110[tmp];[tmp]drawtext=text='${line1}':fontcolor=white:fontsize=${HEIGHT}/13:x=(w-text_w)/2:y=h*0.60:shadowcolor=black@0.35:shadowx=2:shadowy=2[tmp2];[tmp2]drawtext=text='${line2}':fontcolor=white:fontsize=${HEIGHT}/24:x=(w-text_w)/2:y=h*0.72:shadowcolor=black@0.35:shadowx=2:shadowy=2[v]" \
    -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 128k "$out" >/dev/null 2>&1
}

make_card "$TEMP_DIR/intro.mp4" "$INTRO_TEXT_1" "$INTRO_TEXT_2"
make_card "$TEMP_DIR/outro.mp4" "$OUTRO_TEXT_1" "$OUTRO_TEXT_2"

cat > "$TEMP_DIR/concat.txt" <<EOF
file '$TEMP_DIR/intro.mp4'
file '$TEMP_DIR/main.mp4'
file '$TEMP_DIR/outro.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i "$TEMP_DIR/concat.txt" -c copy "$OUTPUT_VIDEO" >/dev/null 2>&1

echo "$OUTPUT_VIDEO"
