import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Esha's Python Projects", layout="wide")

st.title("🐍 Esha's Python Projects")
st.markdown("Explore my Python projects below. Select any to view its output:")

# Sidebar
st.sidebar.title("📁 Projects")

# Automatically detect all folders (assuming one project per folder)
all_items = os.listdir()
projects = [item for item in all_items if os.path.isdir(item) and not item.startswith('.') and item != '.git']
projects.sort()

selected_project = st.sidebar.selectbox("Select a project", projects)

if selected_project:
    st.header(f"🚀 {selected_project.title()}")
    
    # Try to detect a main file inside the project
    possible_main_files = ["app.py", "main.py", f"{selected_project}.py"]
    found = False
    
    for filename in possible_main_files:
        filepath = os.path.join(selected_project, filename)
        if os.path.exists(filepath):
            st.subheader("🔍 Project Output:")
            with st.spinner("Running the project..."):
                result = subprocess.run(["python", filepath], capture_output=True, text=True)
                st.code(result.stdout)
                if result.stderr:
                    st.error("⚠️ Errors:\n" + result.stderr)
            found = True
            break
    
    if not found:
        st.warning("No main file (main.py or app.py) found in this project folder.")

    # GitHub link
    github_url = f"https://github.com/eshaadeel0967/25-Projects/tree/main/{selected_project}"
    st.markdown(f"[🔗 View on GitHub]({github_url})")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Esha | [GitHub](https://github.com/eshaadeel0967/25-Projects)")
