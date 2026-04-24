jd = st.text_area("Enter Job Description")

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
        - 🧠 Skills: {', '.join(r['skills'])}
        - ✅ Matched: {', '.join(r['matched_skills']) if r['matched_skills'] else 'No matching skills'}
        ---
        """)
