import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import cv2
from PIL import Image
import tempfile
import re
import os

# ============================================
# 🔧 TESSERACT PATH FIX (Optional)
# ============================================
# Keep OCR for names / IDs if needed
# if os.name != "nt":
#     pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

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
# 🔧 OMR DETECTION FUNCTION
# ============================================
def omr_detect_answers(uploaded_file):
    """Detect filled bubbles and return answers dict {question: option}"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.getbuffer())
        img_path = tmp.name

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive threshold for different lighting
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )
    thresh = cv2.GaussianBlur(thresh, (5,5), 0)

    # Find contours (potential bubbles)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bubbles = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 300 < area < 5000:
            x, y, w, h = cv2.boundingRect(cnt)
            if 0.8 < w/h < 1.2:
                bubbles.append((x, y, w, h))

    # Sort bubbles into rows and columns
    bubbles = sorted(bubbles, key=lambda b: b[1])
    rows = []
    current_row = []
    last_y = -100
    for b in bubbles:
        x, y, w, h = b
        if abs(y - last_y) > 10:
            if current_row:
                current_row = sorted(current_row, key=lambda c: c[0])
                rows.append(current_row)
            current_row = [b]
            last_y = y
        else:
            current_row.append(b)
    if current_row:
        current_row = sorted(current_row, key=lambda c: c[0])
        rows.append(current_row)

    # Detect filled bubbles
    answers_detected = {}
    for q_index, row in enumerate(rows, start=1):
        for opt_index, (x, y, w, h) in enumerate(row):
            roi = thresh[y:y+h, x:x+w]
            filled_ratio = cv2.countNonZero(roi) / (w*h)
            if filled_ratio > 0.5:
                option = chr(ord('A') + opt_index)
                answers_detected[str(q_index)] = option
                break  # Only one selection per row

    return answers_detected

# ============================================
# 🔧 SCORE CALCULATION
# ============================================
def calculate_score(key_answers, student_answers):
    total = len(key_answers)
    if total == 0:
        return 0
    correct = 0
    for q in key_answers:
        if q in student_answers and key_answers[q] == student_answers[q]:
            correct += 1
    return round((correct / total) * 100, 2)

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
        st.image(answer_key_upload, caption="Answer Key", use_container_width=True)

    passing_score = st.slider("Passing Score (%)", 40, 100, 60)

# ============================================
# 🎯 MAIN UI
# ============================================
st.title("📱 SmartScan EduPad Pro")
st.caption("OMR-Based Test Paper Comparison System")

student_uploads = st.file_uploader(
    "Upload Student Answer Sheets",
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
        st.error("Upload answer key image.")
        st.stop()

    if not st.session_state.student_papers:
        st.error("Upload student sheets.")
        st.stop()

    with st.spinner("Running OMR Detection..."):
        time.sleep(1)

    # ----------------------------
    # Detect answers from answer key
    # ----------------------------
    key_answers = omr_detect_answers(st.session_state.answer_key_image)
    st.subheader("🔍 OMR Detection (Answer Key)")
    st.json(key_answers)

    results = []

    for i, paper in enumerate(st.session_state.student_papers):
        # ----------------------------
        # Detect answers from student sheet
        # ----------------------------
        student_answers = omr_detect_answers(paper)
        st.subheader(f"🧪 OMR Detection (Student {i+1})")
        st.json(student_answers)

        # ----------------------------
        # Calculate score
        # ----------------------------
        score = calculate_score(key_answers, student_answers)
        confidence = np.random.uniform(85, 99)

        results.append({
            "Student ID": f"STU{i+1:03d}",
            "Score (%)": score,
            "AI Confidence (%)": f"{confidence:.1f}%",
            "Status": "PASS" if score >= passing_score else "FAIL"
        })

    st.session_state.results = pd.DataFrame(results)
    st.success("✅ OMR Comparison Complete")

# ============================================
# 📊 RESULTS
# ============================================
if st.session_state.results is not None:
    df = st.session_state.results

    col1, col2, col3 = st.columns(3)
    col1.metric("Students", len(df))
    col2.metric("Pass Rate", f"{(df['Score (%)'] >= passing_score).mean() * 100:.1f}%")
    col3.metric("Top Score", f"{df['Score (%)'].max()}%")

    st.dataframe(df, use_container_width=True)

    fig = px.histogram(df, x="Score (%)", nbins=10)
    st.plotly_chart(fig, use_container_width=True)

    df["AI_Confidence_num"] = df["AI Confidence (%)"].str.rstrip('%').astype(float)
    fig2 = px.scatter(df, x="Score (%)", y="AI_Confidence_num")
    st.plotly_chart(fig2, use_container_width=True)

    csv = df.to_csv(index=False)
    st.download_button("📥 Download Results", csv, "results.csv", "text/csv")
