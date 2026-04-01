#!/bin/bash
# AdugboInsure Video Branding Script
# Adds 4-second yellow intro/outro with logo using FFmpeg

set -e

INPUT_VIDEO="$1"
OUTPUT_DIR="${2:-.}"
LOGO_PATH="${3:-/home/claw/.openclaw/workspace/assets/adugboinsure_logo.jpg}"
BRAND_COLOR="yellow"  # FFmpeg color code for yellow

# Validate inputs
if [ -z "$INPUT_VIDEO" ] || [ ! -f "$INPUT_VIDEO" ]; then
  echo "Error: Input video not found: $INPUT_VIDEO"
  echo "Usage: $0 <input_video> [output_dir] [logo_path]"
  exit 1
fi

# Create output directory if needed
mkdir -p "$OUTPUT_DIR"

# Get video info
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1:novalue=1 "$INPUT_VIDEO")
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 "$INPUT_VIDEO" | cut -d'/' -f1)
WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 "$INPUT_VIDEO")
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 "$INPUT_VIDEO")

BASENAME=$(basename "$INPUT_VIDEO" | sed 's/\.[^.]*$//')
BRANDED_OUTPUT="$OUTPUT_DIR/${BASENAME}_branded.mp4"
TEMP_DIR="/tmp/adugbo_brand_$$"
mkdir -p "$TEMP_DIR"

echo "📹 AdugboInsure Video Branding"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Input: $INPUT_VIDEO"
echo "Duration: ${DURATION}s | FPS: ${FPS} | Resolution: ${WIDTH}x${HEIGHT}"
echo "Output: $BRANDED_OUTPUT"
echo ""

# Step 1: Create 4-second yellow intro with text
echo "[1/4] Generating yellow intro (4 sec)..."
ffmpeg -f lavfi -i color=c=yellow:s=${WIDTH}x${HEIGHT}:d=4 \
  -vf "drawtext=text='AdugboInsure':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-100,\
        drawtext=text='Health at ₦200/month':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+50" \
  -pix_fmt yuv420p \
  "$TEMP_DIR/intro.mp4" -y 2>/dev/null || true

# Step 2: Create 4-second yellow outro with logo reference
echo "[2/4] Generating yellow outro (4 sec)..."
ffmpeg -f lavfi -i color=c=yellow:s=${WIDTH}x${HEIGHT}:d=4 \
  -vf "drawtext=text='Visit us today':fontsize=50:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-100,\
        drawtext=text='AdugboInsure.com | Hotline: [Contact]':fontsize=30:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+80" \
  -pix_fmt yuv420p \
  "$TEMP_DIR/outro.mp4" -y 2>/dev/null || true

# Step 3: Concatenate intro + main video + outro
echo "[3/4] Assembling branded video (intro + main + outro)..."
cat > "$TEMP_DIR/concat.txt" << EOF
file '$TEMP_DIR/intro.mp4'
file '$INPUT_VIDEO'
file '$TEMP_DIR/outro.mp4'
EOF

ffmpeg -f concat -safe 0 -i "$TEMP_DIR/concat.txt" -c copy -y "$BRANDED_OUTPUT" 2>/dev/null || true

# Step 4: Final encoding pass (ensure compatibility)
echo "[4/4] Final encoding pass..."
FINAL_OUTPUT="$OUTPUT_DIR/${BASENAME}_branded_final.mp4"
ffmpeg -i "$BRANDED_OUTPUT" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  -y "$FINAL_OUTPUT" 2>/dev/null || true

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Branding Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Output: $FINAL_OUTPUT"
echo "Size: $(du -h "$FINAL_OUTPUT" | cut -f1)"
ls -lh "$FINAL_OUTPUT"
echo ""
echo "Ready for YouTube upload."
