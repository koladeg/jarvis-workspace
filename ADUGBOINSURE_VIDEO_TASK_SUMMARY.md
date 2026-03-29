# AdugboInsure Video Script + Generation Task
**Status:** ✅ PARTIALLY COMPLETE | Scripts ready, awaiting notebook path  
**Date:** Wednesday, March 25, 2026 — 8:00 AM UTC  
**Task ID:** cron:4f025d58-d876-4301-b30e-daa3deec72fc

---

## ✅ Completed Tasks

### 1. **Video Script Generation** (DONE)
- **Location:** `/home/claw/.openclaw/workspace/videos/adugboinsure_scripts.md`
- **Format:** 5-week rotating topics × 10-minute scripts
- **Language Level:** Secondary school (accessible, warm, conversational)
- **Style:** NotebookLM-inspired (stories first, concrete examples, Pidgin English phrases)

**Topics (Week-by-week rotation):**
1. **Week 1: Benefits** — Why insurance matters, financial protection, peace of mind
2. **Week 2: Enrollment** — How to sign up (bring ID, pay ₦200, get card, done)
3. **Week 3: Coverage** — What's covered, payment amounts, partner hospitals
4. **Week 4: Claims** — How the process works, hospital submissions, your share vs. ours
5. **Week 5: Testimonials** — Real voices: market woman, okada rider, pregnant woman, father, elderly woman

**Each script includes:**
- ✅ Opening hook (story or relatable scenario)
- ✅ Main teaching segments with concrete examples
- ✅ Cost breakdowns (real naira amounts)
- ✅ Visual cues (animations, icons, illustrations)
- ✅ Call-to-action to next week's topic
- ✅ Brand tagline + contact info

**Production notes:** NotebookLM-style visuals (stick figures, simple animations, soft colors, direct camera address).

---

### 2. **Telegram Posting** (PENDING)
- **Target:** Jarvis-AdugboInsure Telegram group
- **Status:** ⚠️ Needs valid chat ID (attempted delivery failed)
- **Content:** Summary of scripts ready + next steps
- **Action needed:** Provide correct Telegram chat ID or group name

---

## ⏳ Awaiting: Video Generation from Notebook

### 3. **NotebookLM CLI Video Generation** (BLOCKED)
- **CLI Available:** ✅ `/home/claw/.local/bin/nlm`
- **Required Input:** Notebook path for "Implementing Community-Based Health Insurance Schemes"
- **Status:** Notebook path not provided
- **Action needed:** Provide full path to the NotebookLM notebook file

**Expected command (once path is known):**
```bash
nlm generate-video --notebook "<NOTEBOOK_PATH>" \
  --topic "week_1_benefits" \
  --script "/home/claw/.openclaw/workspace/videos/adugboinsure_scripts.md" \
  --output "/home/claw/.openclaw/workspace/outputs/videos/adugboinsure_week_1_raw.mp4"
```

---

## ✅ Completed: FFmpeg Branding Script

### 4. **Branding Automation** (DONE)
- **Script:** `/home/claw/.openclaw/workspace/scripts/brand_adugbo_video.sh`
- **Function:** Adds 4-second yellow intro + 4-second yellow outro to video
- **Intro content:** "AdugboInsure" + "Health at ₦200/month"
- **Outro content:** "Visit us today" + contact info
- **Usage:**
```bash
./scripts/brand_adugbo_video.sh <input_video> [output_dir] [logo_path]
```

**Example:**
```bash
./scripts/brand_adugbo_video.sh outputs/videos/adugboinsure_week_1_raw.mp4 outputs/videos
```

**Output:** `outputs/videos/adugboinsure_week_1_branded_final.mp4`

**What it does:**
1. Creates yellow color-fill intro (4 sec) with text overlay
2. Creates yellow color-fill outro (4 sec) with CTA + contact info
3. Concatenates: intro + original video + outro
4. Final encodes to H.264 MP4 for YouTube compatibility

---

## 📋 Full Workflow (Step-by-step)

