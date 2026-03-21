#!/usr/bin/env python3
"""
Create professional CV PDF from markdown template.
Uses reportlab for PDF generation.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import sys

def create_cv_pdf(output_path):
    """Create a professional CV PDF."""
    
    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.6*inch, rightMargin=0.6*inch)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    name_style = ParagraphStyle(
        'CustomName',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=4,
        alignment=TA_CENTER
    )
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333'),
        spaceAfter=2
    )
    
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666'),
        spaceAfter=10
    )
    
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=6,
        spaceBefore=8,
        borderColor=colors.HexColor('#dddddd'),
        borderWidth=1,
        borderPadding=4
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=12
    )
    
    # Header
    story.append(Paragraph("KOLADE GUREJE", name_style))
    story.append(Paragraph("Senior React Native Developer", title_style))
    story.append(Paragraph(
        "+234 8079366207 | koladegureje@gmail.com | Lagos, Nigeria<br/>" +
        "<a href='https://koladeg.github.io/'>Portfolio</a> | " +
        "<a href='https://github.com/koladeg'>GitHub</a> | " +
        "<a href='https://linkedin.com/in/kolade-gureje'>LinkedIn</a>",
        contact_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    
    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
    summary_text = (
        "Senior React Native specialist with 4+ years delivering production mobile applications in healthcare "
        "and fintech. Proven expertise in Redux state management, RESTful APIs, Firebase, and cross-platform "
        "development. Seeking Canada-based opportunity to build enterprise-grade mobile solutions while "
        "establishing international tech career. Open to work permit sponsorship and relocation."
    )
    story.append(Paragraph(summary_text, normal_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_style))
    skills_data = [
        ["Mobile Development", "Backend & APIs", "DevOps & Tools"],
        [
            "React Native/Expo<br/>Redux • Firebase<br/>TypeScript • JavaScript<br/>iOS & Android Deployment",
            "Node.js • REST APIs<br/>MongoDB • Firebase<br/>Python • Socket.IO",
            "Git • CircleCI<br/>AWS (S3) • Docker<br/>Jest • Sentry<br/>Monitoring & CI/CD"
        ]
    ]
    skills_table = Table(skills_data, colWidths=[2*inch, 2*inch, 2*inch])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('FONTSIZE', (0, 1), (-1, 1), 9),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.white]),
    ]))
    story.append(skills_table)
    
    story.append(Spacer(1, 0.1*inch))
    
    # Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
    
    # Job 1
    story.append(Paragraph(
        "<b>Software Developer / Deputy Manager</b> — SIFAX | Jan 2020 – Present (3+ years)",
        normal_style
    ))
    story.append(Paragraph(
        "• Architected and deployed cross-platform mobile apps using React Native<br/>" +
        "• Integrated RESTful APIs and Redux for complex state management<br/>" +
        "• Conducted unit testing with Jest, maintaining high code coverage<br/>" +
        "• Mentored junior developers on React Native best practices<br/>" +
        "<i>Tech: React Native, Redux, Firebase, REST APIs, Node.js</i>",
        normal_style
    ))
    story.append(Spacer(1, 0.05*inch))
    
    # Job 2
    story.append(Paragraph(
        "<b>Project Lead Developer</b> — University College Hospital (UCH) | Sep 2024 – Nov 2024",
        normal_style
    ))
    story.append(Paragraph(
        "• Led team of 3 to develop mhGAP mental health app replica for clinical study<br/>" +
        "• <b>Impact:</b> 250+ patient visits, 98% data accuracy<br/>" +
        "• Implemented eForms and workflows in React Native<br/>" +
        "• Streamlined API integrations for real-time analytics<br/>" +
        "<i>Tech: React Native, Redux, Formik, Firebase, REST APIs</i>",
        normal_style
    ))
    story.append(Spacer(1, 0.05*inch))
    
    # Job 3
    story.append(Paragraph(
        "<b>Front-End Developer</b> — NeighborTailor.com | Nov 2019 – Nov 2022",
        normal_style
    ))
    story.append(Paragraph(
        "• Built responsive React Native components for e-commerce platform<br/>" +
        "• Improved app load time by 35% through optimization<br/>" +
        "• Collaborated with backend team on 15+ feature integrations",
        normal_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    
    # Key Projects
    story.append(Paragraph("KEY PROJECTS", section_style))
    story.append(Paragraph(
        "<b>mhGAP Replica</b> — WHO Mental Health Intervention Platform<br/>" +
        "<i>Impact:</i> 250+ patient visits, 98% data accuracy | " +
        "<i>Tech:</i> React Native, Redux, Firebase<br/><br/>" +
        "<b>GoTruck</b> — Logistics Mobile App<br/>" +
        "<i>Impact:</i> Enterprise logistics for 50+ daily shipments | " +
        "<i>Tech:</i> React Native, Redux, APIs<br/><br/>" +
        "<b>ReportPrep AI</b> — Voice-First Report Generation<br/>" +
        "<i>Impact:</i> 500+ documents monthly | " +
        "<i>Tech:</i> Next.js, Firebase, Gemini AI",
        normal_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    
    # Education & Certifications
    story.append(Paragraph("EDUCATION & CERTIFICATIONS", section_style))
    story.append(Paragraph(
        "<b>AWS Certified Solutions Architect – Associate</b> | Nov 2022 (Score: 920/1000)<br/>" +
        "<b>Cloud DevOps Nanodegree — Udacity</b> | Jun 2022 – Aug 2022<br/>" +
        "<b>Ironhack Bootcamp — Miami, FL</b> | Jun 2020 – Aug 2020 (Full-Stack Web Development)<br/>" +
        "<b>Bachelor of Computer Science & IT — Bowen University</b> | 2010 – 2014 (GPA 3.5)",
        normal_style
    ))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF created successfully: {output_path}")

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "/home/claw/.openclaw/workspace/CV_Orium_SeniorReactNativeDeveloper.pdf"
    create_cv_pdf(output)
