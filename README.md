# 🧠 InsightAI — AI Assistant Feedback & Evaluation Platform

InsightAI is an independent chatbot feedback and response-evaluation application built with Python and Streamlit. Users ask questions, review AI responses, rate answer quality, submit comments, and explore feedback analytics.

## Features
- AI assistant with optional Google Gemini API integration.
- Demo response mode without an API key, so the feedback workflow can be tested immediately.
- 1–5 star ratings, helpfulness selection, feedback categories and comments.
- SQLite storage for conversations and feedback.
- Lightweight positive/neutral/negative sentiment estimation.
- Dashboard with interaction count, feedback count, average rating, low ratings and sentiment breakdown.
- Feedback explorer, CSV export and response evaluation history.

## Technology
Python · Streamlit · SQLite · Google Gemini REST API (optional) · Python standard library.

## Project structure
```text
InsightAI/
├── app.py
├── src/
│   ├── __init__.py
│   ├── ai.py
│   ├── analytics.py
│   ├── database.py
│   └── sentiment.py
├── data/.gitkeep
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Run on Windows
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```
If PowerShell blocks activation, use the environment executable directly:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app.py
```

## Enable Gemini (optional)
Set environment variables in the same terminal before launching Streamlit:
```powershell
$env:GOOGLE_API_KEY="your_actual_api_key"
$env:GEMINI_MODEL="gemini-2.0-flash"
```
You can obtain an API key through Google AI Studio. Never commit a real key to GitHub. Without a key, InsightAI runs in demo mode and all feedback features remain usable.

For Streamlit Community Cloud, add these to App → Settings → Secrets:
```toml
GOOGLE_API_KEY = "your_actual_api_key"
GEMINI_MODEL = "gemini-2.0-flash"
```

## Deploy
Push this repository to GitHub, then create an app at https://share.streamlit.io/ using branch `main` and main file `app.py`. Add Gemini secrets only if live responses are required.

## Feedback workflow
1. Ask a question in AI Assistant.
2. Review the generated answer.
3. Rate it from 1–5, indicate helpfulness, select a category and optionally comment.
4. Review aggregate patterns in Overview and individual records in Feedback Explorer.
5. Export collected feedback as CSV.

## Limitations and responsible use
- Educational prototype, not a production AI quality assurance service.
- Sentiment analysis is a small keyword heuristic and can misread negation, sarcasm and context.
- User ratings are subjective signals, not proof of factual correctness.
- Gemini can produce inaccurate content; verify important answers independently.
- Do not submit confidential, medical, financial or authentication information.
- Local SQLite storage is suitable for a demo; hosted ephemeral storage may reset. Use a managed database for persistent multi-user deployment.

## Future improvements
- Evaluation rubric for factuality, relevance, clarity and completeness.
- Multi-model comparison, user authentication, persistent hosted database and automated tests.
