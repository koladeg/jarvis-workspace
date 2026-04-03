# Failure Patterns for Boxed PDF Forms

## What failed in the Zenith form tests

### 1. Blanket signature placement
Problem:
- signature image was stamped across too many pages/regions
- some placements landed in ordinary data-entry areas

Guardrail:
- only place signatures on validated signature lines or specimen-signature boxes
- if scope is unclear, ask before placing broadly

### 2. Generic textbox filling on boxed forms
Problem:
- free-text overlays crossed labels and rows
- forms used box-per-character layout, but text was treated as a normal line

Guardrail:
- classify boxed forms early
- switch to per-character placement with row calibration

### 3. Broad full-document attempts too early
Problem:
- too many field classes were attempted at once
- failures compounded and made review harder

Guardrail:
- start with one page or one field class only
- prove the method on a small slice first

### 4. False sense of progress from narrower guesses
Problem:
- reducing scope helped a little, but coordinate guesses were still wrong
- the method was still wrong even when the scope was smaller

Guardrail:
- do not confuse smaller guesses with real calibration
- if box alignment is still off, stop and redesign the method

## Recommended future pattern

1. Inspect PDF structure
2. Identify the real form pages
3. Classify field types
4. Run one calibration draft
5. Review visually
6. Scale only after success

## Temporary signature handling

If the user shares signature images for short-term use:
- use only for the active task/day if requested
- avoid storing as durable memory
- delete temporary derivatives after the task window ends
