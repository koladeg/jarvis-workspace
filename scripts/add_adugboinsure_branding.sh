#!/bin/bash
# Add AdugboInsure branding (intro + outro) to NotebookLM video
# Usage: bash add_adugboinsure_branding.sh <input_video> <output_video> [logo_image]

set -e

INPUT_VIDEO="$1"
OUTPUT_VIDEO="$2"
LOGO_IMAGE="${3:-$(dirname "$0")/../assets/adugboinsure_logo.jpg}"
DURATION=4
TEMP_DIR=$(mktemp -d)

echo "🎬 Adding AdugboInsure branding..."

# Check inputs
if [ ! -f "$INPUT_VIDEO" ]; then
    echo "❌ Input video not found: $INPUT_VIDEO"
    exit 1
fi

if [ ! -f "$LOGO_IMAGE" ]; then
    echo "❌ Logo image not found: $LOGO_IMAGE"
    exit 1
fi

# Get video dimensions
WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1:noinput=1 "$INPUT_VIDEO")
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1:noinput=1 "$INPUT_VIDEO")
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1:noinput=1 "$INPUT_VIDEO")

echo "📹 Video specs: ${WIDTH}x${HEIGHT} @ $FPS fps"

# Create intro frame (yellow background with logo, 4 seconds)
echo "🟨 Creating intro frame..."
ffmpeg -f lavfi -i color=c=FFD700:s=${WIDTH}x${HEIGHT}:d=$DURATION -f lavfi -i anullsrc=r=44100:cl=stereo:d=$DURATION \
    -pix_fmt yuv420p -r "$FPS" -y "$TEMP_DIR/intro.mp4" 2>/dev/null

# Add logo to intro (centered)
echo "🏷️  Overlaying logo on intro..."
LOGO_SCALE="min(${WIDTH},${HEIGHT})*0.4"
ffmpeg -i "$TEMP_DIR/intro.mp4" -i "$LOGO_IMAGE" \
    -filter_complex "[1:v]scale=$LOGO_SCALE:-1[logo];[0:v][logo]overlay=(W-w)/2:(H-h)/2:enable='between(t,0,$DURATION)'[v]" \
    -map "[v]" -map 0:a -c:a aac -y "$TEMP_DIR/intro_branded.mp4" 2>/dev/null

# Create outro frame (same as intro)
echo "🟨 Creating outro frame..."
ffmpeg -f lavfi -i color=c=FFD700:s=${WIDTH}x${HEIGHT}:d=$DURATION -f lavfi -i anullsrc=r=44100:cl=stereo:d=$DURATION \
    -pix_fmt yuv420p -r "$FPS" -y "$TEMP_DIR/outro.mp4" 2>/dev/null

# Add logo to outro
echo "🏷️  Overlaying logo on outro..."
ffmpeg -i "$TEMP_DIR/outro.mp4" -i "$LOGO_IMAGE" \
    -filter_complex "[1:v]scale=$LOGO_SCALE:-1[logo];[0:v][logo]overlay=(W-w)/2:(H-h)/2:enable='between(t,0,$DURATION)'[v]" \
    -map "[v]" -map 0:a -c:a aac -y "$TEMP_DIR/outro_branded.mp4" 2>/dev/null

# Create concat file
cat > "$TEMP_DIR/concat.txt" << EOF
file '$TEMP_DIR/intro_branded.mp4'
file '$INPUT_VIDEO'
file '$TEMP_DIR/outro_branded.mp4'
EOF

# Concatenate all parts
echo "🎞️  Concatenating video parts..."
ffmpeg -f concat -safe 0 -i "$TEMP_DIR/concat.txt" -c copy -y "$OUTPUT_VIDEO" 2>/dev/null

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ Branded video created: $OUTPUT_VIDEO"
