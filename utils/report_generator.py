from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import navy
from datetime import datetime

# Step 16.3 – Create Styles
styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER
title_style.textColor = navy

heading_style = styles["Heading2"]
normal_style = styles["BodyText"]

def generate_report(
    filename,
    degree,
    experience,
    resume_skills,
    job_title,
    company,
    matching_skills,
    missing_skills,
    skill_match,
    ai_score
):
    # Create PDF Template Setup
    doc = SimpleDocTemplate(filename)
    story = []

    # Step 16.4 – Add Report Title
    story.append(
        Paragraph(
            "AI Job Match Report",
            title_style
        )
    )
    story.append(Spacer(1, 20))

    # Step 16.5 – Candidate Information
    story.append(
        Paragraph(
            "<b>Candidate Information</b>",
            heading_style
        )
    )
    story.append(
        Paragraph(
            f"Degree : {degree}",
            normal_style
        )
    )
    story.append(
        Paragraph(
            f"Experience : {experience} Years",
            normal_style
        )
    )
    story.append(
        Paragraph(
            f"Resume Skills : {len(resume_skills)}",
            normal_style
        )
    )
    story.append(Spacer(1, 15))

    # Step 16.6 – Job Information
    story.append(
        Paragraph(
            "<b>Job Information</b>",
            heading_style
        )
    )
    story.append(
        Paragraph(
            f"Role : {job_title}",
            normal_style
        )
    )
    story.append(
        Paragraph(
            f"Company : {company}",
            normal_style
        )
    )
    story.append(Spacer(1, 15))

    # Step 16.7 – Matching Skills
    story.append(
        Paragraph(
            "<b>Matching Skills</b>",
            heading_style
        )
    )
    for skill in matching_skills:
        story.append(
            Paragraph(
                "✔ " + skill,
                normal_style
            )
        )
    story.append(Spacer(1, 15))

    # Step 16.8 – Missing Skills
    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            heading_style
        )
    )
    for skill in missing_skills:
        story.append(
            Paragraph(
                "✘ " + skill,
                normal_style
            )
        )
    story.append(Spacer(1, 15))

    # Step 16.9 – Final Scores
    story.append(
        Paragraph(
            "<b>Overall Scores</b>",
            heading_style
        )
    )
    story.append(
        Paragraph(
            f"Skill Match : {skill_match:.2f}%",
            normal_style
        )
    )
    story.append(
        Paragraph(
            f"AI Match : {ai_score:.2f}%",
            normal_style
        )
    )
    story.append(Spacer(1, 15))

    # Step 16.10 – Generation Date
    today = datetime.now().strftime("%d-%m-%Y")
    story.append(
        Paragraph(
            f"Generated On : {today}",
            normal_style
        )
    )

    # Save the finalized story to PDF file document matrix
    doc.build(story)