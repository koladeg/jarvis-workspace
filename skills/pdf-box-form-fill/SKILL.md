---
name: pdf-box-form-fill
description: Fill boxed bank forms, scanned PDF forms, and signature-heavy PDFs with a calibration-first workflow. Use when a PDF is not truly fillable, when text must land inside fixed character boxes, when signatures/checkmarks must be placed precisely, or when a prior PDF edit failed because generic textbox placement or blanket signature stamping was inaccurate.
---

# PDF Box Form Fill

Use a **calibration-first** workflow. Do not guess.

## Quick rules

- Treat bank/account-opening forms as **hostile layouts** until proven otherwise.
- Check whether the PDF is:
  1. truly fillable
  2. scanned/image-based
  3. boxed/cell-per-character
  4. mixed
- Never blanket-stamp signatures across a document.
- Never place free text into boxed forms without checking character spacing and row alignment.
- Prefer a **one-page or one-field-class test** before full-document filling.

## Workflow

### 1. Inspect the PDF first

Determine:
- page count
- whether form fields exist
- which pages actually contain the target form
- whether target fields are normal text lines, checkboxes, signatures, or character boxes

Use lightweight extraction first:
- `pypdf` / `pdfinfo` for page/field inspection
- page renders for visual checks
- image analysis only when structure is unclear

If the PDF is truly fillable, use the native form-field route instead of coordinate overlays.

### 2. Classify the task before editing

Pick one class only:
- **text fields**
- **checkboxes**
- **signatures**
- **character-box fields**

Do not mix all classes in the first pass unless the layout is already proven.

### 3. Run a narrow calibration test

Start with exactly one of these:
- one page only
- one field type only
- one or two fields only

Examples:
- company name + RC number only
- checkboxes only
- signature lines only

Export a draft and inspect it before scaling up.

### 4. Handle each field type differently

#### Normal text fields
- Use restrained text boxes.
- Keep font small and neutral.
- Do not cross labels or adjacent rows.

#### Character-box fields
- Place text **character by character**.
- Calibrate against the actual box grid on that row.
- Match row baseline before filling full values.
- If the first character alignment is wrong, stop and recalibrate.

#### Checkboxes
- Use small `X` or check marks centered in the box.
- Do not let marks touch labels or box borders.

#### Signatures
- Place signatures only on validated signature lines or specimen-signature boxes.
- Ask before using one signature everywhere unless the user explicitly requests broad use.
- Treat signatures as temporary assets unless the user asks otherwise.

### 5. Preview before claiming success

Before sending the output:
- inspect target pages visually
- confirm no text overlaps labels
- confirm signatures are not inside normal text-entry fields
- confirm check marks are inside boxes
- describe the draft honestly as draft vs final

## Escalation rules

Escalate when:
- the form is boxed/cell-based and alignment is failing
- multiple pages need manual calibration
- signature placement is ambiguous
- OCR/scanned layout makes detection unreliable

When escalating, prefer a stronger reasoning pass to:
- map page structure
- choose a calibration strategy
- define safer coordinate regions

## Failure patterns from real use

Avoid these mistakes:
- blanket signature stamping across all pages
- treating boxed forms like normal textboxes
- filling full documents before proving one page works
- placing text based on rough guesses instead of validated rows
- mixing text, checkboxes, and signatures in one unproven pass

## Bundled resources

- Read `references/failure-patterns.md` when a prior PDF edit went badly and you need the practical lessons.

## Output standard

When returning a draft, say what was actually done:
- pages touched
- field classes touched
- whether placement is calibrated or approximate
- whether the file is a test artifact or a real draft
