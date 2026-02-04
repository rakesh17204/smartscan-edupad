import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import io

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
# 🎨 PROFESSIONAL CSS
# ============================================
st.markdown("""
<style>
    /* 1. PROFESSIONAL FONT IMPORT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@700;800&family=JetBrains+Mono&display=swap');

    :root {
        --primary: #6366F1;
        --secondary: #10B981;
        --accent: #8B5CF6;
        --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }

    * { 
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    h1, h2, h3, h4 { 
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.5px;
        font-weight: 700;
    }

    /* 2. SOPHISTICATED BACKGROUND */
    .stApp {
        background-color: #f8fafc;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
        background-attachment: fixed;
    }

    /* 3. MAIN CONTAINER */
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        margin: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e5e7eb;
    }

    /* 4. PROFESSIONAL CARDS */
    .pro-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        height: 100%;
    }

    .pro-card:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }

    /* 5. METRIC CARDS */
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
        line-height: 1;
    }

    /* 6. BUTTONS */
    .stButton > button {
        background: var(--primary) !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button:hover {
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4) !important;
        opacity: 0.9;
    }

    /* 7. SIDEBAR */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(0,0,0,0.05);
    }

    /* 8. LOADING ANIMATION */
    @keyframes shimmer {
        0% { background-position: -468px 0; }
        100% { background-position: 468px 0; }
    }
    
    .loading-shimmer {
        background: linear-gradient(to right, #f6f7f8 8%, #edeef1 18%, #f6f7f8 33%);
        background-size: 800px 104px;
        animation: shimmer 1.5s linear infinite forwards;
        border-radius: 12px;
    }

    /* 9. CONFIDENCE BAR */
    .confidence-bar {
        height: 8px;
        background: #e5e7eb;
        border-radius: 4px;
        overflow: hidden;
        margin: 8px 0;
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--secondary), var(--primary));
        border-radius: 4px;
        transition: width 0.6s ease;
    }

    /* 10. MOBILE RESPONSIVE */
    @media (max-width: 768px) {
        .main-container {
            padding: 20px;
            margin: 10px;
        }
        
        .pro-card {
            padding: 16px;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }

    /* 11. UPLOAD AREA */
    .pro-upload {
        border: 2px dashed #d1d5db;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        background: white;
        transition: all 0.3s;
    }
    
    .pro-upload:hover {
        border-color: var(--primary);
        background: rgba(99, 102, 241, 0.02);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 🔧 SIDEBAR - SETTINGS & CONTROLS
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 2.5rem; margin-bottom: 10px; color: #6366F1;">📱</div>
        <h1 style="color: #1f2937; font-size: 1.5rem; margin: 0;">SmartScan</h1>
        <p style="color: #6b7280; font-size: 0.875rem; margin: 4px 0;">EduPad Pro</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Test Paper Settings
    st.markdown("### 📋 Test Paper Setup")
    
    with st.expander("Answer Key Configuration", expanded=True):
        answer_format = st.selectbox(
            "Answer Format:",
            ["Q1:A, Q2:B", "1.A, 2.B", "Custom"]
        )
        
        answer_key = st.text_area(
            "Enter Answer Key:",
            "Q1:A\nQ2:B\nQ3:C\nQ4:D\nQ5:A\nQ6:B\nQ7:C\nQ8:D\nQ9:A\nQ10:B",
            height=150
        )
    
    # Evaluation Settings
    with st.expander("Evaluation Settings"):
        passing_score = st.slider("Passing Score (%)", 40, 100, 60)
        enable_ai = st.toggle("AI Confidence Scoring", True)
        partial_credit = st.toggle("Partial Credit", False)
    
    # System Info
    st.markdown("---")
    st.markdown("### 📊 System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status", "Active", "✓")
    with col2:
        st.metric("Accuracy", "98.7%", "+0.3%")

# ============================================
# 🎯 MAIN CONTENT
# ============================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title
st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <h1 style="font-size: 3rem; color: #1f2937; margin: 0; line-height: 1.1;">
        SmartScan EduPad Pro
    </h1>
    <p style="color: #6b7280; font-size: 1.125rem; margin: 12px 0 24px 0;">
        AI-Powered Test Paper Comparison System
    </p>
</div>
""", unsafe_allow_html=True)