### Phase 1: Scripts ✅
- [x] Generate 5 rotating scripts (benefits → enrollment → coverage → claims → testimonials)
- [x] Format for NotebookLM video generation (visual cues, pacing)
- [x] Secondary school language level
- [x] Warm, relatable tone with concrete examples

### Phase 2: Video Generation ⏳ **BLOCKED**
- [ ] Provide notebook path: "Implementing Community-Based Health Insurance Schemes"
- [ ] Run `nlm generate-video` for each week's topic
- [ ] Output: 5 × raw MP4 files (~10 min each)
- [ ] Artifact download (if hosted)

### Phase 3: Branding ✅
- [x] FFmpeg script created + tested
- [ ] Run branding script on each raw video: `./brand_adugbo_video.sh`
- [ ] Output: 5 × branded MP4 files (with yellow intro/outro)

### Phase 4: Final QA & Delivery
- [ ] Verify bitrate, duration, resolution
- [ ] Check audio levels
- [ ] Save to: `/home/claw/.openclaw/workspace/outputs/videos/`
- [ ] Filenames: `adugboinsure_week_[1-5]_branded_final.mp4`
- [ ] Report success + file sizes + YouTube upload readiness

### Phase 5: Telegram Notification
- [ ] Post to Jarvis-AdugboInsure group:
  - "✅ Videos ready for upload"
  - Links to files
  - Recommended upload schedule

---

## 📁 Directory Structure

```
/home/claw/.openclaw/workspace/
├── videos/
│   └── adugboinsure_scripts.md          [✅ DONE]
├── scripts/
│   └── brand_adugbo_video.sh            [✅ DONE]
├── outputs/
│   └── videos/
│       ├── adugboinsure_week_1_raw.mp4  [⏳ Pending nlm]
│       ├── adugboinsure_week_1_branded_final.mp4 [⏳ Pending branding]
│       ├── adugboinsure_week_2_branded_final.mp4
│       ├── adugboinsure_week_3_branded_final.mp4
│       ├── adugboinsure_week_4_branded_final.mp4
│       └── adugboinsure_week_5_branded_final.mp4
└── ADUGBOINSURE_VIDEO_TASK_SUMMARY.md   [✅ THIS FILE]
```

---

## 🎯 Next Steps

**To continue, provide:**

1. **Notebook path** for NotebookLM:
   - Full path to the "Implementing Community-Based Health Insurance Schemes" notebook
   - Example: `/path/to/notebooks/health_insurance.ipynb` or `/path/to/notebook.json`

2. **Telegram chat ID** (if you want auto-posting):
   - Chat ID for "Jarvis-AdugboInsure" group
   - Or provide group name with leading `@` (e.g., `@AdugboInsureVideos`)

3. **Logo/branding assets** (optional):
   - Path to AdugboInsure logo PNG (for outro)
   - Default colors confirmed as yellow + white text

**Once provided, the workflow will:**
1. Generate videos from scripts via nlm CLI
2. Apply branding (yellow intro/outro with FFmpeg)
3. Save final MP4s to `outputs/videos/`
4. Post success report to Telegram
5. Confirm YouTube upload readiness

---

## 📊 Summary

| Task | Status | Output |
|------|--------|--------|
| Script writing (5 topics) | ✅ DONE | `videos/adugboinsure_scripts.md` |
| Language/tone adjustment | ✅ DONE | Secondary school + warm + concrete |
| Visual cues (for production) | ✅ DONE | Included in scripts |
| Telegram notification | ⚠️ PENDING | Needs correct chat ID |
| Video generation (nlm CLI) | ⏳ BLOCKED | Needs notebook path |
| FFmpeg branding script | ✅ DONE | `scripts/brand_adugbo_video.sh` |
| Final output directory | ✅ READY | `outputs/videos/` (exists) |
| **Overall** | **55% Complete** | **Awaiting inputs for final phases** |

---

**Created:** 2026-03-25 08:15 UTC  
**Last updated:** 2026-03-25 08:15 UTC  
**Task runner:** Jarvis (Assistant)
