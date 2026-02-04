import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time

# ============================================
# 🎨 PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="SmartScan EduPad Pro",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 CSS
# ============================================
st.markdown("""
<style>
:root {
    --primary: #6366F1;
    --secondary: #10B981;
    --accent: #8B5CF6;
}

.metric {
    background: white;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.pro-upload {
    border: 2px dashed #d1d5db;
    border-radius: 16px;
    padding: 40px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# 🔧 SESSION INIT
# ============================================
if "answer_key_image" not in st.session_state:
    st.session_state.answer_key_image = None
if "student_papers" not in st.session_state:
    st.session_state.student_papers = []
if "results" not in st.session_state:
    st.session_state.results = None

# ============================================
# 🔧 SIDEBAR
# ============================================
with st.sidebar:
    st.header("📋 Test Setup")

    answer_key_upload = st.file_uploader(
        "Upload Answer Key (Image)",
        type=["jpg", "jpeg", "png"],
        key="answer_key_upload"
    )

    if answer_key_upload:
        st.session_state.answer_key_image = answer_key_upload
        st.image(answer_key_upload, caption="Answer Key", use_column_width=True)

    st.divider()

    passing_score = st.slider("Passing Score (%)", 40, 100, 60)
    ai_mode = st.toggle("AI Assisted Evaluation", True)

# ============================================
# 🎯 MAIN UI
# ============================================
st.title("📱 SmartScan EduPad Pro")
st.caption("AI-Powered Test Paper Comparison System")

# ============================================
# 📄 UPLOAD STUDENT PAPERS
# ============================================
st.subheader("📄 Upload Student Answer Sheets")

student_uploads = st.file_uploader(
    "Upload Student Papers (Images)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key="student_uploads"
)

if student_uploads:
    st.session_state.student_papers = student_uploads
    st.success(f"{len(student_uploads)} student papers uploaded")

# ============================================
# 🔬 START COMPARISON
# ============================================
if st.button("🔬 Start Comparison", use_container_width=True):

    if not st.session_state.answer_key_image:
        st.error("Please upload Answer Key image.")
        st.stop()

    if not st.session_state.student_papers:
        st.error("Please upload Student answer sheets.")
        st.stop()

    with st.spinner("Analyzing papers..."):
        progress = st.progress(0)
        steps = ["Reading answer key...", "Scanning student sheets...", "Comparing answers...", "Generating scores..."]

        for i, step in enumerate(steps):
            st.info(step)
            progress.progress((i + 1) * 25)
            time.sleep(0.5)

    # Simulated comparison results (replace with OCR later)
    results = []
    for i in range(len(st.session_state.student_papers)):
        score = np.random.randint(40, 100)
        confidence = np.random.uniform(85, 99)

        results.append({
            "Student ID": f"STU{i+1:03d}",
            "Score (%)": score,
            "AI Confidence (%)": f"{confidence:.1f}%",
            "Status": "PASS" if score >= passing_score else "FAIL"
        })

    st.session_state.results = pd.DataFrame(results)
    st.success("✅ Comparison Complete")

# ============================================
# 📊 ANALYTICS
# ============================================
if st.session_state.results is not None:
    st.subheader("📊 Results Overview")

    df = st.session_state.results

    col1, col2, col3 = st.columns(3)
    col1.metric("Students", len(df))
    col2.metric("Pass Rate", f"{(df['Score (%)'] >= passing_score).mean() * 100:.1f}%")
    col3.metric("Top Score", f"{df['Score (%)'].max()}%")

    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Score Distribution")
    fig = px.histogram(df, x="Score (%)", nbins=10)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI Confidence vs Score")
    df["AI_Confidence_num"] = df["AI Confidence (%)"].str.rstrip('%').astype(float)
    fig2 = px.scatter(df, x="Score (%)", y="AI_Confidence_num", hover_name="Student ID")
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# 📥 EXPORT
# ============================================
if st.session_state.results is not None:
    csv = st.session_state.results.to_csv(index=False)
    st.download_button("📥 Download Results (CSV)", csv, "results.csv", "text/csv")
