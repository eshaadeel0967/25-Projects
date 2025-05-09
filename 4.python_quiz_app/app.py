import streamlit as st
import random

# List of 100 Python MCQs with options and answers
questions = [
    {"question": "What is the output of print(2 ** 3)?", "options": ["5", "6", "8", "10"], "answer": "8", "explanation": "2 ** 3 means 2 raised to the power 3, which is 8."},
    {"question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "function"], "answer": "def", "explanation": "In Python, functions are defined using the 'def' keyword."},
    {"question": "What will print(type([])) output?", "options": ["list", "tuple", "dict", "set"], "answer": "list", "explanation": "'[]' represents a list in Python."},
    {"question": "Which of the following is NOT a valid variable name in Python?", "options": ["my_var", "_myVar", "3var", "var3"], "answer": "3var", "explanation": "Variable names cannot start with a number in Python."},
    {"question": "What does the 'len()' function do?", "options": ["Returns the type of variable", "Returns the number of elements in a sequence", "Sorts a list", "Converts a string to lowercase"], "answer": "Returns the number of elements in a sequence", "explanation": "The 'len()' function returns the length of an iterable like a list, tuple, or string."},
]

# Add more questions up to 100...

# Shuffle questions
random.shuffle(questions)

st.title("🐍 Python Quiz App")
st.subheader("Test your Python knowledge with 100+ MCQs!")

score = 0
for idx, q in enumerate(questions[:10]):  # Display 10 random questions per session
    st.write(f"**{idx + 1}. {q['question']}**")
    choice = st.radio("Select an option:", q['options'], key=idx)
    
    if st.button(f"Check Answer {idx + 1}", key=f"btn{idx}"):
        if choice == q['answer']:
            st.success("✅ Correct!")
            score += 1
        else:
            st.error(f"❌ Wrong! The correct answer is: {q['answer']}")
        st.info(q['explanation'])
        st.write("---")

st.write("### 📊 Your Final Score:", score, "/ 10")
if score >= 7:
    st.success("🎉 Great job! You know Python well!")
elif 4 <= score < 7:
    st.warning("⚠️ Good attempt! Keep practicing.")
else:
    st.error("❌ Keep learning and practicing!")

st.write("🔹 Developed by Esha using Streamlit")

