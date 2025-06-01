import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄")
st.title("📄 AI Resume Matcher")
st.write("Upload your resume and get matched to jobs using AI!")

# Upload file input
uploaded_file = st.file_uploader("Choose a resume file (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Uploading and analyzing resume..."):
        files = {'file': (uploaded_file.name, uploaded_file.read())}

        # IMPORTANT: Replace this with your deployed Render backend URL
        api_url = "https://resume-matcher-app.onrender.com/upload_resume"

        try:
            response = requests.post(api_url, files=files)
            if response.ok:
                data = response.json()
                st.success("Skills and job matches found!")

                st.subheader("🧠 Extracted Skills")
                st.write(", ".join(data.get("extracted_skills", [])))

                st.subheader("💼 Best Job Matches")
                for match in data.get("matches", []):
                    st.markdown(f"**{match['title']}** — Match Score: `{match['match_score']*100:.0f}%`")
            else:
                st.error("Something went wrong. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
