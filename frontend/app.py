import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
import time
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
.big-font {
    font-size:36px !important;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
}
.highlight {
    color: #2196F3;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-font">🧠 Smart Resume Matcher</div>', unsafe_allow_html=True)

st.write("## Upload Resume and Job Description or Paste Job Link")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
with col2:
    jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

job_url = st.text_input("📎 Or paste a link to an Indeed job posting")

# Load animations
@st.cache_data
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

upload_anim = load_lottie_url("https://lottie.host/22632438-e28d-4e18-8f18-9870cd8cc8f5/sTkakzCfuX.json")
match_anim = load_lottie_url("https://lottie.host/84e0eae3-fc25-4192-a50f-792c33ae218e/I8cWZr9sLf.json")
success_anim = load_lottie_url("https://lottie.host/abe309e6-d9f2-42b3-8d2e-3be342c11eb0/fD63tuvrXZ.json")

if not resume_file or (not jd_file and not job_url):
    st.info("📤 Please upload a resume and either a job description or paste a job link.")
    if upload_anim:
        st_lottie(upload_anim, speed=1, height=300)

def extract_text_from_indeed(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        job_text = "\n".join([tag.get_text(strip=True) for tag in soup.find_all(['p', 'li'])])
        return job_text
    except Exception as e:
        st.error(f"Failed to extract job description from link: {e}")
        return None

if resume_file and (jd_file or job_url):
    st.write("### 🔄 Matching in progress...")
    if match_anim:
        st_lottie(match_anim, speed=1, height=300)

    files = {"resume": resume_file}

    if jd_file:
        files["job_description"] = jd_file
    elif job_url:
        jd_text = extract_text_from_indeed(job_url)
        if jd_text:
            files["job_description"] = ("job_desc.txt", jd_text)
        else:
            st.stop()

    response = requests.post("https://resume-matcher-app.onrender.com/upload_resume", files=files)

    if response.status_code == 200:
        result = response.json()
        score = result.get("score", 0)

        st.subheader("🎯 Match Score")
        st.progress(min(score / 100, 1.0))
        st.metric("Score (%)", f"{score:.2f}%")

        if score > 80:
            st.success("✅ Strong Match!")
            if success_anim:
                st_lottie(success_anim, speed=1, height=250)
        elif score > 50:
            st.warning("⚠️ Partial Match")
        else:
            st.error("❌ Weak Match")

        with st.expander("📋 Full Matching Breakdown"):
            details = result.get("details", {})
            for category, matches in details.items():
                st.markdown(f"### 🔹 {category.capitalize()}")
                for match in matches:
                    if isinstance(match, str):
                        st.markdown(f"- <span class='highlight'>{match}</span>", unsafe_allow_html=True)
                    else:
                        st.write(match)

        st.download_button("📄 Download Resume", resume_file, file_name="resume.pdf")
        if jd_file:
            st.download_button("📄 Download Job Description", jd_file, file_name="job_desc.pdf")
    else:
        st.error("Failed to get a response from the backend.")
