import streamlit as st

# Page setup
st.set_page_config(
    page_title="SmartNotes AI",
    page_icon="📚",
    layout="wide"
)

# ========== HEADER ==========
col1, col2 = st.columns([8, 1])

with col1:
    st.markdown("### 🤖 SmartNotes AI")

with col2:
    if st.button("Login 🔐"):
        st.info("Login system coming soon")

# Divider
st.divider()

# ========== SIDEBAR ==========
st.sidebar.title("📝 Notes Type")

note_type = st.sidebar.radio(
    "Choose format",
    [
        "📘 Short Notes",
        "📖 Detailed Notes",
        "🧠 Exam Revision",
        "📊 Bullet Points",
        "🎯 Interview Prep"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Select note style before generating")

# ========== CENTER UI ==========
st.markdown(
    """
    <style>
        .center-title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-top: 50px;
        }
        .subtitle {
            text-align: center;
            color: gray;
            margin-bottom: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="center-title">AI Study Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate smart notes in seconds</div>', unsafe_allow_html=True)

# Input
topic = st.text_input("", placeholder="Enter topic like Machine Learning, OS, DBMS...")

# Generate button
if st.button("Generate Notes 🚀"):
    if topic:
        st.success(f"Generating {note_type} for: {topic}")

        # Example output
        st.markdown("### 📚 Generated Notes")
        st.write(f"**Topic:** {topic}")
        st.write(f"**Format:** {note_type}")
        st.write("👉 Your AI generated content will appear here...")

    else:
        st.warning("Please enter a topic")


