import streamlit as st
import json
st.set_page_config(page_title="AI Talent Agent", layout="centered")

st.markdown("<h1 style='text-align: center;'>AI Talent Scouting Agent 🚀</h1>", unsafe_allow_html=True)

# Load candidates
with open("candidates.json") as f:
    candidates = json.load(f)

jd = st.text_area("Enter Job Description")

def extract_skills(text):
    skills = ["Python", "SQL", "Java", "Machine Learning", "Data Analysis"]
    return [s for s in skills if s.lower() in text.lower()]

def match_score(candidate, jd_skills):
    match = len(set(candidate["skills"]) & set(jd_skills))
    return round((match / len(jd_skills)) * 100, 2) if jd_skills else 0

if st.button("Find Candidates"):
    jd_skills = extract_skills(jd)
    results = []

    for c in candidates:
        score = match_score(c, jd_skills)
        interest = st.selectbox(f"{c['name']} interested?", ["Yes", "Maybe", "No"])

        interest_score = 90 if interest == "Yes" else 60 if interest == "Maybe" else 20
        results.append({
    "name": c["name"],
    "score": score,
    "interest": interest_score,
    "skills": c["skills"],
    "matched_skills": list(set(c["skills"]) & set(jd_skills))
})
        
        
    results = sorted(results, key=lambda x: (x['score'], x['interest']), reverse=True)

for r in results:
    st.markdown(f"""
### 👤 {r['name']}
- 🎯 Match Score: **{r['score']}**
- 💡 Interest: **{r['interest']}**
- 🧠 Skills: {", ".join(r['skills'])}
- ✅ Matched: {', '.join(r['matched_skills']) if r['matched_skills'] else 'No matching skills'}
---
""")
