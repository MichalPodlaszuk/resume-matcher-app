import streamlit as st
import requests

st.title("📄 AI Resume Matcher")
st.write("Upload your resume (PDF or TXT) to see your best job matches.")

uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Processing your resume..."):
        files = {'file': (uploaded_file.name, uploaded_file.read())}
        # ⬇ Change this to your deployed backend URL if hosted
        response = requests.post("http://localhost:8000/upload_resume", files=files)

        if response.ok:
            data = response.json()
            st.subheader("✅ Extracted Skills:")
            st.write(", ".join(data["extracted_skills"]))

            st.subheader("📊 Job Matches:")
            for match in data["matches"]:
                st.markdown(f"**{match['title']}** — Match Score: `{match['match_score']*100:.0f}%`")
        else:
            st.error("❌ Something went wrong. Try again.")
