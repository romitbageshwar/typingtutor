import streamlit as st
import time
import random

st.set_page_config(page_title="Typing Tutor Pro", page_icon="⌨️", layout="centered")

# --- Initialize session state ---
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""
if "finished" not in st.session_state:
    st.session_state.finished = False
if "time_left" not in st.session_state:
    st.session_state.time_left = 420  # 7 minutes in seconds
if "passage" not in st.session_state:
    st.session_state.passage = ""
if "level" not in st.session_state:
    st.session_state.level = "30 WPM"

# --- Passage library ---
passages_30 = [
    "The cat chased the mouse across the garden before it escaped under the fence.",
    "Typing slowly but accurately helps build strong muscle memory and confidence.",
]
passages_40 = [
    "Practicing regularly at a steady pace is key to improving both speed and accuracy.",
    "A quick brown fox jumps over the lazy dog to test all the letters of the alphabet.",
]
passages_50 = [
    "Typing at fifty words per minute requires consistent focus and rhythm over time.",
    "Good posture and hand placement reduce fatigue and make long typing sessions easier.",
]
passages_60 = [
    "Experienced typists rely on pattern recognition and anticipation to reach higher speeds.",
    "Accuracy must always come before speed to prevent forming bad habits during typing practice.",
]

levels = {
    "30 WPM": passages_30,
    "40 WPM": passages_40,
    "50 WPM": passages_50,
    "60 WPM": passages_60,
}

# --- Sidebar controls ---
st.sidebar.header("⚙️ Test Settings")
selected_level = st.sidebar.selectbox("Typing Level:", list(levels.keys()), index=list(levels.keys()).index(st.session_state.level))

if selected_level != st.session_state.level:
    st.session_state.level = selected_level
    st.session_state.passage = ""
    st.session_state.typed_text = ""
    st.session_state.finished = False
    st.session_state.start_time = None
    st.session_state.time_left = 420

st.title("⌨️ Typing Tutor Pro")
st.markdown("Improve your typing speed and accuracy with timed challenges.")

# --- Load passage ---
if not st.session_state.passage:
    st.session_state.passage = random.choice(levels[st.session_state.level])

st.markdown(f"### Passage for **{st.session_state.level}**:")
st.markdown(f"> {st.session_state.passage}")

# --- Start / Restart buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Test"):
        st.session_state.start_time = time.time()
        st.session_state.typed_text = ""
        st.session_state.finished = False
        st.session_state.time_left = 420
        st.rerun()

with col2:
    if st.button("Restart"):
        st.session_state.start_time = None
        st.session_state.typed_text = ""
        st.session_state.finished = False
        st.session_state.time_left = 420
        st.rerun()

# --- Main test logic ---
if st.session_state.start_time and not st.session_state.finished:
    elapsed = int(time.time() - st.session_state.start_time)
    st.session_state.time_left = max(0, 420 - elapsed)

    minutes = st.session_state.time_left // 60
    seconds = st.session_state.time_left % 60
    st.markdown(f"### ⏱️ Time left: {minutes:02d}:{seconds:02d}")

    st.session_state.typed_text = st.text_area("✍️ Type here:", value=st.session_state.typed_text, height=150)

    # Calculate stats live
    typed = st.session_state.typed_text
    correct_chars = sum(1 for i, c in enumerate(typed) if i < len(st.session_state.passage) and c == st.session_state.passage[i])
    total_chars = len(typed)
    accuracy = round((correct_chars / total_chars) * 100, 2) if total_chars else 0
    words = len(typed.split())
    elapsed_minutes = elapsed / 60 if elapsed > 0 else 1
    wpm = round(words / elapsed_minutes)

    st.markdown(f"**Speed:** {wpm} WPM | **Accuracy:** {accuracy}%")

    # --- End conditions ---
    if st.session_state.time_left <= 0 or typed.strip() == st.session_state.passage.strip():
        st.session_state.finished = True
        st.session_state.start_time = None

# --- Show result popup ---
if st.session_state.finished:
    st.success("✅ Test Completed!")
    typed = st.session_state.typed_text
    correct_chars = sum(1 for i, c in enumerate(typed) if i < len(st.session_state.passage) and c == st.session_state.passage[i])
    total_chars = len(typed)
    accuracy = round((correct_chars / total_chars) * 100, 2) if total_chars else 0
    words = len(typed.split())
    elapsed = 420 - st.session_state.time_left
    elapsed_minutes = elapsed / 60 if elapsed > 0 else 1
    wpm = round(words / elapsed_minutes)
    st.info(f"""
    ### 🧾 Your Results:
    - **Typing Level:** {st.session_state.level}
    - **Speed:** {wpm} WPM  
    - **Accuracy:** {accuracy}%  
    - **Time Used:** {int(elapsed // 60)} min {int(elapsed % 60)} sec
    """)
