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
        candidates = json.load(f)
except:
    candidates = []
    st.warning("No candidates.json file found")
jd_text = st.text_area("Enter Job Description")

if st.button("Analyze Candidates"):

    if not jd_text.strip():
        st.error("Please enter job description")
    else:
        jd_skills = extract_skills(jd_text)

        st.subheader("Extracted Skills:")
        st.write(jd_skills)

        results = []

        for candidate in candidates:
            score = match_score(candidate, jd_skills)
            results.append({
                "name": candidate["name"],
                "score": score,
                "skills": candidate["skills"]
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        st.subheader("Candidate Rankings:")

        for r in results:
            st.write(f"👤 {r['name']}")
            st.write(f"Skills: {r['skills']}")
            st.write(f"Match Score: {r['score']}%")
            st.write("---")
