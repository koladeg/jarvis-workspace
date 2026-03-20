#!/usr/bin/env bash
# Auto-transcribe voice messages from OpenClaw media directory
# Usage: ./auto-transcribe.sh [watch|once]
# - watch: monitor for new files continuously
# - once: transcribe existing .ogg files once and exit (default)

set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

MEDIA_DIR="/home/claw/.openclaw/media/inbound"
TRANSCRIPT_DIR="/home/claw/.openclaw/workspace/transcripts"
MODEL="small"
LANGUAGE="en"

# Create transcript dir
mkdir -p "$TRANSCRIPT_DIR"

transcribe_file() {
  local audio_file="$1"
  local basename=$(basename "$audio_file")
  local transcript_file="$TRANSCRIPT_DIR/${basename%.*}.txt"
  
  # Skip if already transcribed
  if [[ -f "$transcript_file" ]]; then
    echo "[SKIP] Already transcribed: $basename"
    return 0
  fi
  
  echo "[TRANSCRIBE] Processing: $basename"
  
  # Run whisper with small model
  whisper "$audio_file" \
    --model "$MODEL" \
    --language "$LANGUAGE" \
    --output_format txt \
    --output_dir "$TRANSCRIPT_DIR" \
    >/dev/null 2>&1 && echo "[OK] $basename → ${basename%.*}.txt" || echo "[ERROR] Failed: $basename"
}

case "${1:-once}" in
  watch)
    echo "Watching $MEDIA_DIR for voice messages..."
    while true; do
      find "$MEDIA_DIR" -name "*.ogg" -o -name "*.m4a" -o -name "*.mp3" | while read audio_file; do
        transcribe_file "$audio_file"
      done
      sleep 5
    done
    ;;
  once|*)
    echo "Transcribing existing voice files (one-time)..."
    find "$MEDIA_DIR" -name "*.ogg" -o -name "*.m4a" -o -name "*.mp3" 2>/dev/null | while read audio_file; do
      [[ -n "$audio_file" ]] && transcribe_file "$audio_file"
    done
    echo "Done. Transcripts saved to: $TRANSCRIPT_DIR"
    ;;
esac
