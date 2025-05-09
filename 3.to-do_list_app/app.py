import streamlit as st
import datetime
import pandas as pd

# Initialize session state for storing tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Streamlit UI Configuration
st.set_page_config(page_title="📝 To-Do List App", page_icon="✅", layout="centered")

st.title("📝 Advanced To-Do List App ")

# Task Input Section
task = st.text_input("Enter your task:")
category = st.selectbox("Select Category:", ["Work", "Personal", "Shopping", "Others"])
priority = st.selectbox("Set Priority:", ["High", "Medium", "Low"])
deadline = st.date_input("Set Deadline:", datetime.date.today())

if st.button("➕ Add Task"):
    if task:
        st.session_state.tasks.append({"task": task, "category": category, "priority": priority, "deadline": deadline, "status": "Pending"})
        st.success("✅ Task Added Successfully!")
    else:
        st.error("⚠️ Task cannot be empty!")

# Display Tasks
st.header("📋 Your Tasks")
if len(st.session_state.tasks) > 0:
    for index, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        col1.write(f"**{task['task']}** ({task['category']} - {task['priority']})  📅 {task['deadline']}")

        if task["status"] == "Completed":
            col2.success("✅ Done")
        else:
            if col2.button("✔ Mark Done", key=f"done{index}"):
                st.session_state.tasks[index]["status"] = "Completed"
                st.experimental_rerun()

        if col3.button("🗑 Delete", key=f"del{index}"):
            del st.session_state.tasks[index]
            st.experimental_rerun()
else:
    st.info("No tasks yet. Start adding!")

# Productivity Chart
st.header("📊 Task Completion Stats")
if len(st.session_state.tasks) > 0:
    df = pd.DataFrame(st.session_state.tasks)
    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)

st.write("🔹 Developed by Esha")
