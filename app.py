import streamlit as st
import json

st.title("AI Talent Scouting Agent")

# -----------------------------
# Extract Skills
# -----------------------------
def extract_skills(text):
    skills_db = [
        "python", "machine learning", "data analysis",
        "sql", "excel", "java", "communication"
    ]
    return [skill for skill in skills_db if skill in text.lower()]


# -----------------------------
# Match Score
# -----------------------------
def match_score(candidate, jd_skills):
    candidate_skills = [s.lower() for s in candidate["skills"]]

    if not jd_skills:
        return 0

    matched = set(candidate_skills) & set(jd_skills)
    score = (len(matched) / len(jd_skills)) * 100

    return round(score, 2)


# -----------------------------
# Load Candidates
# -----------------------------
try:
    with open("candidates.json") as f:
