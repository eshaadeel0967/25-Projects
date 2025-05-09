import streamlit as st
from deep_translator import GoogleTranslator
import time
import random

# Initialize session state
if "game_text" not in st.session_state:
    st.session_state.game_text = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Typing Master - Generate Random Text
SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is an amazing programming language.",
    "Streamlit makes building web apps super easy.",
    "Machine learning is the future of AI."
]

def start_typing_game():
    st.session_state.game_text = random.choice(SAMPLE_TEXTS)
    st.session_state.start_time = time.time()
    st.session_state.user_input = ""

def calculate_speed():
    end_time = time.time()
    time_taken = end_time - st.session_state.start_time
    words = len(st.session_state.user_input.split())
    speed = words / (time_taken / 60)
    return round(speed, 2)

# Streamlit App UI
st.title("Mad Libs & Typing Master Game 🎭⌨️")

# Section 1: Mad Libs
st.header("📝 Mad Libs Story Generator")
verb = st.text_input("Enter a verb:")
noun = st.text_input("Enter a noun:")
adjective = st.text_input("Enter an adjective:")
if st.button("Generate Story"):
    story = f"Once upon a time, a {adjective} {noun} decided to {verb} all day long."
    st.success(story)
    
    # Translation Feature
    lang = st.selectbox("Translate story to:", ["French", "Spanish", "German", "Urdu"])
    lang_code = {"French": "fr", "Spanish": "es", "German": "de", "Urdu": "ur"}
    translated_story = GoogleTranslator(source='auto', target=lang_code[lang]).translate(story)
    st.write(f"**Translated Story ({lang}):** {translated_story}")

# Section 2: Typing Master Game
st.header("⌨️ Typing Master Challenge")
if st.button("Start Typing Test"):
    start_typing_game()

if st.session_state.game_text:
    st.subheader("Type this as fast as you can:")
    st.write(f"*{st.session_state.game_text}*")
    user_typing = st.text_area("Start typing:", value=st.session_state.user_input, height=100)
    st.session_state.user_input = user_typing
    
    if st.button("Check Speed"):
        if st.session_state.user_input.strip() == st.session_state.game_text.strip():
            speed = calculate_speed()
            st.success(f"Great job! Your typing speed is {speed} words per minute.")
        else:
            st.error("Oops! Your typed text doesn't match exactly. Try again!")

st.write("🔹 Developed by Esha using Streamlit")