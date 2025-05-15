import streamlit as st
import fitz  # PyMuPDF
import docx2txt
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ✅ Fix: Initialize NLTK resources (punkt_tab included)
def setup_nltk():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
        
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")
        
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab")

setup_nltk()

stop_words = set(stopwords.words("english"))

# Enhanced Streamlit UI
st.set_page_config(
    page_title="📄 Smart Resume Analyzer", 
    layout="wide",
    page_icon="📄"
)

# Custom CSS
st.markdown("""
<style>
    .stTextArea [data-baseweb=textarea] {
        background-color: #f8f9fa;
    }
    .match-score {
        font-size: 1.5rem !important;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 Smart Resume Analyzer")
st.markdown("""
Upload your resume to analyze key skills, education qualifications, and experience keywords. 
Compare with job descriptions to improve your resume matching.
""")

# File Upload Section
with st.expander("📤 Upload Resume", expanded=True):
    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file", 
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )

# Text Extraction Functions
def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return " ".join(page.get_text() for page in doc)
    except Exception as e:
        st.error(f"PDF extraction error: {str(e)}")
        return ""

def extract_text_from_docx(file):
    try:
        return docx2txt.process(file)
    except Exception as e:
        st.error(f"DOCX extraction error: {str(e)}")
        return ""

# Keyword Extraction
def extract_keywords(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    try:
        words = word_tokenize(text.lower())
    except Exception as e:
        st.error(f"Tokenization error: {str(e)}")
        return {"Skills": [], "Education": [], "Experience": []}

    words = [word for word in words if word.isalpha() 
             and word not in stop_words 
             and len(word) > 2]

    education_keywords = {"bachelor", "master", "degree", "bs", "ms", 
                         "phd", "diploma", "certification", "education"}
    experience_keywords = {"experience", "worked", "intern", "job", 
                          "project", "years", "role", "position"}
    skill_keywords = {"python", "java", "sql", "excel", "analysis", 
                     "management", "communication", "team"}

    skills = []
    education = []
    experience = []

    for word in set(words):
        if word in skill_keywords:
            skills.append(word)
        elif word in education_keywords:
            education.append(word)
        elif word in experience_keywords:
            experience.append(word)
        else:
            skills.append(word)

    return {
        "Skills": sorted(skills),
        "Education": sorted(education),
        "Experience": sorted(experience)
    }

# Main Logic
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    if resume_text:
        with st.expander("📄 View Extracted Resume Text", expanded=False):
            st.text_area("Full Text", resume_text[:5000], height=300)

        with st.spinner("🔍 Analyzing your resume..."):
            keywords = extract_keywords(resume_text)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("💼 Skills")
            st.write(", ".join(keywords["Skills"]) or "No skills detected")

        with col2:
            st.subheader("🎓 Education")
            st.write(", ".join(keywords["Education"]) or "No education keywords found")

        with col3:
            st.subheader("🏢 Experience")
            st.write(", ".join(keywords["Experience"]) or "No experience keywords found")

        st.divider()
        st.subheader("🔗 Compare with Job Description")
        job_desc = st.text_area(
            "Paste the job description here to check match percentage",
            height=200,
            placeholder="Paste job description text here..."
        )

        if job_desc:
            with st.spinner("⚡ Calculating match score..."):
                resume_keywords = set(keywords["Skills"])
                job_keywords = set(extract_keywords(job_desc)["Skills"])
                
                if not job_keywords:
                    st.error("No keywords found in job description")
                else:
                    match_score = len(resume_keywords & job_keywords)
                    total = len(job_keywords)
                    percentage = (match_score / total) * 100
                    
                    st.markdown(f"""
                    <div class="match-score">
                        <h3>Match Score: {percentage:.1f}%</h3>
                        <p>{match_score} out of {total} keywords matched</p>
                    </div>
                    """, unsafe_allow_html=True)

                    missing = job_keywords - resume_keywords
                    if missing:
                        st.warning(f"Missing keywords: {', '.join(sorted(missing))}")

                    st.info("💡 Tip: Add missing keywords to your resume (if relevant) to improve your match score!")
st.write("🔹 Developed by Esha")
