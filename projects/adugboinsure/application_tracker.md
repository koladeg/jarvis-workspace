# AdugboInsure Application Tracker

Use this file to track every funding, accelerator, partnership, or opportunity application from submission to final outcome.

---

## Status Legend

- `NEW` — link received, not yet reviewed
- `DRAFTING` — answers being prepared
- `SUBMITTED` — form/application submitted
- `CONFIRMED` — receipt acknowledged by platform/email
- `UNDER_REVIEW` — actively being reviewed
- `FOLLOW_UP_DUE` — follow-up date reached
- `FOLLOWED_UP` — follow-up sent
- `NEXT_STAGE` — interview/call/docs requested
- `ACCEPTED` — accepted into program
- `REJECTED` — declined
- `DORMANT` — no response after reasonable follow-up

---

## Master Table

| Opportunity | Type | Link | Date Submitted | Status | Confirmation Evidence | Next Follow-Up | Owner | Notes |
|---|---|---|---|---|---|---|---|---|
| Acumen – Grow your business | Investor intake / lead form | https://acumen.org/entrepreneurs/ | 2026-04-07 | FOLLOW_UP_DUE | Success state on page: "Thanks for joining!" | 2026-04-14 | Jarvis | Submitted with supported facts only; legal entity country left blank because not verified |
| UNICEF Venture Fund – Climate and Health 2026 | Venture fund / health innovation | https://www.unicef.org/innovation/call-for-application-climate-and-health-2026 | 2026-05-08 | FOLLOW_UP_DUE | Submitted per Kolade confirmation | 2026-05-15 | Jarvis | Submitted already; move to follow-up bucket and confirm any receipt / next-step email |
| Visa Africa FinTech Accelerator Program 6 | Accelerator / fintech | https://vc4a.com/visa/visa-africa-fintech-accelerator-program-6/ | 2026-05-08 | FOLLOW_UP_DUE | Submitted per Kolade confirmation | 2026-05-15 | Jarvis | Submitted already; move to follow-up bucket and confirm any receipt / platform status |
| Startup Innovation Challenge 2026 (Nigeria) | Challenge / equity-free support | https://fundsforcompanies.fundsforngos.org/awards-and-prizes/submissions-open-for-startup-innovation-challenge-2026-nigeria/ | — | NEW | — | — | Jarvis | High-priority fresh application; Nigeria-relevant, HealthTech included |
| DayOne Accelerator Program for Healthtech Startups | Accelerator / healthtech | https://fundsforcompanies.fundsforngos.org/training-and-mentorship/dayone-accelerator-program-for-healthtech-startups/ | — | NEW | — | — | Jarvis | Medium priority; requires fresh validation before drafting/submission |
| World Bank JJ/WBGSP Window #2 | Scholarship / school funding | https://www.worldbank.org/en/programs/scholarships/jj-wbgsp | — | DORMANT | — | — | Jarvis | Separate school-funding lane; only actionable after unconditional admission to a participating programme |
| Village Capital Future of Aging 2026 | Accelerator | https://vilcap.com/programs/the-future-of-aging-2026 | — | REJECTED | — | — | Jarvis | Low-fit / US-only from prior pass |
| ACT Foundation 2026 Grant Application | Grant | https://actrustfoundation.org/grant_application | — | DORMANT | — | — | Jarvis | Conflicting date signals; do not treat as live unless directly revalidated |

---

## Per-Application Detail Template

Copy this block for each new application.

```md
### [Opportunity Name]
- **Type:** grant / accelerator / investor / partner / fellowship
- **Link:**
- **Date received:**
- **Date submitted:**
- **Status:** NEW
- **Priority:** high / medium / low
- **Program fit:**
- **What we submitted:**
- **Unverified facts intentionally omitted:**
- **Confirmation evidence:**
- **Expected response window:**
- **Next follow-up date:**
- **Follow-up owner:** Jarvis / Kolade
- **Portal/account needed later?:** yes / no
- **Extra docs requested?:**
- **Outcome:** pending
- **Notes:**

#### Follow-up draft
Hi, I’m following up on AdugboInsure’s submission to [Program Name] on [date]. We’re building a community-based health insurance platform improving access to affordable coverage for underserved communities in Nigeria through local agent distribution and simple digital enrollment. Please let us know if any additional information or materials would be helpful from our side.
```

