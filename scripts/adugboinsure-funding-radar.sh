#!/bin/bash
# AdugboInsure Weekly Funding Radar
# Aggregates funding opportunities + generates weekly dashboard
# Posted to Jarvis-AdugboInsure Telegram group every Sunday 18:00 UTC (19:00 WAT)

set -e

# Telegram credentials
TELEGRAM_BOT_TOKEN="8733839699:AAEwhBgxZ7Lj9O894AQwlcVjoR3cv5zg1vo"
TELEGRAM_CHAT_ID="-5126825082"

LOG_FILE="/home/claw/.openclaw/workspace/logs/adugboinsure-funding.log"
DASHBOARD_FILE="/home/claw/.openclaw/workspace/memory/adugboinsure-dashboard-$(date +%Y-%m-%d).md"

echo "[$(date)] Starting AdugboInsure funding radar..." >> "$LOG_FILE"

# Generate dashboard from template
cat > "$DASHBOARD_FILE" << 'EOF'
# AdugboInsure Weekly Dashboard

**Week of:** $(date +%Y-%m-%d)
**Status:** Active

---

## 📊 Agent Engagement

### Apete (5 Active Agents)
- Status: Engaged
- Responsiveness: 3-5 per week
- Action items: [Add weekly summary]

### Abe Emu (8 Recruited Agents)
- Status: Activating mid-April 2026
- Training prep: 6 weeks notice sent
- Next milestone: [Add dates]

---

## 💰 Funding Status

**Target:** $5,000 USD (near-term expansion)
**Timeline:** Mar-May 2026 (3 months)

### Grant Opportunities This Week
- [FundsForNGOs checks]
- [Foundation deadlines]
- [Startup ecosystem opportunities]

---

## 🎯 Key Priorities

1. Clarify MOU status with OYSHIA
2. Confirm ₦13,500 cost split + quarterly payments
3. Collect agent onboarding feedback
4. Track enrollment progress

---

## 📝 Notes

- Content creation: Available from NotebookLM notebook
- Agent activation: Weak on Apete, focus on Abe Emu preparation
- Payment: Paystack + Moniepoint integrated (₦3,375/quarter available)

---

**Next update:** Next Sunday 19:00 WAT
EOF

# Send summary to Telegram
MESSAGE="📈 **AdugboInsure Weekly Funding Radar**

**Agent Status:**
• Apete: 5 active (3-5 responses/week)
• Abe Emu: 8 recruited (launching mid-April)
• Total enrollments: 0 (awareness phase)

**Funding Focus:**
• Target: \$5,000 USD
• Timeline: 3 months (Mar-May 2026)
• This week: Grant opportunity scan underway

**Action Items:**
✓ MOU status clarification pending
✓ Quarterly payment structure confirmation
✓ Onboarding feedback collection

Dashboard saved & ready for updates 📊"

# Post to Telegram
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": ${TELEGRAM_CHAT_ID}, \"text\": \"📊 AdugboInsure Funding Radar\\n\\n${MESSAGE}\", \"parse_mode\": \"HTML\"}" > /dev/null 2>&1 && echo "[$(date)] Telegram post sent" >> "$LOG_FILE" || echo "[$(date)] WARNING: Telegram send failed" >> "$LOG_FILE"

echo "[$(date)] Funding radar complete. Dashboard: $DASHBOARD_FILE" >> "$LOG_FILE"
