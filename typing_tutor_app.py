import streamlit as st
import time
import random

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
    st.session_state.time_left = 420  # 7 minutes (420s)
if "passage" not in st.session_state:
    st.session_state.passage = ""
if "level" not in st.session_state:
    st.session_state.level = "30 WPM"

# --- PASSAGE BANKS ---

passages_30 = [
    """Typing is one of the most useful skills in the digital world. Whether you are a student, an employee, or simply someone who spends time on a computer, the ability to type quickly and accurately saves valuable time. Many people begin by typing slowly, focusing on accuracy over speed. Over time, the mind adapts to the rhythm of the keyboard, and speed begins to increase naturally.

The key to success is consistency. Practicing every day, even for a few minutes, builds strong muscle memory. Soon, your fingers will find their positions without you having to think. It’s also important to maintain good posture while typing. Keep your back straight, wrists relaxed, and monitor at eye level. These small adjustments prevent fatigue and make your typing sessions more productive.""",

    """Learning to type effectively can open many doors in today’s technology-driven world. When you can type efficiently, you can write emails faster, take notes more accurately, and express your ideas without interruption. Accuracy should be your first priority. Once you stop worrying about mistakes, your speed will improve on its own.

Typing practice doesn’t have to be boring. You can type song lyrics, book passages, or even your own stories. The goal is to keep your fingers moving and your eyes focused on the screen. Over time, your hands will memorize the keyboard layout, and typing will become as natural as speaking.""",

    """Touch typing is the art of typing without looking at the keyboard. It might seem difficult at first, but it’s one of the most rewarding skills you can learn. The trick is to position your fingers correctly and trust your memory. At first, you may make mistakes, but that’s a normal part of the learning process.

A steady typing speed of around thirty words per minute is a great goal for beginners. Focus on building accuracy and rhythm before you chase higher speeds. Remember, even professional typists once started with basic exercises and patience.""",

    """The digital world runs on written communication. From messages to documents, typing plays an essential role in daily life. Many people underestimate how much faster and more efficient they can become with a little practice. Typing exercises not only build speed but also improve focus and coordination.

As you type, try to keep your eyes on the screen instead of the keyboard. This technique will strengthen your hand-eye coordination and allow you to catch mistakes more quickly. The more you practice, the more natural your typing will feel.""",

    """Typing well doesn’t happen overnight. It requires daily effort, patience, and consistency. Start with simple words and phrases, then move to longer sentences and paragraphs. The goal is not just to press keys faster but to press the right keys every time.

When you type, your brain and fingers must work together in harmony. This coordination improves over time. Before long, you’ll find yourself typing full pages effortlessly. Remember, slow progress is still progress.""",

    """A good typist values accuracy above all else. While speed can be impressive, accuracy is what ensures professional results. Imagine finishing a page quickly but having to correct dozens of mistakes afterward. That’s why it’s better to type slowly and cleanly.

Once you have mastered accuracy, increasing your speed becomes much easier. Practicing short passages daily and reviewing your mistakes helps you become aware of your weak spots. Gradually, your speed will rise while keeping precision intact.""",

    """Typing tests are a great way to measure your progress. They challenge you to maintain focus under time pressure. At first, the timer might make you nervous, but with experience, you’ll learn to stay calm and type consistently throughout.

A seven-minute test, for example, gives you enough time to find your rhythm. It helps reveal how long you can maintain steady speed and accuracy without fatigue. Consistency matters more than bursts of speed.""",

    """Posture plays a major role in typing efficiency. Poor posture can lead to fatigue, wrist pain, or reduced concentration. Always ensure that your back is straight and your elbows are bent at right angles. Your fingers should rest lightly on the keyboard.

Remember to take breaks. Typing for hours without rest can cause strain on your hands and eyes. Stretch, breathe, and return refreshed for better performance.""",

    """The most successful typists have one thing in common: practice. Even ten minutes of daily typing can make a huge difference. Each session strengthens your familiarity with the keyboard, your sense of rhythm, and your ability to think while typing.

If you ever feel discouraged, remind yourself that improvement takes time. Every key you press brings you closer to mastery. Be patient and persistent, and you’ll soon see progress.""",

    """Typing at a steady pace helps you avoid mistakes. Rushing often leads to errors and unnecessary corrections. When you slow down and focus on precision, your typing naturally becomes smoother and more reliable. Confidence grows from accuracy, not from speed.

Over time, your fingers will learn where every key is without looking. This allows you to focus entirely on your ideas instead of the keyboard. That’s when typing truly becomes a creative tool rather than just a skill."""
]