---

## Follow-Up Rules

### Default timing
- If there is **no confirmation**: check within **3–5 business days**
- If there is a **confirmation but no next step**: follow up in **7–10 business days**
- If they gave a stated review window: follow up **after that window passes**
- If they request documents: send as soon as available

### Escalation cadence
1. Submit
2. Confirm receipt
3. Follow up once at 7–10 business days
4. Follow up again at 14–21 business days if still silent
5. Mark `DORMANT` if no movement after that unless strategically important

### Success measures
A submission only counts as meaningful progress if it reaches one of these:
- `CONFIRMED`
- `UNDER_REVIEW`
- `NEXT_STAGE`
- `ACCEPTED`

---

## Weekly Review Checklist

Run this once a week:
- Review all `SUBMITTED` and `CONFIRMED` entries
- Move any overdue item to `FOLLOW_UP_DUE`
- Draft/send follow-ups
- Record replies and next steps
- Mark dead leads as `DORMANT` or `REJECTED`

---

## Current Open Opportunities

### Follow-up list
- **Acumen – Grow your business**
  - Status: `FOLLOW_UP_DUE`
  - Next action: send follow-up
  - Why: already submitted; should be moved from passive waiting to active follow-up
- **UNICEF Venture Fund – Climate and Health 2026**
  - Status: `FOLLOW_UP_DUE`
  - Next action: confirm receipt / check for any response window or next-step email
  - Why: Kolade confirmed it has already been submitted
- **Visa Africa FinTech Accelerator Program 6**
  - Status: `FOLLOW_UP_DUE`
  - Next action: confirm receipt / check platform status or response email
  - Why: Kolade confirmed it has already been submitted

### Fresh applications to start
1. **Startup Innovation Challenge 2026 (Nigeria)**
   - Status: `NEW`
   - Priority: high
   - Why: Nigeria-relevant, HealthTech included, equity-free support
2. **DayOne Accelerator Program for Healthtech Startups**
   - Status: `NEW`
   - Priority: medium
   - Why: healthtech-specific, but must be revalidated fresh before effort

### Hold / separate lane / skip
- **World Bank JJ/WBGSP Window #2** — school-funding lane only; actionable after unconditional admission
- **Village Capital Future of Aging 2026** — reject / low fit
- **ACT Foundation 2026 Grant Application** — hold until directly revalidated

### Acumen – Grow your business
- **Type:** investor intake / lead form
- **Link:** https://acumen.org/entrepreneurs/
- **Date received:** 2026-04-07
- **Date submitted:** 2026-04-07
- **Status:** SUBMITTED
- **Priority:** medium
- **Program fit:** West Africa + healthcare + low-income community impact
- **What we submitted:** name, email, organization name, region, for-profit, healthcare sector, investment-fit summary
- **Unverified facts intentionally omitted:** legal entity country / registration-specific claim
- **Confirmation evidence:** on-page success message: "Thanks for joining! We'll keep you up-to-date on the latest Acumen news and updates."
- **Expected response window:** unknown
- **Next follow-up date:** 2026-04-14
- **Follow-up owner:** Jarvis
- **Portal/account needed later?:** no known portal yet
- **Extra docs requested?:** none yet
- **Outcome:** pending
- **Notes:** treat this as initial intake, not full diligence

#### Follow-up draft
Hi, I’m following up on AdugboInsure’s submission via Acumen’s Grow your business page on April 7, 2026. AdugboInsure is building a community-based health insurance platform to improve affordable coverage access for underserved communities in Nigeria through local agent distribution and simple digital enrollment. Please let us know if any additional information or materials would be helpful from our side.
