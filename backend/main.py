# AI-Powered Resume Parser + Job Matcher (Full Web App)

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import spacy
import uvicorn
import fitz  # PyMuPDF
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

app = FastAPI()

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USE_API_KEY = False
VALID_API_KEY = os.getenv("API_KEY", "test123")

# Sample job postings database (mock)
job_postings = [
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Looking for Python, APIs, and SQL experience.",
        "skills": ["python", "api", "sql"]
    },
    {
        "id": 2,
        "title": "Data Analyst",
        "description": "Must know Pandas, Excel, and data visualization.",
        "skills": ["pandas", "excel", "visualization"]
    },
    {
        "id": 3,
        "title": "Machine Learning Engineer",
        "description": "Experience with TensorFlow, PyTorch, and ML pipelines.",
        "skills": ["tensorflow", "pytorch", "ml"]
    }
]

class MatchResult(BaseModel):
    job_id: int
    title: str
    match_score: float


class ResumeResult(BaseModel):
    filename: str
    extracted_skills: List[str]
    matches: List[MatchResult]


def extract_skills(text: str) -> List[str]:
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if token.is_alpha]
    common_skills = [
        "python", "java", "sql", "excel", "pandas", "api", "flask", "django",
        "tensorflow", "pytorch", "ml", "visualization", "data", "javascript"
    ]
    found_skills = list(set(tokens) & set(common_skills))
    return found_skills


def match_jobs(user_skills: List[str]) -> List[MatchResult]:
    matches = []
    for job in job_postings:
        overlap = set(user_skills) & set(job["skills"])
        score = len(overlap) / len(job["skills"])
        if score > 0:
            matches.append(MatchResult(job_id=job["id"], title=job["title"], match_score=round(score, 2)))
    matches.sort(key=lambda x: x.match_score, reverse=True)
    return matches


def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


@app.get("/")
def root():
    return {"message": "🚀 Resume Matcher API is live!"}


@app.post("/upload_resumes")
async def upload_resumes(
    files: List[UploadFile] = File(...),
    job_description: Optional[UploadFile] = File(None),
    job_description_text: Optional[str] = Form(None),
    x_api_key: Optional[str] = Header(None)
):
    if USE_API_KEY and x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    job_skills = None
    if job_description:
        job_bytes = await job_description.read()
        job_text = extract_text_from_pdf(job_bytes) if job_description.filename.endswith(".pdf") else job_bytes.decode("utf-8")
        job_skills = extract_skills(job_text)
    elif job_description_text:
        job_skills = extract_skills(job_description_text)


    results = []
    for file in files:
        content = await file.read()
        text = extract_text_from_pdf(content) if file.filename.endswith(".pdf") else content.decode("utf-8")

        extracted_skills = extract_skills(text)
        matches = match_jobs(extracted_skills, [
            {"id": 0, "title": "Custom Job", "skills": job_skills}
        ]) if job_skills else match_jobs(extracted_skills, job_postings)

        results.append(ResumeResult(
            filename=file.filename,
            extracted_skills=extracted_skills,
            matches=matches
        ))

    return {"results": [r.dict() for r in results]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
