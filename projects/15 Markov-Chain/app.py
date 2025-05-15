import streamlit as st
import random
import re

# Function to build Markov Chain Model
def build_markov_chain(text, order=2):
    words = text.split()
    markov_chain = {}

    for i in range(len(words) - order):
        key = tuple(words[i:i + order])
        next_word = words[i + order]

        if key not in markov_chain:
            markov_chain[key] = []
        markov_chain[key].append(next_word)

    return markov_chain

# Function to generate text using Markov Chain
def generate_text(markov_chain, length=50, order=2):
    start_key = random.choice(list(markov_chain.keys()))
    generated_words = list(start_key)

    for _ in range(length - order):
        key = tuple(generated_words[-order:])
        if key in markov_chain:
            generated_words.append(random.choice(markov_chain[key]))
        else:
            break

    return " ".join(generated_words)

# Streamlit UI
st.title("📜 Markov Chain Text Composer")

# Upload file or enter text
uploaded_file = st.file_uploader("📤 Upload a text file", type=["txt"])
user_text = st.text_area("Or paste your text here:")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
elif user_text:
    text = user_text
else:
    text = ""

if text:
    order = st.slider("Markov Chain Order", 1, 5, 2)
    length = st.slider("Generated Text Length", 20, 200, 50)

    markov_chain = build_markov_chain(text, order)
    generated_text = generate_text(markov_chain, length, order)

    st.subheader("📝 Generated Text:")
    st.write(generated_text)

    # Copy button
    st.button("📋 Copy to Clipboard", on_click=lambda: st.write(generated_text))

# Footer
st.markdown("📌 Create random text using Markov Chains in Python & Streamlit.")
st.write("🔹 Developed by Esha using Streamlit")
