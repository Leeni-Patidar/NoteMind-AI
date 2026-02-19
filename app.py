import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

import streamlit as st
from agents.crew_setup import run_notes, run_questions
from auth.google_auth import google_login

st.set_page_config(page_title="AI Education System", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

.top-bar {
    display: flex;
    justify-content: flex-end;
}

.title {
    text-align: center;
    font-size: 32px;
    font-weight: 600;
    margin-top: 100px;
    margin-bottom: 20px;
}

.chat-box {
    max-width: 700px;
    margin: auto;
}

.user {
    background-color: #DCF8C6;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
    text-align: right;
}

.bot {
    background-color: #F1F0F0;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
}

.stTextInput > div > div > input {
    font-size: 16px;
    padding: 12px;
}

</style>
""", unsafe_allow_html=True)


# ---------- SESSION ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------- TOP BAR LOGIN ----------
col1, col2 = st.columns([8,1])

with col2:
    auth_url = google_login()
    st.link_button("Login with Google", auth_url)


# ---------- TITLE ----------
st.markdown('<div class="title">What’s in your mind today?</div>', unsafe_allow_html=True)


# ---------- CHAT DISPLAY ----------
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.messages:

    if msg["role"] == "user":
        st.markdown(
            f'<div class="user">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f'<div class="bot">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)


# ---------- INPUT ----------
user_input = st.text_input(
    "Message",
    placeholder="Ask anything...",
    label_visibility="collapsed"
)


# ---------- BUTTONS ----------
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Notes", use_container_width=True):

        if user_input:

            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            with st.spinner("Generating Notes..."):
                response = run_notes(user_input, "Detailed Notes")

            st.session_state.messages.append(
                {"role": "bot", "content": response}
            )

            st.rerun()


with col2:
    if st.button("Generate Questions", use_container_width=True):

        if user_input:

            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            with st.spinner("Generating Questions..."):
                response = run_questions(user_input, "MCQs", 10)

            st.session_state.messages.append(
                {"role": "bot", "content": response}
            )

            st.rerun()
