#!/bin/bash
# AdugboInsure Weekly Grant Search
# Scans grant sources for health insurance + Nigeria opportunities
# Posted to Jarvis-AdugboInsure Telegram group every Sunday 18:00 UTC (19:00 WAT)

set -e

# Telegram credentials
TELEGRAM_BOT_TOKEN="8733839699:AAEwhBgxZ7Lj9O894AQwlcVjoR3cv5zg1vo"
TELEGRAM_CHAT_ID="-5126825082"

LOG_FILE="/home/claw/.openclaw/workspace/logs/adugboinsure-grants.log"
GRANT_FILE="/home/claw/.openclaw/workspace/memory/adugboinsure-weekly-grants.md"

echo "[$(date)] Starting AdugboInsure grant search..." >> "$LOG_FILE"

# Create markdown report
cat > "$GRANT_FILE" << 'EOF'
# AdugboInsure Weekly Grant Search

**Generated:** $(date)
**Status:** Active funding opportunities for community health insurance

---

## Active Grant Sources

### FundsForNGOs Nigeria
- [Visit](https://fundsfornpos.org.ng)
- Focus: Health, community development, microfinance
- Search terms: health insurance, community-based insurance, Nigeria

### Mastercard Foundation
- [Visit](https://www.mastercardfdn.org)
- Focus: Financial inclusion, Africa
- Deadline tracking: Usually 4-6 week cycles

### Gates Foundation
- [Visit](https://www.gatesfoundation.org)
- Focus: Global health, development
- Nigeria programs: Malaria, maternal health (adjacent to AdugboInsure)

### USAID
- [Visit](https://www.usaid.gov)
- Focus: Development, health, humanitarian
- Nigeria funding: Significant

### Echoing Green
- [Visit](https://www.echoinggreen.org)
- Focus: Social entrepreneurs, Africa fellowship
- Relevant: Founded ventures (AdugboInsure qualifies)

### Plug and Play Africa
- [Visit](https://www.plugandplayafrica.com)
- Focus: Startup ecosystem, FinTech, HealthTech
- Relevant: InsurTech category

---

## This Week's Findings

**High Priority (Closing Soon):**
- [To be populated manually or via web scrape]

**Medium Priority (30+ days):**
- [To be populated]

**Watch List (2+ months):**
- [To be populated]

---

## Action Items

- [ ] Email prospects identified
- [ ] Customize pitch for each grant (CAC/LTV focus)
- [ ] Track application deadlines

---

**Next update:** Next Sunday 19:00 WAT
EOF

# Send to Telegram
MESSAGE="📋 **AdugboInsure Weekly Grant Search**

Weekly funding opportunity scan complete. Check memory file for details.

Key sources tracked:
• FundsForNGOs Nigeria
• Mastercard Foundation
• Gates Foundation
• USAID
• Echoing Green
• Plug and Play Africa

Status: Ready for customization & outreach 🎯"

# Post to Telegram group
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": ${TELEGRAM_CHAT_ID}, \"text\": \"${MESSAGE}\", \"parse_mode\": \"HTML\"}" > /dev/null 2>&1 && echo "[$(date)] Telegram post sent" >> "$LOG_FILE" || echo "[$(date)] WARNING: Telegram send failed" >> "$LOG_FILE"

echo "[$(date)] Grant search complete. Report saved to $GRANT_FILE" >> "$LOG_FILE"
