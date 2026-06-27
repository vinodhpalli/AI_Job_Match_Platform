import matplotlib.pyplot as plt
import streamlit as st

def create_skill_pie_chart(matching_skills, missing_skills):
    labels = [
        "Matching Skills",
        "Missing Skills"
    ]

    sizes = [
        len(matching_skills),
        len(missing_skills)
    ]

    # Ensure we don't pass empty data arrays to Matplotlib
    if sum(sizes) == 0:
        st.warning("No data available to display distribution.")
        return

    fig, ax = plt.subplots(figsize=(6, 6))

    # Step 1: Improved Pie Chart Layout & Colors
    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4CAF50", "#F44336"],
        explode=(0.05, 0),
        shadow=True
    )

    ax.set_title("Skill Match Distribution")
    st.pyplot(fig)


def create_skill_bar_chart(resume_skills, job_skills):
    labels = [
        "Resume Skills",
        "Job Skills"
    ]

    values = [
        len(resume_skills),
        len(job_skills)
    ]

    fig, ax = plt.subplots(figsize=(6, 4))

    # Step 2: Improved Bar Chart with unique colors
    bars = ax.bar(
        labels,
        values,
        color=["#2196F3", "#FF9800"]
    )

    ax.set_ylabel("Number of Skills")
    
    # Step 4: Add Y-Axis Grid
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    
    ax.set_title("Resume vs Job Skills")

    # Step 3: Show Numeric Metrics Above Bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            str(height),
            ha="center",
            va="bottom",
            fontsize=11
        )

    st.pyplot(fig)