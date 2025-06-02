import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("AI-Powered Resume Matcher")

backend_url = st.text_input("Backend URL", "https://resume-matcher-app.onrender.com/upload_resumes")
api_key = st.text_input("API Key (optional)", type="password")

resume_files = st.file_uploader("Upload Resume(s)", type=["pdf", "txt"], accept_multiple_files=True)
job_file = st.file_uploader("Upload Job Description (optional)", type=["pdf", "txt"])

if st.button("Match Candidates"):
    if not resume_files:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Processing resumes..."):
            files = [("files", (f.name, f.read(), f.type)) for f in resume_files]
            if job_file:
                files.append(("job_description", (job_file.name, job_file.read(), job_file.type)))

            headers = {"x-api-key": api_key} if api_key else {}
            try:
                response = requests.post(backend_url, files=files, headers=headers)
                data = response.json()

                for result in data["results"]:
                    st.subheader(f"Results for {result['filename']}")
                    st.markdown(f"**Extracted Skills:** {', '.join(result['extracted_skills']) or 'None'}")

                    df = pd.DataFrame(result['matches'])
                    if df.empty:
                        st.info("No matching jobs found.")
                    else:
                        st.dataframe(df)
                        st.bar_chart(df.set_index("title")["match_score"])

            except Exception as e:
                st.error(f"Error: {e}")
