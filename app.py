import os
import streamlit as st
import pandas as pd
import ast
from datetime import datetime

from utils.resume_parser import (
    extract_pdf_text,
    extract_skills,
    extract_degree,
    extract_experience
)

from utils.feature_engineering import (
    calculate_skill_match,
    calculate_degree_match,
    calculate_experience_match,
    create_feature_vector
)

from utils.prediction import predict

from utils.database import (
    create_database,
    save_prediction,
    show_history
)

from utils.report_generator import generate_report

from utils.charts import (
    create_skill_pie_chart,
    create_skill_bar_chart
)

# Phase 14: Skill Taxonomy Blueprint Data Map
SKILL_CATEGORIES = {
    "Programming": ["Python", "Java", "C++", "SQL", "R", "Go", "Rust", "JavaScript", "TypeScript"],
    "Machine Learning & AI": ["Machine Learning", "Deep Learning", "TensorFlow", "Keras", "Scikit-learn", "PyTorch", "NLP", "LLM", "Computer Vision"],
    "Data Visualization & Analytics": ["Power BI", "Tableau", "Excel", "Matplotlib", "Seaborn", "Looker", "Pandas", "NumPy"],
    "Cloud & DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Git", "Jenkins"]
}

# Page Configuration
st.set_page_config(
    page_title="AI Job Match Platform",
    page_icon="🤖",
    layout="wide"
)

# Initialize Database
create_database()

# ---------------------------------------------------------
# Sidebar Control Panel
# ---------------------------------------------------------
st.sidebar.image("assets/logo.png", width=140)
st.sidebar.title("🤖 AI Job Match")

st.sidebar.markdown("---")
st.sidebar.header("📄 Resume Intake")
uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

# Load Dataset early to populate sidebar filters dynamically
try:
    jobs = pd.read_csv("jobs_parsed.csv")
except Exception as e:
    st.error(f"❌ Failed to load jobs_parsed.csv: {e}")
    st.stop()

# Use all jobs from dataset directly
filtered_jobs = jobs.copy()

# ----------------------------------------
# Select Job
# ----------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("💼 Select Job")

job_titles = sorted(
    filtered_jobs["title"].dropna().unique().tolist()
)

if len(job_titles) > 0:
    selected_job = st.sidebar.selectbox(
        "Select a Job",
        job_titles
    )
    st.sidebar.success(f"{len(job_titles)} Jobs Available")
else:
    st.sidebar.warning("No jobs found.")
    selected_job = None


# ---------------------------------------------------------
# Main Page Layout Engine
# ---------------------------------------------------------
st.title("🤖 AI Job Match Platform")
st.write("Analyze structural compatibility vectors between corporate requisitions and candidate profiles.")

