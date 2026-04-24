# AdugboInsure Project Memory

**Last Updated:** 2026-04-20 11:48 UTC  
**Status:** Plug and Play submission completed; pitch deck + registration-flow variant generated and exported

---

## Setup Complete (2026-03-21)

### Files Created
1. **`adugboinsure_agents_master.md`** — Master agent list (5 Apete + 8 Abe Emu)
2. **`adugboinsure_oyshia_tasks.md`** — OYSHIA tasks (48 items, prioritized)
3. **`adugboinsure_application_template.md`** — Grant pitch boilerplate
4. **`adugboinsure_dashboard_template.md`** — Weekly dashboard template (manual fill, 5 min)

### Credentials Saved
- ✅ **Notion API key:** `/home/claw/.openclaw/workspace/.credentials/notion_api_key.txt`
  - Token: `ntn_x1517655162aymT1uxlUcAUVg9PzeEORi8fEkxRyUKDeSY`
  - Synced pages:
    - AdugboInsure agents: https://www.notion.so/AdugboInsure-agents-23505a75947a80318298fb6d09906d9b
    - OYSHIA tasks: https://www.notion.so/OYSHIA-AdugboInsure-Tasks-19d05a75947a80da87f0c45d5ebe4787
- ✅ **Zapier MCP token:** Already stored (62 tools available)

### Automation Schedule
- **Weekly Funding Radar:** Sunday 19:00 WAT
  - Sources: FundsForNGOs Nigeria, Mastercard Foundation, Gates, USAID, Echoing Green, Plug and Play Africa
  - Post to: `Jarvis-AdugboInsure` Telegram group
  
- **Weekly Agent Dashboard:** Sunday 19:00 WAT (same post)
  - Metrics: Agent engagement, status, action items
  - Template file: `adugboinsure_dashboard_template.md`
  - Manual fill required (5 min)

---

## Current Status

**Agents:**
- Apete: 5 active agents (engaged)
- Abe Emu: 8 recruited agents (activating mid-April 2026)
- Total enrollments: 0 (awareness/education phase)

**Partnership:**
- ✅ MOU from OYSHIA (locked)
- ✅ POS agent freelancers (individual network, 13 total)

**Funding:**
- Target: $5,000 USD (near-term expansion)
- Timeline: 3 months (Mar-May 2026)
- Model: Community-based health insurance via POS agents

---

## Next Tasks

**By Sunday Mar 23 (Funding Radar Launch):**
- [ ] Clarify MOU status with OYSHIA (signed? drafted?)
- [ ] Confirm ₦13,500 cost + quarterly payment split discussion with OYSHIA

**By Mid-April (Abe Emu Activation):**
- [ ] Complete agent forms (Apete + Abe Emu)
- [ ] Collect onboarding feedback (customer perception, e-form issues, registration barriers)
- [ ] Send training confirmation to Abe Emu (6 weeks notice)
- [ ] Verify churn follow-up willingness (Yusuf Raman: marked NOT ok)

**Still to Build:**
- ⏳ 3-year financial model (revenue projections, CAC/LTV)
- ⏳ Content automation (NotebookLM script generation for agents)
- ⏳ Enrollment tracking (when pilot data available)

---

## April 2026 Submission Record

### Plug and Play / Pitch Deck Flow (Completed 2026-04-20)
- ✅ Google Slides access verified with OAuth account `jarviskolademail@gmail.com`
- ✅ Main deck created: `AdugboInsure Pitch Deck`
  - Slides: https://docs.google.com/presentation/d/17LTGi4Vwd1yW6TnHdLG1tiwuWaTNG_0JB66dIp9EgTI/edit
  - PDF: `outputs/adugboinsure_pitch_deck_final.pdf`
  - Spec: `outputs/adugboinsure_pitch_deck_final.json`
- ✅ Registration-flow update deck created after Kolade shared the flow image
  - Slides: https://docs.google.com/presentation/d/12DMEET465RPQWPAu1kZhMZvqaCgOYia5qT8Apk7Prvs/edit
  - PDF: `outputs/adugboinsure_pitch_deck_with_registration_flow.pdf`
  - Spec: `outputs/adugboinsure_pitch_deck_with_registration_flow.json`
- ✅ Registration flow added as a dedicated slide with cleaner presentation wording
- ✅ Kolade confirmed the submission was finished successfully

### Reuse Notes
- Use the registration-flow deck variant as the better starting point for future investor/application deck edits
- If a future deck is needed, current Google Slides auth is working through the `google-slides-safe` workflow
- The registration flow message is simple and strong:
  1. enroll with agent
  2. make first payment
  3. get covered
  4. continue payments anywhere

## Important Notes

- **Content creation:** Weekly POS agent education scripts → available from NotebookLM notebook + existing YouTube videos
- **Agent engagement:** Weak on Apete (only 3-5 respond), need activation work on Abe Emu
- **OYSHIA relationship:** Strong (MOU exists), critical for scaling
- **Payment processing:** Paystack + Moniepoint integrated, flexible quarterly payment ₦3,375/quarter available

---

*Read this file when discussing AdugboInsure. All automation details, credentials, and schedules stored here.*
