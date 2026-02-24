import streamlit as st
from utils import (
    extract_text_from_pdf,
    calculate_similarity,
    get_missing_keywords,
    get_matched_keywords,
    calculate_ats_score
)

st.set_page_config(page_title="AI Resume Optimization System", layout="centered")

# ---------- UI Styling ----------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>AI Resume Optimization System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Resume Screening using NLP</div>", unsafe_allow_html=True)
st.write("")

# ---------- Inputs ----------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description Here")

# ---------- Analysis ----------
if st.button("Analyze Resume"):

    if uploaded_file is not None and jd_text.strip() != "":

        resume_text = extract_text_from_pdf(uploaded_file)

        similarity_score = calculate_similarity(resume_text, jd_text)
        ats_score = calculate_ats_score(resume_text)
        missing_keywords = get_missing_keywords(resume_text, jd_text)
        matched_keywords = get_matched_keywords(resume_text, jd_text)

        st.subheader("Analysis Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Job Match Score (%)", similarity_score)
            st.progress(int(similarity_score))

        with col2:
            st.metric("ATS Compatibility Score", ats_score)

        # Matched Keywords
        st.subheader("Matched Skills")
        if matched_keywords:
            for word in matched_keywords:
                st.success(f"✔ {word}")
        else:
            st.write("No strong matching keywords found.")

        # Missing Keywords
        st.subheader("Missing Keywords")
        if missing_keywords:
            for word in missing_keywords:
                st.error(f"✘ {word}")
        else:
            st.success("No major keywords missing!")

        # Suggestions
        st.subheader("Improvement Suggestions")

        suggestions = []

        if similarity_score < 50:
            suggestions.append("Add more relevant skills from the job description.")

        if ats_score < 70:
            suggestions.append("Improve structure. Add clear sections like Skills, Projects, Education.")

        if similarity_score >= 70:
            suggestions.append("Your resume is well aligned with the job description.")

        for s in suggestions:
            st.info(s)

        # ---------- Download Report ----------
        report = f"""
AI RESUME ANALYSIS REPORT
----------------------------
Job Match Score: {similarity_score} %
ATS Score: {ats_score}

Matched Skills:
{', '.join(matched_keywords) if matched_keywords else "None"}

Missing Skills:
{', '.join(missing_keywords) if missing_keywords else "None"}

Suggestions:
{', '.join(suggestions)}
"""

        st.download_button(
            label="Download Analysis Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )

    else:
        st.warning("Please upload resume and paste job description.")
st.markdown("___")
st.markdown("Developed by: Manyam Prakash</b><br>B.tech - ECE</Rise Krishna Sai Prakasam Group Of institutions",unsafe_allow_html=True)
