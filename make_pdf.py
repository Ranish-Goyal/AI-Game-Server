from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf():
    pdf_filename = "Ranish_Goyal_Resume.pdf"
    doc = SimpleDocTemplate(
        pdf_filename, 
        pagesize=letter,
        rightMargin=36, 
        leftMargin=36,
        topMargin=36, 
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.HexColor('#1A202C')
    )
    
    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=10
    )
    
    heading_style = ParagraphStyle(
        'ResumeHeading',
        parent=styles['Heading2'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=3
    )

    story = []

    # Header
    story.append(Paragraph("<b>RANISH GOYAL</b>", title_style))
    story.append(Paragraph("9084931881 | goyalranish@gmail.com | Solan (HP) | GitHub | LinkedIn", contact_style))
    
    # Profile Summary
    story.append(Paragraph("<b>PROFILE SUMMARY</b>", heading_style))
    story.append(Paragraph("Aspiring Game Developer pursuing a B.Tech in Computer Science with a specialization in Artificial Intelligence[cite: 2]. Experienced in Unreal Engine, C++ basics, Blueprint scripting, and building AI-driven gameplay systems[cite: 2]. Skilled in narrative design and content writing, combining technical problem-solving with creative world-building[cite: 1, 2].", body_style))

    # Education
    story.append(Paragraph("<b>EDUCATION</b>", heading_style))
    story.append(Paragraph("• <b>B.Tech in Computer Science & Engineering (AI)</b> | Shoolini University | 8.8 CGPA (2022–2026)[cite: 2]", body_style))
    story.append(Paragraph("• <b>Class XII</b> | Saraswati Bal Mandir, Hapur | 82% (2020–2021)[cite: 2]", body_style))
    story.append(Paragraph("• <b>Class X</b> | Saraswati Bal Mandir, Hapur | 78% (2018–2019)[cite: 2]", body_style))

    # Skills
    story.append(Paragraph("<b>TECHNICAL & CREATIVE SKILLS</b>", heading_style))
    story.append(Paragraph("• <b>Languages & Frameworks:</b> C++, C, Python, FastAPI, Unreal Engine, Database Management[cite: 2].", body_style))
    story.append(Paragraph("• <b>Core Competencies:</b> Data Structures & Algorithms, Game Development, Problem Solving, Project Management[cite: 2].", body_style))
    story.append(Paragraph("• <b>Creative:</b> Content Writing, Narrative Design, World-Building[cite: 1, 2].", body_style))

    # Projects & Experience
    story.append(Paragraph("<b>PROJECTS & EXPERIENCE</b>", heading_style))
    story.append(Paragraph("• <b>The Simulation (Narrative Design & Content Writing):</b> Developed a comprehensive story summary for a game where a captive family must survive a virtual-reality simulation[cite: 1]. Designed distinct progression mechanics, such as an aggressive playstyle for the grandmother, and built a world map divided into five regions based on mythological deities[cite: 1].", body_style))
    story.append(Paragraph("• <b>AI Game Server Integration:</b> Engineered a local Python backend using FastAPI to dynamically trigger AI asset generation, bridging game engines and real-time AI tools.", body_style))
    story.append(Paragraph("• <b>Unreal Engine AI Shooting Game:</b> Developed a shooting game using Blueprint scripting featuring AI NPCs that track the player to designated areas and fight back, utilizing health bars for both entities[cite: 2].", body_style))
    story.append(Paragraph("• <b>Crypt Raider:</b> Created an independent game in Unreal Engine focused on searching and stealing items[cite: 2].", body_style))
    story.append(Paragraph("• <b>E-Commerce Database Project (Project Head):</b> Led a team in March 2024 to design a robust database system, handling user profiles and transaction processing while optimizing queries[cite: 2].", body_style))
    story.append(Paragraph("• <b>Hackathon & Sprint Team Leader:</b> Directed backend operations and presented projects for Shoolini University events[cite: 2]. Trained and created a Python picture identification AI model[cite: 2].", body_style))

    doc.build(story)
    print(f"Successfully generated {pdf_filename}!")

if __name__ == "__main__":
    generate_pdf()