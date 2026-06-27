import pandas as pd


def calculate_skill_match(resume_skills, job_skills):

    matching = list(set(resume_skills).intersection(job_skills))

    if len(job_skills) == 0:
        score = 0
    else:
        score = round(len(matching) / len(job_skills) * 100, 2)

    return score


def calculate_experience_match(experience):

    if experience >= 5:
        return 100
    elif experience >= 3:
        return 80
    elif experience >= 1:
        return 60
    else:
        return 40


def calculate_degree_match(degree):

    degree = degree.upper()

    if degree == "PHD":
        return 100
    elif degree in ["M.TECH", "MCA", "MBA", "M.SC"]:
        return 90
    elif degree in ["B.TECH", "BCA", "B.SC"]:
        return 80
    else:
        return 50


def create_feature_vector(skill, experience, degree):

    return pd.DataFrame(
        [[skill, experience, degree]],
        columns=[
            "skill_match",
            "experience_match",
            "degree_match"
        ]
    )