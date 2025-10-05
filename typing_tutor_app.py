import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Typing Tutor", page_icon="⌨️", layout="centered")

# --- INIT SESSION STATE ---
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""
if "finished" not in st.session_state:
    st.session_state.finished = False

# --- PASSAGES ---
passages = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing practice helps improve speed and accuracy.",
    "Streamlit makes Python web apps simple and powerful.",
]
passage = st.selectbox("Choose a passage:", passages)

# --- HEADER ---
st.title("⌨️ Online Typing Tutor")
st.write("Type the passage below as quickly and accurately as possible!")

st.markdown(f"### 📖 Passage:")
st.markdown(f"> {passage}")

# --- BUTTONS ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Test"):
        st.session_state.start_time = time.time()
        st.session_state.typed_text = ""
        st.session_state.finished = False
        st.rerun()

with col2:
    if st.button("Restart"):
        st.session_state.start_time = None
        st.session_state.typed_text = ""
        st.session_state.finished = False
        st.rerun()

# --- MAIN LOGIC ---
if st.session_state.start_time:
    st.session_state.typed_text = st.text_area(
        "✍️ Type here:",
        value=st.session_state.typed_text,
        height=150,
        key="typing_box",
    )

    # --- CALCULATE STATS ---
    elapsed = time.time() - st.session_state.start_time
    words = len(st.session_state.typed_text.split())
    wpm = round((words / elapsed) * 60) if elapsed > 0 else 0

    typed = st.session_state.typed_text
    correct_chars = sum(1 for i, c in enumerate(typed) if i < len(passage) and c == passage[i])
    total_chars = len(typed)
    accuracy = round((correct_chars / total_chars) * 100, 2) if total_chars > 0 else 0

    st.markdown(f"**🕒 Time:** {int(elapsed)}s | **💨 Speed:** {wpm} WPM | **🎯 Accuracy:** {accuracy}%")

    # --- FINISH CHECK ---
    if typed.strip() == passage.strip():
        st.success(f"✅ Finished! Speed: {wpm} WPM | Accuracy: {accuracy}% | Time: {int(elapsed)}s")
        st.session_state.finished = True
        st.session_state.start_time = None
