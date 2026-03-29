#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import re
import sys
from pathlib import Path


def inline(text: str) -> str:
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    return text.replace('  ', '<br/>')


def render(md_path: str, pdf_path: str):
    raw = Path(md_path).read_text()
    lines = raw.splitlines()

    styles = getSampleStyleSheet()
    title = ParagraphStyle('title', parent=styles['Heading1'], fontSize=18, leading=22,
                           textColor=colors.HexColor('#0b57d0'), alignment=TA_CENTER, spaceAfter=6)
    heading = ParagraphStyle('heading', parent=styles['Heading2'], fontSize=11, leading=13,
                             textColor=colors.HexColor('#0b57d0'), spaceBefore=8, spaceAfter=5)
    subheading = ParagraphStyle('subheading', parent=styles['Heading3'], fontSize=10.5, leading=13,
                                textColor=colors.black, spaceBefore=5, spaceAfter=3)
    normal = ParagraphStyle('normal', parent=styles['Normal'], fontSize=9.5, leading=12, spaceAfter=3)
    contact = ParagraphStyle('contact', parent=styles['Normal'], fontSize=9, leading=11,
                             alignment=TA_CENTER, textColor=colors.HexColor('#444444'), spaceAfter=5)
    footer = ParagraphStyle('footer', parent=styles['Normal'], fontSize=8.5, leading=10,
                            textColor=colors.HexColor('#666666'), spaceBefore=6)

    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            leftMargin=0.6*inch, rightMargin=0.6*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []

    for line in lines:
        s = line.strip()
        if not s:
            story.append(Spacer(1, 0.05*inch))
            continue
        if s == '---':
            story.append(Spacer(1, 0.06*inch))
            continue
        if s.startswith('# '):
            story.append(Paragraph(inline(s[2:].strip()), title))
        elif s.startswith('## '):
            story.append(Paragraph(inline(s[3:].strip().upper()), heading))
        elif s.startswith('### '):
            story.append(Paragraph(inline(s[4:].strip()), subheading))
        elif s.startswith('- '):
            story.append(Paragraph('• ' + inline(s[2:].strip()), normal))
        elif s.startswith('*Customized for '):
            story.append(Paragraph(inline(s), footer))
        elif s.startswith('**Contact:**') or s.startswith('**Portfolio:**'):
            story.append(Paragraph(inline(s), contact))
        else:
            story.append(Paragraph(inline(s), normal))

    doc.build(story)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: render_markdown_cv_to_pdf.py input.md output.pdf')
        sys.exit(1)
    render(sys.argv[1], sys.argv[2])
    print(f'Created {sys.argv[2]}')
