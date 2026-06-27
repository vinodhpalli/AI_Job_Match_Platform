import pdfplumber
import pandas as pd
import re
import string
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

skill_dictionary = pd.read_csv(
    os.path.join(BASE_DIR, "skill_dictionary.csv")
)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills(text):
    text = clean_text(text)

    skills = []

    for skill in skill_dictionary["skill"]:
        if skill.lower() in text:
            skills.append(skill)

    return sorted(list(set(skills)))


DEGREES = [
    "phd",
    "m.tech",
    "b.tech",
    "mba",
    "mca",
    "bca",
    "m.sc",
    "b.sc"
]


def extract_degree(text):
    text = text.lower()

    for degree in DEGREES:
        if degree in text:
            return degree.upper()

    return "Unknown"


def extract_experience(text):
    pattern = r'(\d+)\+?\s*years?'

    matches = re.findall(pattern, text.lower())

    if len(matches) == 0:
        return 0

    return max(map(int, matches))


def extract_pdf_text(uploaded_file):
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text