if uploaded_file is not None and selected_job is not None:
    st.success("✅ Application profiles loaded. Processing structural comparisons...")

    # Resume Processing Parsing
    resume_text = extract_pdf_text(uploaded_file)
    resume_skills = extract_skills(resume_text)
    degree = extract_degree(resume_text)
    experience = extract_experience(resume_text)

    # Extract Job attributes safely from the filtered scope
    job = filtered_jobs[filtered_jobs["title"] == selected_job].iloc[0]

    # Parse Required Skills Cleanly
    try:
        job_skills_raw = job["job_skills"]
        if isinstance(job_skills_raw, str):
            job_skills = ast.literal_eval(job_skills_raw)
        else:
            job_skills = job_skills_raw
        
        job_skills = [s.strip() for s in job_skills if len(s.strip()) >= 3]
        job_skills = sorted(list(set(job_skills)))
    except Exception:
        job_skills = []

    # Intersect Metrics
    matching_skills = sorted(list(set(resume_skills).intersection(job_skills)))
    missing_skills = sorted(list(set(job_skills) - set(resume_skills)))

    # Calculations for metrics
    if len(job_skills) > 0:
        skill_match_percentage = round((len(matching_skills) / len(job_skills)) * 100, 2)
    else:
        skill_match_percentage = 0.0

    # AI Prediction Precomputations 
    experience_match = calculate_experience_match(experience)
    degree_match = calculate_degree_match(degree)
    features = create_feature_vector(skill_match_percentage, experience_match, degree_match)
    raw_output = predict(features)

    try:
        val = float(raw_output)
        if 1.0 < val <= 100.0:
            final_score = val
        elif 0.0 <= val <= 1.0:
            final_score = val * 100.0
        else:
            final_score = max(0.0, min((val / 1000.0) if val > 100.0 else val, 100.0))
    except (ValueError, TypeError):
        final_score = 0.0

    # ---------------------------------------------------------
    # ✅ Refactored Candidate Dashboard (Steps 18.2 - 18.9)
    # ---------------------------------------------------------
    st.markdown("---")
    st.header("👤 Candidate Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    with col1:
        st.metric(
            "Resume Skills",
            len(resume_skills)
        )
        
    with col2:
        st.metric(
            "Matching Skills",
            len(matching_skills)
        )
        
    with col3:
        st.metric(
            "Missing Skills",
            len(missing_skills)
        )
        
    with col4:
        st.metric(
            "Degree",
            degree if degree else "N/A"
        )
        
    with col5:
        st.metric(
            "Experience",
            f"{experience} Years" if experience else "0 Years"
        )
        
    with col6:
        st.metric(
            "AI Match",
            f"{final_score:.2f}%"
        )

    # ---------------------------------------------------------
    # ✅ Refactored Target Job Section (Steps 18.10 - 18.15)
    # ---------------------------------------------------------
    st.markdown("---")
    st.header("💼 Target Job")
    
    job_col1, job_col2, job_col3, job_col4 = st.columns(4)
    
    with job_col1:
        st.metric(
            "Company",
            job.get("company_name", "N/A")
        )
        
    with job_col2:
        st.metric(
            "Role",
            job.get("title", "N/A")
        )
        
    with job_col3:
        st.metric(
            "Location",
            job.get("location", "N/A")
        )
        
    with job_col4:
        st.metric(
            "Work Type",
            job.get("formatted_work_type", "N/A")
        )

    # ---------------------------------------------------------
    # Phase 13: Enhanced AI Score Section
    # ---------------------------------------------------------
    st.markdown("---")
    st.header("🤖 Advanced AI Match Vector Prediction Engine")
    score_col1, score_col2 = st.columns([1, 2])
    
    with score_col1:
        st.metric(label="Overall Operational Fit Score", value=f"{final_score:.1f}%")
        st.progress(final_score / 100)
    
    with score_col2:
        st.write("### Match Status Evaluation")
        if final_score >= 80:
            st.success("🎉 Excellent Match")
            st.write("The candidate matches the structural prerequisites and predictive feature baselines perfectly.")
        elif final_score >= 60:
            st.warning("👍 Good Match")
            st.write("The profile shows healthy convergence with target metrics but displays addressable core gaps.")
        else:
            st.error("📘 Needs Improvement")
            st.write("Strategic missing gaps detected. Review the up-skilling roadmap details below to correct matching vector metrics.")

    # Extra Optional metadata fields mapping checks (kept safely)
    extra_cols = [col for col in ["salary", "salary_min", "salary_max", "experience_required"] if col in job.index]
    if extra_cols:
        st.write("")
        c_extra = st.columns(len(extra_cols))
        for idx, col_name in enumerate(extra_cols):
            with c_extra[idx]:
                st.metric(
                    col_name.replace("_", " ").title(),
                    str(job[col_name]) if pd.notna(job[col_name]) else "N/A"
                )

    # Resume Preview Accordion
    with st.expander("📄 View Parsed Raw Resume Extraction"):
        st.text_area("Resume Text Mirror", resume_text, height=200)

    # ---------------------------------------------------------
    # ✅ Phase 14: Skill Categories Breakdown
    # ---------------------------------------------------------
    st.markdown("---")
    st.header("📊 Detailed Gap Matrix Analysis")
    
    col5_layout, col6_layout = st.columns(2)
    
    with col5_layout:
        st.subheader("🗂️ Categorized Skill Verification")
        
        # Categorize known items
        uncategorized_matches = list(matching_skills)
        uncategorized_missing = list(missing_skills)
        
        for category, keywords in SKILL_CATEGORIES.items():
            # Find category matches using case-insensitive check intersections
            cat_matches = [s for s in matching_skills if any(k.lower() in s.lower() for k in keywords)]
            cat_missing = [s for s in missing_skills if any(k.lower() in s.lower() for k in keywords)]
            
            if cat_matches or cat_missing:
                st.write(f"#### {category}")
                for m_skill in cat_matches:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;✓ **{m_skill}**")
                    if m_skill in uncategorized_matches: uncategorized_matches.remove(m_skill)
                for mis_skill in cat_missing:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;✗ <span style='color:#ff4b4b'>{mis_skill}</span>", unsafe_allow_html=True)
                    if mis_skill in uncategorized_missing: uncategorized_missing.remove(mis_skill)
        
        # Output everything remaining outside taxonomy rules
        if uncategorized_matches or uncategorized_missing:
            st.write("#### Other Professional Skills")
            for m_skill in uncategorized_matches:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;✓ **{m_skill}**")
            for mis_skill in uncategorized_missing:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;✗ <span style='color:#ff4b4b'>{mis_skill}</span>", unsafe_allow_html=True)

    with col6_layout:
        st.subheader("🎯 Direct Delta Lists")
        flat_col1, flat_col2 = st.columns(2)
        with flat_col1:
            st.write("**All Matches**")
            if matching_skills:
                for skill in matching_skills: st.success(f"✓ {skill}")
            else:
                st.warning("No overlapping matches.")
        with flat_col2:
            st.write("**All Gaps**")
            if missing_skills:
                for skill in missing_skills: st.error(f"✗ {skill}")
            else:
                st.success("Flawless structural symmetry!")

    # Recommended Skills Roadmap
    st.header("📚 Targeted Up-skilling Roadmaps")
    if missing_skills:
        for skill in missing_skills:
            st.info(f"📘 Action Item: Acquire proficiency in **{skill}**")
    else:
        st.success("🎉 Up-skilling complete for this role's baseline requirements!")

    # Step 9 & 10: Charts Presentation
    st.markdown("---")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.header("🥧 Skill Match Distribution")
        create_skill_pie_chart(matching_skills, missing_skills)
    with chart_col2:
        st.header("📊 Resume vs Job Skills")
        create_skill_bar_chart(resume_skills, job_skills)

    # Save historical evaluation metrics 
    save_prediction(uploaded_file.name, selected_job, skill_match_percentage, final_score)

    # Reporting Compilation Engine Download 
    st.markdown("---")
    st.header("📄 Secure Compliance PDF Export")
    if st.button("Compile Structural Evaluation Document"):
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        generate_report(
            "resume_report.pdf", degree, experience, resume_skills,
            job.get("title", "N/A"), job.get("company_name", "N/A"),
            matching_skills, missing_skills, skill_match_percentage, final_score
        )
        st.success("✅ Document compilation pipeline completed successfully!")
        with open("resume_report.pdf", "rb") as pdf_file:
            st.download_button(
                label="⬇ Download Match Report PDF",
                data=pdf_file,
                file_name=f"AI_Job_Match_Report_{current_date}.pdf",
                mime="application/pdf"
            )

    # Historical Database records execution button
    st.markdown("---")
    st.header("📜 System Historical Evaluation Registers")
    if st.button("Query Persistent Log History"):
        show_history()

else:
    st.info("💡 Please finalize your configurations: upload a standard resume file framework and specify a destination target in the sidebar panel.")