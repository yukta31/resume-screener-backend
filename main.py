from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import io
from pypdf import PdfReader
import json
import re
import os
from groq import Groq

app = FastAPI(title="AI Resume Screener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
# Set GROQ_API_KEY in your environment variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def analyze_with_groq(resume_text: str, job_description: str) -> dict:
    """Send resume + JD to Groq LLM for analysis."""
    
    prompt = f"""You are an expert AI resume screener and career coach. Analyze the following resume against the job description and provide a detailed, structured assessment.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

Provide your analysis in the following EXACT JSON format (no other text, just the JSON):
{{
  "overall_score": <integer 0-100>,
  "match_level": "<Excellent|Strong|Good|Fair|Weak>",
  "summary": "<2-3 sentence overall assessment>",
  "skills_match": {{
    "matched": ["<skill1>", "<skill2>", ...],
    "missing": ["<skill1>", "<skill2>", ...],
    "score": <integer 0-100>
  }},
  "experience_match": {{
    "assessment": "<assessment text>",
    "score": <integer 0-100>
  }},
  "strengths": [
    {{"title": "<strength title>", "detail": "<explanation>"}},
    {{"title": "<strength title>", "detail": "<explanation>"}},
    {{"title": "<strength title>", "detail": "<explanation>"}}
  ],
  "gaps": [
    {{"title": "<gap title>", "detail": "<explanation>", "priority": "<High|Medium|Low>"}},
    {{"title": "<gap title>", "detail": "<explanation>", "priority": "<High|Medium|Low>"}}
  ],
  "improvements": [
    {{"action": "<specific action to take>", "impact": "<High|Medium|Low>"}},
    {{"action": "<specific action to take>", "impact": "<High|Medium|Low>"}},
    {{"action": "<specific action to take>", "impact": "<High|Medium|Low>"}}
  ],
  "ats_keywords_missing": ["<keyword1>", "<keyword2>", "<keyword3>"],
  "verdict": "<one sentence hiring recommendation>"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000,
    )
    
    raw = response.choices[0].message.content.strip()
    
    # Extract JSON from response
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    raise ValueError("Could not parse AI response as JSON")

@app.get("/")
def root():
    return {"status": "AI Resume Screener API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Analyze a resume against a job description."""
    
    # Validate file type
    if not resume.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Validate JD length
    if len(job_description.strip()) < 50:
        raise HTTPException(status_code=400, detail="Job description is too short")
    
    try:
        # Read and parse PDF
        file_bytes = await resume.read()
        resume_text = extract_text_from_pdf(file_bytes)
        
        if len(resume_text) < 100:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Analyze with Groq
        result = analyze_with_groq(resume_text, job_description)
        
        return JSONResponse(content={
            "success": True,
            "data": result
        })
        
    except HTTPException:
        raise
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI response parsing failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
