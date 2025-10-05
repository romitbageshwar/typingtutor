import streamlit as st
import time
import threading

# --- PAGE CONFIG ---
st.set_page_config(page_title="Typing Tutor Pro", page_icon="⌨️", layout="wide")

# --- INITIAL STATE ---
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""
if "finished" not in st.session_state:
    st.session_state.finished = False
if "time_left" not in st.session_state:
    st.session_state.time_left = 420  # 7 minutes
if "passage" not in st.session_state:
    st.session_state.passage = ""
if "running" not in st.session_state:
    st.session_state.running = False

# --- PASSAGE BANKS ---
passages_30 = [
    """Typing is one of the most useful skills in the digital world. Whether you are a student, an employee, or simply someone who spends time on a computer, the ability to type quickly and accurately saves valuable time.

The key to success is consistency. Practicing every day, even for a few minutes, builds strong muscle memory. Soon, your fingers will find their positions without you having to think. It’s also important to maintain good posture while typing. Keep your back straight, wrists relaxed, and monitor at eye level. These small adjustments prevent fatigue and make your typing sessions more productive.""",
    """Learning to type effectively can open many doors in today’s technology-driven world. When you can type efficiently, you can write emails faster, take notes more accurately, and express your ideas without interruption.

Typing practice doesn’t have to be boring. You can type song lyrics, book passages, or even your own stories. The goal is to keep your fingers moving and your eyes focused on the screen. Over time, your hands will memorize the keyboard layout, and typing will become as natural as speaking.""",
    """Touch typing is the art of typing without looking at the keyboard. It might seem difficult at first, but it’s one of the most rewarding skills you can learn. The trick is to position your fingers correctly and trust your memory. At first, you may make mistakes, but that’s a normal part of the learning process.

A steady typing speed of around thirty words per minute is a great goal for beginners. Focus on building accuracy and rhythm before you chase higher speeds."""
]

passages_40 = [
    """Typing at forty words per minute marks a comfortable intermediate level. At this stage, your focus should shift toward endurance and smoothness. Being able to maintain a steady pace for several minutes without errors is more valuable than reaching higher speeds temporarily.

To develop this control, try typing longer passages. Don’t rush—focus on breathing and keeping your rhythm steady. By maintaining consistency, you’ll soon be able to type entire documents effortlessly.""",
    """Many people think that typing fast is just about moving fingers quickly, but true speed comes from accuracy and anticipation. Skilled typists think several words ahead of their hands. Their fingers simply follow a rhythm that the brain sets.

To achieve this, practice with texts you find interesting. Typing something you enjoy keeps your attention high and helps you retain the correct movements.""",
    """Typing efficiently is not about racing—it’s about flow. A calm typist is a fast typist. When you stay relaxed, your accuracy improves and your brain processes text more fluidly.

Try to make typing part of your daily routine. A few minutes each day keeps your progress steady and sustainable."""
]

# --- LEVELS ---
levels = {"30 WPM": passages_30, "40 WPM": passages_40}

# --- SIDEBAR ---
st.sidebar.header("⚙️ Settings")
level = st.sidebar.selectbox("Choose Level", list(levels.keys()))
passage_index = st.sidebar.selectbox("Choose Passage", [f"Passage {i+1}" for i in range(len(levels[level]))])
st.session_state.passage = levels[level][int(passage_index.split()[-1]) - 1]

# --- HEADER ---
st.title("⌨️ Typing Tutor (7-Minute Test)")
st.caption("Focus on accuracy and rhythm. Timer runs live!")

# --- START BUTTONS ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("▶️ Start Test"):
        st.session_state.start_time = time.time()
        st.session_state.time_left = 420
        st.session_state.finished = False
        st.session_state.running = True
        st.session_state.typed_text = ""
        st.rerun()
with col2:
    if st.button("🔄 Restart"):
        st.session_state.start_time = None
        st.session_state.typed_text = ""
        st.session_state.finished = False
        st.session_state.time_left = 420
        st.session_state.running = False
        st.rerun()
with col3:
    if st.button("✅ Submit"):
        st.session_state.finished = True
        st.session_state.running = False
        st.rerun()

# --- TIMER + TEST ---
placeholder = st.empty()

if st.session_state.running and not st.session_state.finished:
    start_time = st.session_state.start_time
    passage = st.session_state.passage

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("📖 Passage")
        st.write(passage)

    with col_right:
        st.subheader("✍️ Type Here")
        st.session_state.typed_text = st.text_area(" ", value=st.session_state.typed_text, height=400)

    timer_placeholder = st.empty()

    while st.session_state.time_left > 0 and not st.session_state.finished:
        time.sleep(1)
        elapsed = int(time.time() - start_time)
        st.session_state.time_left = max(0, 420 - elapsed)

        minutes = st.session_state.time_left // 60
        seconds = st.session_state.time_left % 60
        timer_placeholder.markdown(f"### ⏱️ Time Left: {minutes:02d}:{seconds:02d}")

        if st.session_state.time_left <= 0:
            st.session_state.finished = True
            st.session_state.running = False
            st.rerun()

# --- RESULT ---
if st.session_state.finished:
    typed = st.session_state.typed_text
    passage = st.session_state.passage
    correct_chars = sum(1 for i, c in enumerate(typed) if i < len(passage) and c == passage[i])
    total_chars = len(typed)
    accuracy = round((correct_chars / total_chars) * 100, 2) if total_chars > 0 else 0
    words = len(typed.split())
    elapsed = min(420, time.time() - (st.session_state.start_time or time.time()))
    elapsed_minutes = elapsed / 60 if elapsed > 0 else 1
    wpm = round(words / elapsed_minutes)

    st.success(f"✅ Test Completed!\n\n**Speed:** {wpm} WPM | **Accuracy:** {accuracy}% | **Time:** {int(elapsed // 60)}m {int(elapsed % 60)}s")
