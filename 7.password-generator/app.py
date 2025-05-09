import streamlit as st
import random
import string

# Function to generate password
def generate_password(length, use_upper, use_lower, use_numbers, use_special):
    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        return "Please select at least one character type."
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Streamlit UI
st.title("🔑 Random Password Generator")

# User input options
length = st.slider("Select Password Length", min_value=4, max_value=50, value=12)
use_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
use_lower = st.checkbox("Include Lowercase Letters (a-z)", value=True)
use_numbers = st.checkbox("Include Numbers (0-9)", value=True)
use_special = st.checkbox("Include Special Characters (!@#$%^&*)", value=True)

# Generate password on button click
if st.button("Generate Password 🔄"):
    password = generate_password(length, use_upper, use_lower, use_numbers, use_special)
    st.text_input("Your Generated Password", value=password, key="password")
    
    # Copy to clipboard button (requires st.code)
    st.code(password, language="")

# Footer
st.markdown("🔒 Keep your passwords secure and don't share them with anyone.")
st.write("🔹 Developed by Esha")
