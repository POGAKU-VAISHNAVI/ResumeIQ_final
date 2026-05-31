# ResumeIQ — AI Resume Assistant

## Project Structure
```
ResumeIQ/
├── backend/
│   ├── app.py              ← Main Flask server (run this)
│   ├── auth.py             ← Signup / Login / Logout
│   ├── resume_parser.py    ← PDF text extraction
│   ├── validator.py        ← Resume validation
│   ├── skill_detector.py   ← Skills gap analysis
│   ├── scorer.py           ← Resume scoring
│   ├── job_matcher.py      ← JD matching
│   └── requirements.txt    ← Python dependencies
├── frontend/
│   ├── pages/
│   │   ├── analyze.html    ← Main analyzer page
│   │   ├── home.html       ← Landing page
│   │   ├── login.html      ← Login page
│   │   ├── signup.html     ← Sign up page
│   │   └── forgot-password.html
│   └── js/
│       └── auth.js         ← Frontend auth helper
└── uploads/                ← PDF uploads stored here
```

## How to Run

### 1. Install Python dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the backend
```bash
python app.py
```
Backend runs at: http://localhost:5000

### 3. Open the frontend
Open `frontend/pages/analyze.html` directly in your browser,
OR use VS Code Live Server (right-click → Open with Live Server).

> The backend must be running for full AI analysis.
> Without the backend, the app runs in demo mode automatically.
