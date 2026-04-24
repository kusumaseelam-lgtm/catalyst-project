import streamlit as st
from PyPDF2 import PdfReader

st.title("🚀 AI Talent Scouting Agent (Advanced)")

# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

# Extract skills
def extract_skills(text):
    skills_db = [
        "python", "machine learning", "data analysis",
        "sql", "excel", "java", "communication",
        "nlp", "deep learning"
    ]
    return list(set([skill for skill in skills_db if skill in text]))

# Match score
def match_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    matched = set(resume_skills) & set(jd_skills)
    return round((len(matched) / len(jd_skills)) * 100, 2)

# Job description
jd = st.text_area("📌 Enter Job Description")

# Upload resumes
uploaded_files = st.file_uploader(
    "📄 Upload Candidate Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

# Button
if st.button("🔍 Analyze Candidates"):

    if not jd:
        st.warning("Please enter job description")
    elif not uploaded_files:
        st.warning("Please upload resumes")
    else:
        jd_skills = extract_skills(jd)

        st.write("### 🧠 Job Skills:", jd_skills)

        results = []

        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resume_skills = extract_skills(text)

            score = match_score(resume_skills, jd_skills)

            results.append({
                "name": file.name,
                "score": score,
                "skills": resume_skills,
                "matched": list(set(resume_skills) & set(jd_skills))
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        st.write("## 🏆 Ranked Candidates")

        for r in results:
            st.markdown(f"""
### 👤 {r['name']}
- 🎯 Match Score: **{r['score']}%**
- 🧠 Skills: {", ".join(r['skills']) if r['skills'] else "No skills found"}
- ✅ Matched: {", ".join(r['matched']) if r['matched'] else "No match"}
---
""")
