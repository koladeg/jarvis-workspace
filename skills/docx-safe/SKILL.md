---
name: docx-safe
description: Create, read, review, or edit `.docx` documents with local-only tooling and layout verification. Use when Word document formatting matters and prefer `python-docx` for structured edits plus the bundled render helper for DOCX to PDF to PNG page checks. Treat `.docm` files and other untrusted Office files as risky and avoid enabling macros.
---

# docx-safe

Use this skill for Word documents where formatting matters, not just raw text.

## When to use

- Create a new `.docx` with headings, tables, lists, or basic report structure.
- Edit an existing `.docx` while preserving readable layout.
- Review a document where pagination, tables, or diagrams matter.
- Produce a final client-ready Word file and verify how pages actually render.

## Guardrails

- Treat `.docm`, `.dotm`, and untrusted Office files as risky. Do not enable macros or trust embedded code.
- Keep work local. Do not upload documents or use remote conversion services unless the user explicitly asks.
- Render from a copy or a temporary path when the source document must remain untouched.
- If visual rendering is unavailable, say that layout was not fully verified.

## Workflow

1. Identify the file type.
   - For `.docx`, use `python-docx` for structured edits.
   - For `.docm` or template formats, avoid macro execution and preserve the original unless the user explicitly wants format conversion.
2. Prefer visual review.
   - Use the bundled render helper when `soffice` and `pdftoppm` are available.
   - Inspect rendered pages for spacing, alignment, clipped text, table overflow, and page breaks.
3. Make the document changes.
   - Use consistent heading levels, margins, spacing, and table widths.
   - Keep typography plain and professional unless the file already has a design system.
4. Re-render after each meaningful change.
5. Clean up temp output unless the user wants the render artifacts kept.

## Commands

Install Python packages if needed:

```bash
python3 -m pip install python-docx pdf2image
```

Install local rendering tools if needed:

```bash
# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils

# macOS
brew install libreoffice poppler
```

Render a document to page PNGs:

```bash
python3 skills/docx-safe/scripts/render_docx.py \
  /absolute/path/to/file.docx \
  --output-dir /absolute/path/to/tmp/doc-pages
```

## Output conventions

- Use `tmp/docs/` for temporary render output.
- Use `output/doc/` for final deliverables when working inside this workspace.
- Keep filenames stable and descriptive.

## Quality bar

- Final documents should look intentional, not default-template rough.
- Tables must remain readable and stay inside page bounds.
- Lists, headings, and paragraph spacing must be consistent.
- Do not leave placeholders, broken references, or tool artifacts in the final document.
- Use ASCII hyphens in generated content unless the existing document clearly requires something else.

## Resources

- `scripts/render_docx.py` converts a local Word document to PDF and page PNGs for visual review.
