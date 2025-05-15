import streamlit as st
import random

# Custom CSS for beautiful UI
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 10px;
        border-radius: 5px;
    }
    .stMarkdown h2 {
        color: #2c3e50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 Guess The Number Game!")
st.subheader("Can you guess the secret number?")

# Difficulty levels
difficulty = st.radio("Select Difficulty Level:", ["Easy (1-50)", "Medium (1-100)", "Hard (1-200)"])

# Set range based on difficulty
if difficulty == "Easy (1-50)":
    max_number = 50
elif difficulty == "Medium (1-100)":
    max_number = 100
else:
    max_number = 200

# Initialize session state
if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, max_number)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Input for user's guess
user_guess = st.text_input(f"Enter a number between 1 and {max_number}:", "")

# Check user's guess
if st.button("Submit Guess") and not st.session_state.game_over:
    try:
        guess = int(user_guess)
        st.session_state.attempts += 1

        if guess < st.session_state.target_number:
            st.warning("📉 Too low! Try again.")
        elif guess > st.session_state.target_number:
            st.warning("📈 Too high! Try again.")
        else:
            st.session_state.game_over = True
            st.success(f"🎉 Correct! You guessed it in {st.session_state.attempts} attempts.")
            st.balloons()

    except ValueError:
        st.error("❌ Please enter a valid number.")

# Play again button
if st.session_state.game_over:
    if st.button("🔄 Play Again"):
        st.session_state.target_number = random.randint(1, max_number)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.experimental_rerun()

st.write("🔹 Developed by Esha")
