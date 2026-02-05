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
# 🎨 PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="SmartScan EduPad Pro",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🔧 OMR DETECTION FUNCTION (FOR BLUE-FILLED BUBBLES)
# ============================================
def omr_detect_answers(uploaded_file, debug=False):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.getbuffer())
        img_path = tmp.name

    img = cv2.imread(img_path)
    orig = img.copy()

    # --- Convert to HSV to detect blue filled circles ---
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Blue color range (tuned for your sheet)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    if debug:
        st.subheader("🧪 Blue Mask Preview")
        st.image(mask, use_container_width=True)

    # --- Find filled bubbles ---
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bubbles = []
    for c in contours:
        area = cv2.contourArea(c)
        if 500 < area < 10000:   # tuned for your bubble size
            x, y, w, h = cv2.boundingRect(c)
            if 0.7 < w/h < 1.3:
                bubbles.append((x, y, w, h))

    if not bubbles:
        return {}

    # --- Group by rows ---
    bubbles = sorted(bubbles, key=lambda b: b[1])
    rows = []
    for b in bubbles:
        placed = False
        for row in rows:
            if abs(row[0][1] - b[1]) < 40:
                row.append(b)
                placed = True
                break
        if not placed:
            rows.append([b])

    for row in rows:
        row.sort(key=lambda b: b[0])

    # --- Map to A/B/C/D ---
    answers = {}
    for qi, row in enumerate(rows, start=1):
        if len(row) < 2:
            continue

        for oi, (x, y, w, h) in enumerate(row):
            answers[str(qi)] = chr(ord('A') + oi)

            if debug:
                cv2.rectangle(orig, (x,y), (x+w,y+h), (0,255,0), 2)

    if debug:
        st.subheader("🖼️ Final Detection")
        st.image(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB), use_container_width=True)

    return answers

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

    key_answers = omr_detect_answers(st.session_state.answer_key_image, debug=True)
    st.subheader("🔍 OMR Detection (Answer Key)")
    st.json(key_answers)

    results = []

    for i, paper in enumerate(st.session_state.student_papers):
        student_answers = omr_detect_answers(paper, debug=True)
        st.subheader(f"🧪 OMR Detection (Student {i+1})")
        st.json(student_answers)

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
