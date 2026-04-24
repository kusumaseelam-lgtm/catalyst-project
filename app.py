import streamlit as st
import json

st.title("AI Talent Scouting Agent")

# -----------------------------
# Function: Extract Skills
# -----------------------------
def extract_skills(text):
    skills_db = [
        "python", "machine learning", "data analysis",
        "sql", "excel", "java", "communication"
    ]
    return [skill for skill in skills_db if skill in text.lower()]


# -----------------------------
# Function: Match Score
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
    st.error("candidates.json file not found!")
    candidates = []


# -----------------------------
# UI Input
# -----------------------------
jd = st.text_area("Enter Job Description")


# -----------------------------
# Button Logic
# -----------------------------
if st.button("Find Candidates"):

    if not jd:
        st.warning("Please enter a job description")
    else:
        jd_skills = extract_skills(jd)

        st.write("### Extracted Skills:", jd_skills)

        results = []

        for c in candidates:
            score = match_score(c, jd_skills)

            interest = st.selectbox(
                f"{c['name']} interested?",
                ["Yes", "Maybe", "No"],
                key=c['name']
            )

            interest_score = 90 if interest == "Yes" else 60 if interest == "Maybe" else 20

            results.append({
                "name": c["name"],
                "score": score,
                "interest": interest_score,
                "skills": c["skills"],
                "matched_skills": list(set(c["skills"]) & set(jd_skills))
            })

        # Sort results
        results = sorted(
            results,
            key=lambda x: (x["score"], x["interest"]),
            reverse=True
        )

        # -----------------------------
        # Display Results
        # -----------------------------
        st.write("## Top Candidates")

        for r in results:
            st.markdown(f"""
### 👤 {r['name']}
- 🎯 Match Score: **{r['score']}%**
- 👍 Interest: **{r['interest']}**
- 🧠 Skills: {", ".join(r['skills'])}
- ✅ Matched: {", ".join(r['matched_skills']) if r['matched_skills'] else "No match"}
---
""")
