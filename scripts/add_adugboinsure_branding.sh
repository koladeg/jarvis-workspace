#!/bin/bash
# Add AdugboInsure branding (intro + outro) to NotebookLM video
# Usage: bash add_adugboinsure_branding.sh <input_video> <output_video> [logo_image]

set -euo pipefail

INPUT_VIDEO="${1:-}"
OUTPUT_VIDEO="${2:-}"
LOGO_IMAGE="${3:-$(dirname "$0")/../assets/adugboinsure_logo.jpg}"
DURATION=4
TEMP_DIR=$(mktemp -d)

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

echo "🎬 Adding AdugboInsure branding..."

if [ -z "$INPUT_VIDEO" ] || [ -z "$OUTPUT_VIDEO" ]; then
    echo "Usage: bash add_adugboinsure_branding.sh <input_video> <output_video> [logo_image]"
    exit 1
fi

# Check inputs
if [ ! -f "$INPUT_VIDEO" ]; then
    echo "❌ Input video not found: $INPUT_VIDEO"
    exit 1
fi

if [ ! -f "$LOGO_IMAGE" ]; then
    echo "❌ Logo image not found: $LOGO_IMAGE"
    exit 1
fi

mkdir -p "$(dirname "$OUTPUT_VIDEO")"

# Get video dimensions / fps / audio presence
WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$INPUT_VIDEO")
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$INPUT_VIDEO")
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$INPUT_VIDEO")
HAS_AUDIO=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$INPUT_VIDEO" | head -n1 || true)

if [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
    echo "❌ Could not detect input video dimensions"
    exit 1
fi

if [ -z "$FPS" ] || [ "$FPS" = "0/0" ]; then
    FPS="30"
fi

echo "📹 Video specs: ${WIDTH}x${HEIGHT} @ $FPS fps"

if [ -n "$HAS_AUDIO" ]; then
    echo "🔊 Input audio detected"
    AUDIO_INPUT="-i $INPUT_VIDEO"
    AUDIO_MAP_MAIN="[1:a]"
else
    echo "🔇 No input audio detected; creating silent track"
    AUDIO_INPUT="-f lavfi -t $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT_VIDEO") -i anullsrc=r=48000:cl=stereo"
    AUDIO_MAP_MAIN="[1:a]"
fi

# Create branded intro/outro clips
LOGO_SCALE_W=$(( WIDTH * 40 / 100 ))
if [ "$LOGO_SCALE_W" -le 0 ]; then
    LOGO_SCALE_W=400
fi

echo "🟨 Creating intro and outro clips..."
ffmpeg -y \
    -f lavfi -i "color=c=#FFD700:s=${WIDTH}x${HEIGHT}:d=${DURATION}:r=${FPS}" \
    -i "$LOGO_IMAGE" \
    -f lavfi -i "anullsrc=r=48000:cl=stereo:d=${DURATION}" \
    -filter_complex "[1:v]scale=${LOGO_SCALE_W}:-1[logo];[0:v][logo]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]" \
    -map "[v]" -map 2:a -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k \
    "$TEMP_DIR/intro.mp4" >/dev/null 2>&1

ffmpeg -y \
    -f lavfi -i "color=c=#FFD700:s=${WIDTH}x${HEIGHT}:d=${DURATION}:r=${FPS}" \
    -i "$LOGO_IMAGE" \
    -f lavfi -i "anullsrc=r=48000:cl=stereo:d=${DURATION}" \
    -filter_complex "[1:v]scale=${LOGO_SCALE_W}:-1[logo];[0:v][logo]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]" \
    -map "[v]" -map 2:a -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k \
    "$TEMP_DIR/outro.mp4" >/dev/null 2>&1

# Normalize main video for concatenation
DURATION_MAIN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT_VIDEO")

echo "🎞️ Normalizing main video and concatenating..."
if ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$INPUT_VIDEO" | grep -q audio; then
    ffmpeg -y -i "$INPUT_VIDEO" \
        -vf "scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=decrease,pad=${WIDTH}:${HEIGHT}:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fps=${FPS}" \
        -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k \
        "$TEMP_DIR/main.mp4" >/dev/null 2>&1
else
    ffmpeg -y -i "$INPUT_VIDEO" -f lavfi -i "anullsrc=r=48000:cl=stereo:d=${DURATION_MAIN}" \
        -shortest \
        -vf "scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=decrease,pad=${WIDTH}:${HEIGHT}:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fps=${FPS}" \
        -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k \
        "$TEMP_DIR/main.mp4" >/dev/null 2>&1
fi

cat > "$TEMP_DIR/concat.txt" <<EOF
file '$TEMP_DIR/intro.mp4'
file '$TEMP_DIR/main.mp4'
file '$TEMP_DIR/outro.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i "$TEMP_DIR/concat.txt" -c copy "$OUTPUT_VIDEO" >/dev/null 2>&1

echo "✓ Branded video created: $OUTPUT_VIDEO"
