#!/bin/bash
# Weekly Job Search - Remote React/React Native Developer Opportunities
# Runs every Monday at 8:00 AM Lagos time (7:00 AM UTC)

set -e

WORKSPACE="/home/claw/.openclaw/workspace"
BROWSER="agent-browser"
TELEGRAM_GROUP="Jarvis-Job-Search"

echo "🔍 Starting weekly job search scan..."
echo "Time: $(date -u +'%Y-%m-%d %H:%M UTC')"

# Job board URLs to scan
LINKEDIN_URL="https://www.linkedin.com/jobs/search/?keywords=react%20developer&location=Remote&geoId=92000000&f_TP=1,2"
WE_WORK_REMOTELY="https://weworkremotely.com/remote-jobs/search?term=react"
REMOTEOK_URL="https://remoteok.com/remote-jobs?q=react+developer"

# Open browsers in background (non-blocking)
$BROWSER open "$LINKEDIN_URL" 2>&1 &
sleep 2
$BROWSER open "$WE_WORK_REMOTELY" 2>&1 &
sleep 2
$BROWSER open "$REMOTEOK_URL" 2>&1 &

echo "✓ Job board URLs loaded"
echo "📋 Next: Manual filtering and CV customization"
echo "📤 Results will be posted to $TELEGRAM_GROUP"

# TODO: Implement automated scraping + Telegram posting
# For now, this is a placeholder that opens the boards for manual review
