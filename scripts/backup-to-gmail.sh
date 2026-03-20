#!/bin/bash
# backup-to-gmail.sh - Archive memory files to Gmail
# Compresses old memory files and sends via IMAP

set -e

WORKSPACE="/home/claw/.openclaw/workspace"
BACKUP_LABEL="[Backups] Memory Archive"
GMAIL_ACCOUNT="jarviskolademail@gmail.com"

echo "📧 Backup to Gmail"
echo "=================="

# Find all memory files older than 30 days
CUTOFF_DATE=$(date -d "30 days ago" +%s)
ARCHIVE_DIR="/tmp/memory-archive-$(date +%Y%m%d)"
mkdir -p "$ARCHIVE_DIR"

echo "🔍 Finding memory files older than 30 days..."
count=0
for file in "$WORKSPACE"/memory/*.md; do
    if [ -f "$file" ]; then
        modified=$(stat -f%m "$file" 2>/dev/null || stat -c%Y "$file" 2>/dev/null)
        if [ "$modified" -lt "$CUTOFF_DATE" ]; then
            cp "$file" "$ARCHIVE_DIR/"
            echo "  - $(basename "$file")"
            ((count++))
        fi
    fi
done

if [ $count -eq 0 ]; then
    echo "✅ No files older than 30 days. Nothing to back up."
    exit 0
fi

echo "📦 Compressing..."
TAR_FILE="$ARCHIVE_DIR/memory-backup-$(date +%Y-%m).tar.gz"
tar -czf "$TAR_FILE" -C "$ARCHIVE_DIR" --exclude='*.tar.gz' .

echo "✅ Created: $(basename "$TAR_FILE")"
echo "   Size: $(du -h "$TAR_FILE" | cut -f1)"

echo ""
echo "📝 Next steps:"
echo "  1. Download the backup file from: $TAR_FILE"
echo "  2. Email it to: $GMAIL_ACCOUNT"
echo "  3. Tag with: $BACKUP_LABEL"
echo ""
echo "⚠️  TODO: Automate Gmail IMAP sending"
