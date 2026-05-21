# AI Resume Screener — Backend

FastAPI backend for the AI Resume Screener. Parses PDF resumes, sends them to Groq's LLaMA 3.3 with a structured prompt, and returns a detailed JSON analysis including match score, skill gaps, ATS keywords, and actionable improvements.

🌐 **Live Demo:** [resume-screener-frontend-flame.vercel.app](https://resume-screener-frontend-flame.vercel.app)  
⚙️ **API Base:** [resume-screener-backend-7atk.onrender.com](https://resume-screener-backend-7atk.onrender.com)  
🖥️ **Frontend Repo:** [resume-screener-frontend](https://github.com/yukta31/resume-screener-frontend)

---

## 🤖 What It Does

Upload a resume PDF + paste a job description → the API returns:

- **Overall match score** (0–100) with match level (Excellent/Strong/Good/Fair/Weak)
- **Skills analysis** — matched skills vs missing skills with percentage score
- **Experience match** — assessment + score
- **Strengths** — top 3 strengths with explanations
- **Gaps** — identified gaps with priority levels (High/Medium/Low)
- **Action plan** — specific improvement actions with impact ratings
- **Missing ATS keywords** — keywords in JD not found in resume
- **Verdict** — one-sentence hiring recommendation

---

## 🔧 Tech Stack

- **Framework:** FastAPI
- **AI Model:** Groq LLaMA 3.3-70b-versatile
- **PDF Parsing:** pypdf
- **Deployment:** Render (free tier)
- **Language:** Python 3

---

## 📡 API Endpoints

### `GET /`
Health check — returns API status.

### `GET /health`
Returns `{"status": "healthy"}`

### `POST /analyze`
Analyze a resume against a job description.

**Request:** `multipart/form-data`
- `resume` — PDF file
- `job_description` — string (min 50 characters)

**Response:**
```json
{
  "success": true,
  "data": {
    "overall_score": 85,
    "match_level": "Strong",
    "summary": "...",
    "skills_match": {
      "matched": ["Python", "FastAPI", "AWS"],
      "missing": ["Kubernetes", "Terraform"],
      "score": 78
    },
    "experience_match": { "assessment": "...", "score": 80 },
    "strengths": [{ "title": "...", "detail": "..." }],
    "gaps": [{ "title": "...", "detail": "...", "priority": "High" }],
    "improvements": [{ "action": "...", "impact": "High" }],
    "ats_keywords_missing": ["keyword1", "keyword2"],
    "verdict": "Strong candidate — recommend proceeding to interview."
  }
}
```

---

## 🚀 Local Development

```bash
git clone https://github.com/yukta31/resume-screener-backend.git
cd resume-screener-backend

pip install -r requirements.txt

cp .env.example .env
# Add your GROQ_API_KEY to .env

uvicorn main:app --reload --port 8000
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## 🌐 Deploy to Render

1. Fork this repo
2. Create a new Web Service on [render.com](https://render.com)
3. Connect your GitHub repo
4. Add environment variable: `GROQ_API_KEY=your_key_here`
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 📁 Files

| File | Description |
|------|-------------|
| `main.py` | FastAPI app — PDF parsing, Groq API call, JSON response |
| `requirements.txt` | Python dependencies |
| `Procfile` | Render deployment config |
| `.env.example` | Environment variables template |

---

## 👩‍💻 Author

**Yukta Batra** — MS Computer Science, George Mason University

[Portfolio](https://yukta-batra.vercel.app) · [LinkedIn](https://linkedin.com/in/yuktabatra31) · [GitHub](https://github.com/yukta31)
