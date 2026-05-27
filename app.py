import streamlit as st
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import spacy

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

nlp = spacy.load("en_core_web_sm")

def create_pdf_report(score, found_skills, category, suggestions):

    doc = SimpleDocTemplate("resume_report.pdf")

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI Resume Analysis Report",
        styles['Title']
    )

    content.append(title)

    content.append(Spacer(1, 12))

    ats = Paragraph(
        f"<b>ATS Score:</b> {score}/100",
        styles['BodyText']
    )

    content.append(ats)

    content.append(Spacer(1, 12))

    skills = Paragraph(
        f"<b>Detected Skills:</b> {', '.join(found_skills)}",
        styles['BodyText']
    )

    content.append(skills)

    content.append(Spacer(1, 12))

    cat = Paragraph(
        f"<b>Predicted Category:</b> {category}",
        styles['BodyText']
    )

    content.append(cat)

    content.append(Spacer(1, 12))

    sugg = Paragraph(
        f"<b>Suggestions:</b><br/>" +
        "<br/>".join(suggestions),
        styles['BodyText']
    )

    content.append(sugg)

    doc.build(content)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        to right,
        #0f172a,
        #1e293b
    );
}

html, body, [class*="css"]  {
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

p, label, div {
    color: white;
}

div.stButton > button {
    background-color: #38bdf8;
    color: black;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

div.stDownloadButton > button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📌 About")
st.sidebar.write(
    """
    AI Resume Analyzer helps analyze resumes,
    detect skills, and calculate ATS score.
    """
)

st.sidebar.info("Built using Python + Streamlit")

# Main Title
st.title("📄 AI Resume Analyzer")

st.markdown(
    "Upload your resume and get ATS analysis instantly."
)

# Skills Database
skills_list = [
    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "html",
    "css",
    "javascript",
    "tensorflow",
    "mysql",
    "git",
    "github",
    "sql",
    "react",
    "data analysis",
    "nlp",
    "flask",
    "streamlit"
]

# File Upload
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type="pdf"
)

if uploaded_file is not None:

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        text += page.extract_text()

    text = text.lower()

    doc = nlp(text)

    # Skill Detection
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    # ATS Score
    score = len(found_skills) * 5

    if score > 100:
        score = 100

    # Missing Skills
    missing_skills = []

    for skill in skills_list:
        if skill not in found_skills:
            missing_skills.append(skill)

    # Layout Columns
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Detected Skills")

        for skill in found_skills:
            st.success(skill)

    with col2:

        st.subheader("📌 Recommended Skills")

        for skill in missing_skills[:5]:
            st.error(skill)

    # ATS Score Section
    st.subheader("📊 ATS Score")

    st.progress(score / 100)

    st.metric(label="ATS Score", value=f"{score}/100")

    # Skill Chart
    st.subheader("📈 Skills Analysis")

    labels = ["Detected", "Missing"]

    sizes = [len(found_skills), len(missing_skills)]

    fig, ax = plt.subplots()

    ax.pie(
        sizes,
        labels=labels,
         autopct="%1.1f%%"
    )

    st.pyplot(fig)

    st.subheader("🧠 NLP Keywords")

    keywords = []

    for token in doc:

       word = token.text.lower().strip()

    # Ignore stopwords, punctuation, numbers
       if (
        token.is_stop == False
        and token.is_punct == False
        and token.is_digit == False
        and len(word) > 2
        and word.isalpha()
      ):

        keywords.append(word)

# Remove duplicates
    unique_keywords = list(set(keywords))

# Sort alphabetically
    unique_keywords.sort()

# Show only first 20
    st.write(unique_keywords[:20])

    # Resume Category Prediction

    st.subheader("🎯 Predicted Resume Category")

    category = "General"

    if (
       "machine learning" in found_skills
        or "tensorflow" in found_skills
        or "nlp" in found_skills
    ):
       category = "AI / Machine Learning"

    elif (
        "html" in found_skills
        or "css" in found_skills
        or "javascript" in found_skills
        or "react" in found_skills
   ):
       category = "Web Development"

    elif (
        "java" in found_skills
   ):
       category = "Java Developer"

    elif (
      "android" in text
   ):
      category = "Android Development"

    elif (
       "data analysis" in found_skills
        or "sql" in found_skills
   ):
      category = "Data Science"

    st.success(category)

    # Job Recommendations

    st.subheader("💼 Recommended Job Roles")

    recommended_jobs = []

    if category == "AI / Machine Learning":

       recommended_jobs = [
        "Machine Learning Intern",
        "AI Engineer",
        "Data Scientist",
        "NLP Engineer"
    ]

    elif category == "Web Development":

      recommended_jobs = [
        "Frontend Developer",
        "Web Developer",
        "React Developer",
        "UI Developer"
    ]

    elif category == "Java Developer":

      recommended_jobs = [
        "Java Developer",
        "Backend Developer",
        "Software Engineer"
    ]

    elif category == "Android Development":

      recommended_jobs = [
        "Android Developer",
        "Mobile App Developer"
    ]

    elif category == "Data Science":

       recommended_jobs = [
        "Data Analyst",
        "Business Analyst",
        "Data Scientist"
    ]

    else:

      recommended_jobs = [
        "Software Developer",
        "Python Developer"
    ]

    for job in recommended_jobs:

     st.info(job)

     # AI Resume Suggestions

    st.subheader("🤖 AI Resume Improvement Suggestions")

    suggestions = []

# Low ATS score
    if score < 40:
      suggestions.append(
        "Add more technical skills to improve ATS score."
    )

# Missing GitHub
    if "github" not in found_skills:
      suggestions.append(
        "Include GitHub projects or profile links."
    )

# Missing ML skills
    if category == "AI / Machine Learning":

       if "tensorflow" not in found_skills:
         suggestions.append(
            "Add TensorFlow or deep learning projects."
        )

# Missing web skills
    if category == "Web Development":

       if "react" not in found_skills:
          suggestions.append(
            "Learning React can improve frontend opportunities."
        )

# Generic suggestion
    suggestions.append(
      "Add more project descriptions with measurable impact."
   )

# Display Suggestions
    for suggestion in suggestions:

     st.warning(suggestion)

    # Portfolio Summary
    st.subheader("📝 Portfolio Summary")

    summary = f"""
    Aspiring software developer skilled in {", ".join(found_skills)}.
    Passionate about AI, machine learning, and software development.
    """

    st.info(summary)

    # Generate PDF Report

    create_pdf_report(
    score,
    found_skills,
    category,
    suggestions
   )

# Download Button

    with open("resume_report.pdf", "rb") as pdf_file:

      st.download_button(
        label="📥 Download Resume Report",
        data=pdf_file,
        file_name="AI_Resume_Report.pdf",
        mime="application/pdf"
    )