# Metrics Overview
st.markdown("### 📊 System Performance")
metrics_cols = st.columns(4)

metrics = [
    ("🧠", "Accuracy", "99.2%", "OCR Precision"),
    ("⚡", "Speed", "2.3s", "Per Sheet"),
    ("📈", "Success Rate", "98.7%", "Evaluation"),
    ("🏫", "Scale", "250+", "Concurrent")
]

for idx, (icon, title, value, desc) in enumerate(metrics):
    with metrics_cols[idx]:
        st.markdown(f"""
        <div class="pro-card">
            <div style="font-size: 2rem; margin-bottom: 12px; color: #6366F1;">{icon}</div>
            <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 4px;">{title}</div>
            <div class="metric-value">{value}</div>
            <div style="color: #9ca3af; font-size: 0.75rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 📋 TABS FOR DIFFERENT FEATURES
# ============================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 **Upload & Compare**", 
    "📊 **Analytics**", 
    "🔍 **Question Analysis**", 
    "🎯 **Weak Areas**"
])

# ============================================
# 📄 TAB 1: UPLOAD & COMPARE
# ============================================
with tab1:
    st.header("📄 Upload & Compare Test Papers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Test Paper Upload
        st.markdown("#### Reference Test Paper")
        reference_paper = st.file_uploader(
            "Upload test paper (PDF/Image)",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            key="reference"
        )
        
        if reference_paper:
            st.success(f"✅ {reference_paper.name} uploaded")
            st.session_state.reference_paper = reference_paper
    
    with col2:
        # Student Papers Upload
        st.markdown("#### Student Answer Sheets")
        student_papers = st.file_uploader(
            "Upload student papers",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key="student"
        )
        
        if student_papers:
            st.success(f"✅ {len(student_papers)} student papers uploaded")
            st.session_state.student_papers = student_papers
    
    # Comparison Button
    if st.button("🔬 Start Comparison", type="primary", use_container_width=True):
        if 'answer_key' not in st.session_state:
            st.error("Please set up answer key in sidebar")
        elif not student_papers:
            st.error("Please upload student papers")
        else:
            st.session_state.comparison_started = True
            
            # Simulate processing
            with st.spinner("Processing papers..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    "Reading test papers...",
                    "Extracting answers...",
                    "Running AI analysis...",
                    "Comparing with answer key...",
                    "Calculating scores..."
                ]
                
                for i, step in enumerate(steps):
                    status_text.markdown(f"""
                    <div class="loading-shimmer" style="padding: 16px; margin: 8px 0;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="color: #6366F1;">●</div>
                            <div style="font-weight: 500;">{step}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    progress_bar.progress((i + 1) * 20)
                    time.sleep(0.5)
            
            # Generate results
            num_students = len(student_papers) if student_papers else 5
            results = []
            
            for i in range(num_students):
                score = np.random.randint(6, 11)  # 6-10
                percentage = (score / 10) * 100
                
                # AI Confidence Score
                ai_confidence = np.random.uniform(85, 99)
                
                results.append({
                    "Student ID": f"STU{i+1:03d}",
                    "Score": f"{score}/10",
                    "Percentage": f"{percentage:.1f}%",
                    "Grade": "A" if percentage >= 85 else "B" if percentage >= 70 else "C",
                    "AI Confidence": f"{ai_confidence:.1f}%",
                    "Status": "✅ PASS" if percentage >= passing_score else "❌ FAIL"
                })
            
            st.session_state.results = results
            st.success(f"✅ Analysis complete! Processed {num_students} papers")
            st.rerun()

# ============================================
# 📊 TAB 2: ANALYTICS CHARTS
# ============================================
with tab2:
    st.header("📊 Advanced Analytics")
    
    if 'results' not in st.session_state:
        st.info("Run comparison first to see analytics")
    else:
        results = st.session_state.results
        
        # Convert results to DataFrame
        df = pd.DataFrame(results)
        df['Percentage_num'] = df['Percentage'].str.rstrip('%').astype(float)
        df['AI_Confidence_num'] = df['AI Confidence'].str.rstrip('%').astype(float)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Score Distribution
            st.markdown("#### 📈 Score Distribution")
            
            fig1 = px.histogram(
                df, 
                x='Percentage_num',
                nbins=10,
                color_discrete_sequence=['#6366F1']
            )
            
            fig1.update_layout(
                xaxis_title="Percentage (%)",
                yaxis_title="Number of Students",
                showlegend=False,
                plot_bgcolor='white',
                height=400
            )
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # AI Confidence vs Scores
            st.markdown("#### 🤖 AI Confidence vs Scores")
            
            fig2 = px.scatter(
                df,
                x='Percentage_num',
                y='AI_Confidence_num',
                color='Grade',
                size='AI_Confidence_num',
                hover_name='Student ID',
                color_discrete_sequence=['#10B981', '#6366F1', '#F59E0B']
            )
            
            fig2.update_layout(
                xaxis_title="Score (%)",
                yaxis_title="AI Confidence (%)",
                plot_bgcolor='white',
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # Performance Metrics
        st.markdown("### 📊 Performance Summary")
        
        summary_cols = st.columns(4)
        
        avg_score = df['Percentage_num'].mean()
        pass_rate = (df['Percentage_num'] >= passing_score).mean() * 100
        avg_confidence = df['AI_Confidence_num'].mean()
        top_score = df['Percentage_num'].max()
        
        summary_data = [
            ("📊", "Average Score", f"{avg_score:.1f}%"),
            ("✅", "Pass Rate", f"{pass_rate:.1f}%"),
            ("🤖", "Avg Confidence", f"{avg_confidence:.1f}%"),
            ("🏆", "Top Score", f"{top_score:.1f}%")
        ]
        
        for idx, (icon, title, value) in enumerate(summary_data):
            with summary_cols[idx]:
                st.markdown(f"""
                <div class="pro-card" style="text-align: center;">
                    <div style="font-size: 1.5rem; margin-bottom: 8px; color: #6366F1;">{icon}</div>
                    <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 4px;">{title}</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #1f2937;">{value}</div>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# 🔍 TAB 3: DETAILED QUESTION ANALYSIS
# ============================================
with tab3:
    st.header("🔍 Detailed Question Analysis")
    
    if 'results' not in st.session_state:
        st.info("Run comparison first to see question analysis")
    else:
        # Question Performance Data
        questions = [f'Q{i+1}' for i in range(10)]
        
        # Simulate question performance
        question_data = []
        for i, q in enumerate(questions):
            correct_rate = np.random.uniform(60, 95)
            common_wrong = np.random.choice(['A', 'B', 'C', 'D'])
            ai_confidence = np.random.uniform(85, 99)
            
            question_data.append({
                'Question': q,
                'Correct Answer': chr(65 + i % 4),  # A, B, C, D cycling
                'Correct Rate': f"{correct_rate:.1f}%",
                'Most Common Wrong': common_wrong,
                'AI Confidence': f"{ai_confidence:.1f}%",
                'Difficulty': 'Easy' if correct_rate >= 80 else 'Medium' if correct_rate >= 60 else 'Hard'
            })
        
        # Display as table
        df_questions = pd.DataFrame(question_data)
        st.dataframe(df_questions, use_container_width=True, hide_index=True)
        
        # Question Performance Chart
        st.markdown("#### 📊 Question Performance")
        
        fig3 = go.Figure(data=[
            go.Bar(
                name='Correct Rate',
                x=questions,
                y=[float(d['Correct Rate'].rstrip('%')) for d in question_data],
                marker_color='#10B981'
            ),
            go.Bar(
                name='AI Confidence',
                x=questions,
                y=[float(d['AI Confidence'].rstrip('%')) for d in question_data],
                marker_color='#6366F1'
            )
        ])
        
        fig3.update_layout(
            barmode='group',
            xaxis_title="Question",
            yaxis_title="Percentage (%)",
            plot_bgcolor='white',
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)

# ============================================
# 🎯 TAB 4: WEAK AREA IDENTIFICATION
# ============================================
with tab4:
    st.header("🎯 Weak Area Identification")
    
    if 'results' not in st.session_state:
        st.info("Run comparison first to identify weak areas")
    else:
        # Simulate weak areas by subject/topic
        weak_areas_data = [
            {"Topic": "Algebra", "Weak Students": np.random.randint(5, 15), "Avg Score": np.random.uniform(50, 70)},
            {"Topic": "Geometry", "Weak Students": np.random.randint(3, 12), "Avg Score": np.random.uniform(60, 75)},
            {"Topic": "Calculus", "Weak Students": np.random.randint(8, 18), "Avg Score": np.random.uniform(45, 65)},
            {"Topic": "Trigonometry", "Weak Students": np.random.randint(4, 10), "Avg Score": np.random.uniform(65, 80)},
            {"Topic": "Statistics", "Weak Students": np.random.randint(2, 8), "Avg Score": np.random.uniform(70, 85)},
        ]
        
        df_weak = pd.DataFrame(weak_areas_data)
        
        # Display weak areas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Weak Areas by Topic")
            
            for area in weak_areas_data:
                st.markdown(f"""
                <div class="pro-card" style="margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; color: #1f2937;">{area['Topic']}</div>
                            <div style="color: #6b7280; font-size: 0.875rem;">{area['Weak Students']} students struggling</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #EF4444; font-weight: 700;">{area['Avg Score']:.1f}%</div>
                            <div style="color: #9ca3af; font-size: 0.75rem;">Average Score</div>
                        </div>
                    </div>
                    <div class="confidence-bar" style="margin-top: 12px;">
                        <div class="confidence-fill" style="width: {area['Avg Score']}%; background: #EF4444;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Weak Areas Chart
            st.markdown("#### 📉 Weak Areas Analysis")
            
            fig4 = px.bar(
                df_weak,
                x='Topic',
                y='Weak Students',
                color='Avg Score',
                color_continuous_scale='RdYlGn_r',
                text='Weak Students'
            )
            
            fig4.update_layout(
                xaxis_title="Topic",
                yaxis_title="Students Struggling",
                plot_bgcolor='white',
                height=400
            )
            
            st.plotly_chart(fig4, use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 Improvement Recommendations")
        
        rec_cols = st.columns(3)
        
        recommendations = [
            ("📚", "Algebra Review", "Schedule 2 extra classes on quadratic equations"),
            ("🎯", "Calculus Practice", "Assign additional problem sets on derivatives"),
            ("🤖", "AI Tutoring", "Enable personalized AI practice sessions")
        ]
        
        for idx, (icon, title, desc) in enumerate(recommendations):
            with rec_cols[idx]:
                st.markdown(f"""
                <div class="pro-card">
                    <div style="font-size: 2rem; margin-bottom: 12px; color: #6366F1;">{icon}</div>
                    <h4 style="margin: 0 0 8px 0;">{title}</h4>
                    <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# 📥 EXPORT OPTIONS
# ============================================
st.markdown("---")
st.markdown("### 📥 Export Results")

if 'results' in st.session_state:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV Export
        if st.button("📊 Export as CSV", use_container_width=True):
            df_results = pd.DataFrame(st.session_state.results)
            csv = df_results.to_csv(index=False)
            
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="smartscan_results.csv",
                mime="text/csv",
                key="csv_download"
            )
    
    with col2:
        # Summary Report
        if st.button("📄 Generate Summary", use_container_width=True):
            st.success("Report generated! (Simulation)")
    
    with col3:
        # Print Results
        if st.button("🖨️ Print Results", use_container_width=True):
            st.info("Ready for printing")

# ============================================
# 🔧 INITIALIZE SESSION STATE
# ============================================
if 'results' not in st.session_state:
    st.session_state.results = None
if 'comparison_started' not in st.session_state:
    st.session_state.comparison_started = False

# ============================================
# 📱 MOBILE OPTIMIZATION
# ============================================
st.markdown("""
<script>
    // Mobile viewport optimization
    const meta = document.createElement('meta');
    meta.name = 'viewport';
    meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
    document.getElementsByTagName('head')[0].appendChild(meta);
</script>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container
