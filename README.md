# 🔍 GitHub Portfolio Analyzer — JSO Career Intelligence System

> An AI-powered agent that evaluates GitHub repositories and generates a portfolio score, recruiter verdict, and improvement recommendations — built for the JSO Agentic AI platform.

![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg) https://portfolio-analyzer-6q9rkqpkozx7xwnfktthomith.streamlit.app

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)

![Groq](https://img.shields.io/badge/Groq-LLaMA3--70B-orange)

![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?logo=streamlit)

![Status](https://img.shields.io/badge/Status-Live-brightgreen)

---

## 📌 Project Overview

This project is a **live AI agent prototype** built as part of the **AariyaTech Agentic JSO — Stage 2 Technical Assignment**.

It addresses the **Code Portfolio Evaluation Agent** task from Part B — helping recruiters automatically evaluate a candidate's GitHub repositories without manual review.

| Detail | Info |
|--------|------|
| **Assignment** | AariyaTech — Agentic AI Engineer Intern |
| **Part** | Part B — Main Task Execution |
| **Focus** | User Dashboard — Code Portfolio Evaluation Agent |
| **AI Model** | LLaMA3-70B via Groq API |
| **Data Source** | GitHub Public REST API |
| **Deployment** | Streamlit Community Cloud (Free) |

---

## 🤖 What the Agent Does

A recruiter or job seeker pastes any **public GitHub repository URL** → the agent fetches live repo data → sends it to an AI model → returns a full evaluation report.

| Output | Description |
|--------|-------------|
| **Overall Score (0–100)** | Composite portfolio quality score |
| **Grade (A+ to D)** | Letter grade based on score |
| **Seniority Level** | Junior / Mid-level / Senior |
| **Hire Recommendation** | Strong Yes / Yes / Maybe / No |
| **Detailed Sub-scores** | Code Quality, Documentation, Complexity, Maintainability, Portfolio Value |
| **Strengths** | What the project does well |
| **Improvements** | Specific actionable suggestions |
| **Recruiter Verdict** | What a hiring manager would think |
| **Tech Stack Detection** | Languages and tools identified |

---

## 🔁 Agent Workflow

```
User pastes GitHub Repo URL
          ↓
GitHub Public API (free)
  → repo info, languages, commits, file structure
          ↓
Groq API — LLaMA3-70B
  → analyzes code quality, complexity, documentation
          ↓
Streamlit Dashboard
  → displays score, grade, verdict, recommendations
```

---

## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| Streamlit | Frontend UI + deployment |
| Groq API (LLaMA3-70B) | AI analysis — free tier |
| GitHub REST API | Live repository data fetching |
| Requests | HTTP calls to APIs |

---

## 📂 Project Structure

```
github-portfolio-analyzer/
├── app.py               ← Main Streamlit application
├── requirements.txt     ← Python dependencies
├── .gitignore           ← Ignore secrets and cache files
└── README.md            ← Project documentation
```

---

## 🚀 How to Run Locally

**1. Clone this repo**
```bash
git clone https://github.com/Sharda2004196/github-portfolio-analyzer.git
cd github-portfolio-analyzer
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Get a free Groq API key**

Go to [console.groq.com](https://console.groq.com) → Sign up → Create API Key → Copy it (no credit card needed)

**4. Run the app**
```bash
streamlit run app.py
```

Opens at `http://localhost:8501` in your browser ✅

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **New App** → Select this repo → Set main file as `app.py`
5. Click **Deploy** ✅

---

## 💡 What This Solves

The current JSO platform faces a key problem — **recruiters cannot easily evaluate GitHub repositories** submitted by technical candidates. Manual code review is time-consuming, inconsistent, and not scalable for high-volume hiring. This agent automates the entire evaluation in under 10 seconds, giving every recruiter a **consistent, AI-backed portfolio score** with zero manual effort.

---

## 🔗 Related Projects

- [Xavier — AI Assistant (n8n Workflow)] https://github.com/Sharda2004196/Xavier-ai-assistant
- [House Price Prediction — ML Regression] https://github.com/Sharda2004196/house-price-prediction

---

## 👤 Author

**Sharda Vatsal Bhat**

Aspiring AI/ML Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/Sharda2004196)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/Sharda2004196)


