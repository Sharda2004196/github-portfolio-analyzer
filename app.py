import streamlit as st
import requests
import json
from groq import Groq

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GitHub Portfolio Analyzer | JSO",
    page_icon="🔍",
    layout="centered"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0d1117; }
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3 { color: #58a6ff !important; }
    .score-box {
        background: linear-gradient(135deg, #1f2937, #111827);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    .score-number {
        font-size: 52px;
        font-weight: 800;
        color: #58a6ff;
    }
    .tag {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        margin: 3px;
        display: inline-block;
        color: #8b949e;
    }
    .section-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 10px 0;
    }
    .stTextInput > div > div > input {
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
        color: #c9d1d9 !important;
        border-radius: 8px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #238636, #2ea043);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
        font-size: 16px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2ea043, #3fb950);
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("# 🔍 GitHub Portfolio Analyzer")
st.markdown("##### Powered by JSO — Career Intelligence System")
st.markdown("---")
st.markdown("Paste any public GitHub repository URL and get an **AI-powered evaluation** of code quality, project complexity, and portfolio score.")

# ─── Helper: Fetch GitHub Data ───────────────────────────────────────────────
def fetch_github_data(repo_url: str):
    """Extract owner/repo from URL and fetch data from GitHub API."""
    repo_url = repo_url.strip().rstrip("/")
    parts = repo_url.replace("https://github.com/", "").replace("http://github.com/", "").split("/")
    if len(parts) < 2:
        return None, "Invalid GitHub URL. Please use format: https://github.com/username/repo"

    owner, repo = parts[0], parts[1]
    headers = {"Accept": "application/vnd.github.v3+json"}

    # Repo info
    repo_res = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
    if repo_res.status_code != 200:
        return None, f"Repository not found or is private. (Status: {repo_res.status_code})"
    repo_data = repo_res.json()

    # Languages
    lang_res = requests.get(f"https://api.github.com/repos/{owner}/{repo}/languages", headers=headers)
    languages = lang_res.json() if lang_res.status_code == 200 else {}

    # Recent commits
    commits_res = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=10", headers=headers
    )
    commits = commits_res.json() if commits_res.status_code == 200 else []
    commit_messages = [c["commit"]["message"][:80] for c in commits if isinstance(c, dict)] if commits else []

    # Contents (root files)
    contents_res = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contents", headers=headers)
    contents = contents_res.json() if contents_res.status_code == 200 else []
    file_names = [f["name"] for f in contents if isinstance(f, dict)] if isinstance(contents, list) else []

    summary = {
        "name": repo_data.get("name", ""),
        "description": repo_data.get("description", "No description provided"),
        "stars": repo_data.get("stargazers_count", 0),
        "forks": repo_data.get("forks_count", 0),
        "watchers": repo_data.get("watchers_count", 0),
        "open_issues": repo_data.get("open_issues_count", 0),
        "default_branch": repo_data.get("default_branch", "main"),
        "created_at": repo_data.get("created_at", "")[:10],
        "updated_at": repo_data.get("updated_at", "")[:10],
        "size_kb": repo_data.get("size", 0),
        "has_readme": "README.md" in file_names or "readme.md" in file_names,
        "has_license": "LICENSE" in file_names or "LICENSE.md" in file_names,
        "has_requirements": any("requirement" in f.lower() or f in ["package.json", "Pipfile", "pyproject.toml"] for f in file_names),
        "has_tests": any("test" in f.lower() for f in file_names),
        "languages": languages,
        "root_files": file_names[:20],
        "recent_commits": commit_messages[:5],
        "topics": repo_data.get("topics", []),
        "homepage": repo_data.get("homepage", ""),
        "owner": owner,
        "repo": repo,
    }
    return summary, None


# ─── Helper: Analyze with Groq ──────────────────────────────────────────────
def analyze_with_groq(repo_summary: dict, api_key: str):
    """Send repo data to Groq and get structured analysis."""
    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert technical recruiter and senior software engineer.
Analyze the following GitHub repository data and provide a structured portfolio evaluation.

REPOSITORY DATA:
{json.dumps(repo_summary, indent=2)}

Respond ONLY in valid JSON format with this exact structure:
{{
  "overall_score": <integer 0-100>,
  "grade": "<A+/A/B+/B/C+/C/D>",
  "summary": "<2-3 sentence overview of the project>",
  "scores": {{
    "code_quality": <integer 0-100>,
    "documentation": <integer 0-100>,
    "project_complexity": <integer 0-100>,
    "maintainability": <integer 0-100>,
    "portfolio_value": <integer 0-100>
  }},
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"],
  "recruiter_verdict": "<What a recruiter would think seeing this repo>",
  "tech_stack": ["<tech1>", "<tech2>", "<tech3>"],
  "seniority_level": "<Junior/Mid-level/Senior>",
  "hire_recommendation": "<Strong Yes / Yes / Maybe / No>"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1200,
    )

    raw = response.choices[0].message.content.strip()
    # Clean up potential markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ─── Score Color Helper ──────────────────────────────────────────────────────
def score_color(score):
    if score >= 80: return "#3fb950"
    if score >= 60: return "#d29922"
    return "#f85149"


# ─── Main UI ─────────────────────────────────────────────────────────────────
with st.container():
    repo_url = st.text_input(
        "🔗 GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        label_visibility="visible"
    )
    api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        placeholder="Get free key at console.groq.com",
        label_visibility="visible"
    )
    st.caption("Your API key is never stored. Get a free key at [console.groq.com](https://console.groq.com)")

    analyze_btn = st.button("🚀 Analyze Repository")

if analyze_btn:
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
    elif not api_key:
        st.error("Please enter your Groq API key.")
    else:
        # Step 1: Fetch GitHub data
        with st.spinner("🔍 Fetching repository data from GitHub..."):
            repo_data, error = fetch_github_data(repo_url)

        if error:
            st.error(f"❌ {error}")
        else:
            # Step 2: Analyze with Groq
            with st.spinner("🤖 Analyzing with AI..."):
                try:
                    result = analyze_with_groq(repo_data, api_key)
                except Exception as e:
                    st.error(f"❌ AI analysis failed: {str(e)}")
                    st.stop()

            st.success("✅ Analysis Complete!")
            st.markdown("---")

            # ── Repo Info ────────────────────────────────────────────────────
            st.markdown(f"### 📦 {repo_data['name']}")
            st.markdown(f"*{repo_data['description']}*")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("⭐ Stars", repo_data["stars"])
            col2.metric("🍴 Forks", repo_data["forks"])
            col3.metric("📁 Size", f"{repo_data['size_kb']} KB")
            col4.metric("🐛 Issues", repo_data["open_issues"])

            # Topics / tags
            if repo_data["topics"]:
                tags_html = "".join([f'<span class="tag">{t}</span>' for t in repo_data["topics"]])
                st.markdown(tags_html, unsafe_allow_html=True)

            st.markdown("---")

            # ── Overall Score ────────────────────────────────────────────────
            score = result.get("overall_score", 0)
            grade = result.get("grade", "N/A")
            color = score_color(score)

            st.markdown(f"""
            <div class="score-box">
                <div style="color:#8b949e; font-size:14px; margin-bottom:4px;">OVERALL PORTFOLIO SCORE</div>
                <div class="score-number" style="color:{color};">{score}<span style="font-size:24px">/100</span></div>
                <div style="font-size:28px; font-weight:700; color:{color};">Grade: {grade}</div>
                <div style="color:#8b949e; margin-top:8px; font-size:13px;">
                    Seniority: <b style="color:#c9d1d9">{result.get("seniority_level","N/A")}</b> &nbsp;|&nbsp;
                    Hire Recommendation: <b style="color:#c9d1d9">{result.get("hire_recommendation","N/A")}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Sub Scores ───────────────────────────────────────────────────
            st.markdown("### 📊 Detailed Scores")
            scores = result.get("scores", {})
            score_labels = {
                "code_quality": "🧹 Code Quality",
                "documentation": "📄 Documentation",
                "project_complexity": "🧠 Project Complexity",
                "maintainability": "🔧 Maintainability",
                "portfolio_value": "💼 Portfolio Value"
            }
            for key, label in score_labels.items():
                val = scores.get(key, 0)
                c = score_color(val)
                col_a, col_b = st.columns([3, 1])
                col_a.markdown(f"**{label}**")
                col_b.markdown(f"<span style='color:{c}; font-weight:700; font-size:18px'>{val}/100</span>", unsafe_allow_html=True)
                st.progress(val / 100)

            # ── Summary ──────────────────────────────────────────────────────
            st.markdown("### 💬 AI Summary")
            st.markdown(f"""<div class="section-card">{result.get("summary", "")}</div>""", unsafe_allow_html=True)

            # ── Strengths & Improvements ─────────────────────────────────────
            col_s, col_i = st.columns(2)
            with col_s:
                st.markdown("### ✅ Strengths")
                for s in result.get("strengths", []):
                    st.markdown(f"- {s}")
            with col_i:
                st.markdown("### 🔧 Improvements")
                for imp in result.get("improvements", []):
                    st.markdown(f"- {imp}")

            # ── Recruiter Verdict ────────────────────────────────────────────
            st.markdown("### 👔 Recruiter Verdict")
            st.info(result.get("recruiter_verdict", ""))

            # ── Tech Stack ───────────────────────────────────────────────────
            st.markdown("### 🛠️ Tech Stack Detected")
            tech = result.get("tech_stack", [])
            if tech:
                tags_html = "".join([f'<span class="tag">{t}</span>' for t in tech])
                st.markdown(tags_html, unsafe_allow_html=True)

            st.markdown("---")
            st.caption("Powered by JSO Career Intelligence System • Built with Groq LLaMA3-70B + GitHub API")
