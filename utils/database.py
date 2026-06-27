import sqlite3
import pandas as pd
import streamlit as st


def create_database():

    conn = sqlite3.connect("prediction_history.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            job_title TEXT,
            skill_match REAL,
            ai_score REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(resume_name, job_title, skill_match, ai_score):

    conn = sqlite3.connect("prediction_history.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history
        (resume_name, job_title, skill_match, ai_score)
        VALUES (?,?,?,?)
    """, (
        resume_name,
        job_title,
        skill_match,
        ai_score
    ))

    conn.commit()
    conn.close()


def show_history():

    conn = sqlite3.connect("prediction_history.db")

    df = pd.read_sql("SELECT * FROM history ORDER BY id DESC", conn)

    conn.close()

    if len(df) == 0:
        st.warning("No prediction history available.")
    else:
        st.dataframe(df, use_container_width=True)