passages_40 = [
    """Typing at forty words per minute marks a comfortable intermediate level. At this stage, your focus should shift toward endurance and smoothness. Being able to maintain a steady pace for several minutes without errors is more valuable than reaching higher speeds temporarily.

To develop this control, try typing longer passages. Don’t rush—focus on breathing and keeping your rhythm steady. By maintaining consistency, you’ll soon be able to type entire documents effortlessly.""",

    """Many people think that typing fast is just about moving fingers quickly, but true speed comes from accuracy and anticipation. Skilled typists think several words ahead of their hands. Their fingers simply follow a rhythm that the brain sets.

To achieve this, practice with texts you find interesting. Typing something you enjoy keeps your attention high and helps you retain the correct movements.""",

    """Typing efficiently is not about racing—it’s about flow. A calm typist is a fast typist. When you stay relaxed, your accuracy improves and your brain processes text more fluidly.

Try to make typing part of your daily routine. A few minutes each day keeps your progress steady and sustainable.""",

    """Every typist experiences fatigue after a few minutes of intense focus. That’s why professional typists practice pacing. Rather than typing at maximum speed the entire time, they learn to balance bursts of energy with steady control.

During long sessions, proper breathing and posture are essential. Remember: comfort sustains performance.""",

    """To reach higher speeds like forty words per minute and beyond, pay attention to finger placement. The home row keys—A, S, D, F for the left hand and J, K, L, ; for the right—are your foundation. From there, every movement should be quick but minimal.

Avoid unnecessary motion. Smooth, small movements are faster and more accurate than large, rushed ones.""",

    """Speed and accuracy are inseparable. Typing without errors saves time in revisions. That’s why improving accuracy first always leads to better speed later.

Consider timing yourself weekly. Keep a record of your progress—it’s motivating to see your words-per-minute increase while your error rate decreases.""",

    """Modern life demands typing proficiency. From sending messages to writing reports, your hands spend more time on a keyboard than anywhere else. Learning to type quickly gives you a lifelong productivity advantage.

Think of typing practice as an investment in your efficiency. Every second you save while typing adds up over time.""",

    """Good lighting and a quiet environment make typing easier. Distractions break your flow and reduce your accuracy. Whenever possible, practice in a calm space where you can fully focus on the passage in front of you.

Set small goals—maybe just one more accurate paragraph each day. Tiny improvements multiply into big results.""",

    """Advanced typists measure their progress not only in speed but also in endurance. A seven-minute test challenges your ability to stay precise even as fatigue sets in.

If you can maintain accuracy through the full duration, it shows your control and focus are improving steadily.""",

    """Typing should never feel like a chore. Treat it like music—find your rhythm and enjoy the motion. Each keypress is a note, and your flow creates harmony on the keyboard.

When you begin to enjoy typing, your progress accelerates naturally."""
]

# --- LEVEL DICTIONARY ---
levels = {"30 WPM": passages_30, "40 WPM": passages_40}

# --- SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Typing Test Settings")
selected_level = st.sidebar.selectbox("Select Level", list(levels.keys()))
selected_passage = st.sidebar.selectbox("Select Passage", [f"Passage {i+1}" for i in range(len(levels[selected_level]))])

# --- LOAD PASSAGE ---
st.session_state.passage = levels[selected_level][int(selected_passage.split()[-1]) - 1]

# --- HEADER ---
st.title("⌨️ Typing Tutor (Split Screen Edition)")
st.caption("Practice typing for 7 minutes. Focus on accuracy and rhythm.")

# --- START / RESTART BUTTONS ---
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("▶️ Start"):
        st.session_state.start_time = time.time()
        st.session_state.typed_text = ""
        st.session_state.finished = False
        st.session_state.time_left = 420
        st.rerun()

with col2:
    if st.button("🔄 Restart"):
        st.session_state.start_time = None
        st.session_state.typed_text = ""
        st.session_state.finished = False
        st.session_state.time_left = 420
        st.rerun()

# --- MAIN INTERFACE (Split Screen) ---
col_left, col_right = st.columns(2)

if st.session_state.start_time and not st.session_state.finished:
    # TIMER
    elapsed = int(time.time() - st.session_state.start_time)
    st.session_state.time_left = max(0, 420 - elapsed)
    minutes = st.session_state.time_left // 60
    seconds = st.session_state.time_left % 60
    st.markdown(f"### ⏱️ Time Left: {minutes:02d}:{seconds:02d}")

    # LEFT SIDE - PASSAGE
    with col_left:
        st.subheader("📖 Passage")
        st.write(st.session_state.passage)

    # RIGHT SIDE - TYPING BOX
    with col_right:
        st.subheader("✍️ Type Below")
        st.session_state.typed_text = st.text_area(" ", value=st.session_state.typed_text, height=400)

    # STATS
    typed = st.session_state.typed_text
    correct_chars = sum(1 for i, c in enumerate(typed) if i < len(st.session_state.passage) and c == st.session_state.passage[i])
    total_chars = len(typed)
    accuracy = round((correct_chars / total_chars) * 100, 2) if total_chars else 0
    words = len(typed.split())
    elapsed_minutes = elapsed / 60 if elapsed > 0 else 1
    wpm = round(words / elapsed_minutes)

    st.markdown(f"**Speed:** {wpm} WPM | **Accuracy:** {accuracy}%")

    # END CONDITION
    if st.session_state.time_left <= 0 or typed.strip() == st.session_state.passage.strip():
        st.session_state.finished = True
        st.session_state.start_time = None
        st.rerun()

# --- RESULTS ---
if st.session_state.finished:
    typed = st.session_state.typed_text
    correct_chars = sum(1 for i, c in enumerate(typed) if i < len(st.session_state.passage) and c == st.session_state.passage[i])
    total_chars = len(typed)
    accuracy = round((correct_chars / total_chars) * 100, 2) if total_chars else 0
    words = len(typed.split())
    elapsed = 420 - st.session_state.time_left
    elapsed_minutes = elapsed / 60 if elapsed > 0 else 1
    wpm = round(words / elapsed_minutes)
    st.success(f"✅ Test Completed! Speed: {wpm} WPM | Accuracy: {accuracy}% | Time: {int(elapsed // 60)}m {int(elapsed % 60)}s")
