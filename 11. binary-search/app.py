import streamlit as st
import time

# Binary Search Function
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    steps = []
    
    while low <= high:
        mid = (low + high) // 2
        steps.append((low, mid, high))  # Store the search range
        
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1, steps  # If not found

# Streamlit UI
st.title("🔍 Binary Search Visualization")

# User input for sorted list
numbers = st.text_input("Enter a sorted list of numbers (comma-separated):", "1, 3, 5, 7, 9, 11, 13, 15")
target = st.number_input("Enter the number to search for:", value=7)

if st.button("Search 🔎"):
    try:
        # Convert input to list of numbers
        arr = list(map(int, numbers.split(',')))
        arr.sort()  # Ensure it's sorted
        
        # Perform Binary Search
        index, steps = binary_search(arr, target)
        
        # Visualization
        for low, mid, high in steps:
            st.write(f"Searching between indices {low} and {high}, middle: {mid} (value: {arr[mid]})")
            time.sleep(0.5)
        
        # Display result
        if index != -1:
            st.success(f"✅ Number {target} found at index {index}!")
        else:
            st.error(f"❌ Number {target} not found in the list.")
    
    except ValueError:
        st.error("⚠️ Please enter valid numbers separated by commas.")

# Footer
st.markdown("📌 Learn how Binary Search works step by step!")
st.write("🔹 Developed by Esha")

