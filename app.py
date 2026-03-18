import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

import streamlit as st
from agents.crew_setup import run_notes, run_questions
from auth.google_auth import google_login, get_user_info, logout
from utils.history_manager import save_history, load_history
from tools.docx_export import export_docx


st.set_page_config(page_title="NoteMind AI", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
.block-container {padding-top: 1rem;}
header {visibility: hidden;}
.stApp {background-color: #f8fafc;}

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}

.chat-bubble-user {
    background: #2563eb;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
    text-align: right;
}

.chat-bubble-bot {
    background: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.mode-box {
    background: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #2563eb;
    margin-bottom: 20px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
defaults = {
    "user": None,
    "history": [],
    "chat_history": [],
    "mode": None,
    "pending_action": None,
    "topic_input": "",
    "last_mode": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================= MODE RESET FIX =================
if st.session_state.mode != st.session_state.last_mode:
    st.session_state.pending_action = None
    st.session_state.topic_input = ""
    st.session_state.chat_history = []   # ✅ CLEAR OLD UI
    st.session_state.last_mode = st.session_state.mode

# ================= LOGIN =================
if "user_email" in st.query_params and st.session_state.user is None:
    st.session_state.user = {
        "email": st.query_params["user_email"],
        "name": st.query_params.get("user_name", "User")
    }
    st.session_state.history = load_history(st.session_state.user["email"])

if "code" in st.query_params and st.session_state.user is None:
    user = get_user_info(st.query_params["code"])
    if user:
        st.session_state.user = user
        st.session_state.history = load_history(user["email"])
        st.query_params["user_email"] = user["email"]
        st.query_params["user_name"] = user["name"]
        st.query_params.pop("code")
        st.rerun()

# ================= LANDING PAGE =================
if not st.session_state.user:

    auth_url = google_login()

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        color: white;
    }
    .hero-title {
        font-size: 60px;
        font-weight: 700;
        color: #38bdf8;
    }
    .hero-subtitle {
        font-size: 22px;
        color: #cbd5e1;
        margin-top: 15px;
    }
    .hero-desc {
        color: #94a3b8;
        margin-top: 15px;
        line-height: 1.6;
    }
    .feature-card {
        background: rgba(255,255,255,0.08);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="hero-title">NoteMind AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Multi-Agent Education System</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-desc">Our AI-powered agents generate concise notes, in-depth notes, bullet points, short questions, long questions, and multiple-choice quizzes instantly..</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Custom Styled Login Button
        st.markdown(f"""
        <a href="{auth_url}" target="_self">
            <button class="login-btn">Login with Google</button>
        </a>

        <style>
        .login-btn {{
            background: linear-gradient(145deg, #2563eb, #1d4ed8);
            border: 2px solid #1e40af;
            color: white;
            padding: 12px 28px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .login-btn:hover {{
            background: linear-gradient(145deg, #1d4ed8, #1e40af);
            color: white !important;
            transform: translateY(-2px);
        }}
        </style>
        """, unsafe_allow_html=True)

    with col2:
        image_path = os.path.join(os.getcwd(), "landing_page.png")
        if os.path.exists(image_path):
            st.image(image_path, width=400)
        else:
            st.warning("Place 'landing_page.png' in project root folder.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown('<div class="feature-card"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135755.png" width="60"><br><br><b>Smart Notes</b><br><br>AI agents generate short notes, detailed explanations, and structured bullet points instantly.</div>', unsafe_allow_html=True)

    with f2:
        st.markdown('<div class="feature-card"><img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="60"><br><br><b>AI Question Generator</b><br><br>Automatically creates MCQs, short-answer, and long-answer questions for assessments.</div>', unsafe_allow_html=True)

    with f3:
        st.markdown('<div class="feature-card"><img src="https://cdn-icons-png.flaticon.com/512/4149/4149684.png" width="60"><br><br><b>Multi-Agent System</b><br><br>Specialized AI agents collaborate to deliver accurate, structured, and high-quality results.</div>', unsafe_allow_html=True)
        st.stop()

# ================= TOP BAR =================
col1, col2 = st.columns([10,1])
with col2:
    first_letter = st.session_state.user["email"][0].upper()
    st.markdown(f'<div class="avatar">{first_letter}</div>', unsafe_allow_html=True)



# ================= SIDEBAR =================
def switch_mode(new_mode):
    st.session_state.mode = new_mode
    st.session_state.pending_action = None
    st.session_state.topic_input = ""
    st.rerun()

with st.sidebar:
    st.markdown("## 📘 NoteMind")

    if st.button("➕ New Chat"):
        st.session_state.chat_history = []
        st.session_state.pending_action = None
        st.rerun()

    st.divider()

    if st.button("🧠 Doubt Session"):
        switch_mode("doubt")

    if st.button("📝 Generate Notes"):
        switch_mode("notes")

    if st.button("❓ Generate Questions"):
        switch_mode("questions")

    st.divider()
    st.subheader("History")

    for i, item in enumerate(st.session_state.history[::-1]):
        if st.button(item["query"][:30], key=f"hist_{i}"):
            st.session_state.chat_history.append({
                "user": item["query"],
                "bot": item["result"]
            })
            st.rerun()

    st.divider()
    st.write(f"👤 {st.session_state.user['name']}")

    if st.button("Logout"):
        logout()
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()

# ================= MAIN =================
st.markdown('<div class="main-title">NoteMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">What’s in your mind today?</div>', unsafe_allow_html=True)

# ================= MODE DISPLAY =================
if st.session_state.mode == "doubt":
    st.markdown('<div class="mode-box">🧠 Doubt Session: Ask anything.</div>', unsafe_allow_html=True)

elif st.session_state.mode == "notes":
    st.markdown('<div class="mode-box">📝 Notes Mode</div>', unsafe_allow_html=True)

elif st.session_state.mode == "questions":
    st.markdown('<div class="mode-box">❓ Questions Mode</div>', unsafe_allow_html=True)

else:
    st.warning("⚠️ Select a mode")

# ================= CHAT =================
for chat in st.session_state.chat_history:
    st.markdown(f'<div class="chat-bubble-user">🧑 {chat["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble-bot">🤖 {chat["bot"]}</div>', unsafe_allow_html=True)

# ================= INPUT =================
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.topic_input = user_input

    if st.session_state.mode == "notes":
        st.session_state.pending_action = "notes"
    elif st.session_state.mode == "questions":
        st.session_state.pending_action = "questions"
    elif st.session_state.mode == "doubt":
        st.session_state.pending_action = "doubt"
    else:
        st.warning("Select a mode")
        st.stop()

    st.rerun()

# ================= ACTION UI =================
result = None

if st.session_state.pending_action == "notes":
    st.markdown("### Select Notes Type")
    c1, c2, c3 = st.columns(3)

    if c1.button("Detailed", key="notes_detailed"):
        result = run_notes(st.session_state.topic_input, "Detailed Notes")

    elif c2.button("Short", key="notes_short"):
        result = run_notes(st.session_state.topic_input, "Short Notes")

    elif c3.button("Bullet", key="notes_bullet"):
        result = run_notes(st.session_state.topic_input, "Bullet Points")

elif st.session_state.pending_action == "questions":
    st.markdown("### Select Question Type")
    c1, c2, c3 = st.columns(3)

    if c1.button("MCQ", key="q_mcq"):
        result = run_questions(st.session_state.topic_input, "MCQ", 5)

    elif c2.button("Short", key="q_short"):
        result = run_questions(st.session_state.topic_input, "Short Questions", 5)

    elif c3.button("Long", key="q_long"):
        result = run_questions(st.session_state.topic_input, "Long Questions", 5)

elif st.session_state.pending_action == "doubt":
    with st.spinner("Thinking..."):
        result = run_notes(st.session_state.topic_input, "Detailed Notes")

# ================= SAVE =================
if result:
    st.session_state.chat_history.append({
        "user": st.session_state.topic_input,
        "bot": result
    })

    save_history(
        st.session_state.user["email"],
        st.session_state.topic_input,
        result
    )

    st.session_state.pending_action = None
    st.rerun()

# ================= DOWNLOAD =================
if st.session_state.chat_history:
    last = st.session_state.chat_history[-1]["bot"]
    export_docx(last, "output.docx")

    with open("output.docx", "rb") as f:
        st.download_button("⬇ Download Last Output", f)