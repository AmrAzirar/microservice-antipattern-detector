import streamlit as st
import zipfile
import tempfile
import os
import shutil
from pathlib import Path
from main import run_detection_return

# Configuration de la page
st.set_page_config(
    page_title="Antipattern Detector - Microservices Analysis",
    page_icon="⚙️",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    
    .main-header p {
        font-size: 1.125rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Quality Gate */
    .quality-gate {
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        font-size: 1.125rem;
        font-weight: 600;
        margin: 2rem 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .quality-pass {
        background: #10b981;
        color: white;
        border: 2px solid #059669;
    }
    
    .quality-fail {
        background: #ef4444;
        color: white;
        border: 2px solid #dc2626;
    }
    
    /* Score colors */
    .score-excellent {
        color: #10b981;
    }
    
    .score-good {
        color: #f59e0b;
    }
    
    .score-poor {
        color: #ef4444;
    }
    
    /* Streamlit overrides */
    .stButton>button {
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    .stDownloadButton>button {
        font-weight: 600;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    
    /* Info/success boxes */
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Anti-patterns Detection")
    
    antipatterns = [
        ("Shared Database", "CRITICAL"),
        ("Cyclic Dependencies", "CRITICAL"),
        ("God Service", "CRITICAL"),
        ("Hardcoded Endpoints", "CRITICAL"),
        ("Nano Service", "WARNING")
    ]
    
    for pattern, severity in antipatterns:
        if severity == "CRITICAL":
            st.markdown(f'<span style="color: #ef4444; font-weight: 600;">●</span> **{pattern}**', unsafe_allow_html=True)
        else:
            st.markdown(f'<span style="color: #f59e0b; font-weight: 600;">●</span> **{pattern}**', unsafe_allow_html=True)
        st.caption(severity)
    
    st.markdown("---")
    st.markdown("#### Scientific Reference")
    st.caption("Based on Taibi & Lenarduzzi (2020)")
    st.caption("*Microservices Anti-Patterns: A Taxonomy*")
    
    st.markdown("---")
    st.markdown("#### Resources")
    st.markdown("[GitHub Repository](https://github.com/AmrAzirar/microservice-antipattern-detector)")

# Header
st.markdown("""
<div class="main-header">
    <h1>Antipattern Detector</h1>
    <p>Static Analysis for Microservices Architecture</p>
</div>
""", unsafe_allow_html=True)

# Upload section
st.markdown("### Project Upload")
uploaded_file = st.file_uploader(
    "Select a ZIP file containing your microservices project",
    type=['zip'],
    help="The ZIP must contain docker-compose.yml and/or service directories with OpenAPI/Java code"
)

if uploaded_file is not None:
    if st.button("Analyze", type="primary", use_container_width=True):
        with st.spinner("Analysis in progress..."):
            # Créer un dossier temporaire
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extraire le ZIP
                zip_path = os.path.join(temp_dir, "project.zip")
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                extract_path = os.path.join(temp_dir, "extracted")
                os.makedirs(extract_path, exist_ok=True)
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                # Analyser
                try:
                    violations = run_detection_return(extract_path)
                    
                    # Calculer le score
                    criticals = [v for v in violations if v["severity"] == "CRITICAL"]
                    warnings = [v for v in violations if v["severity"] == "WARNING"]
                    score = max(0, 100 - (len(criticals) * 20) - (len(warnings) * 10))
                    
                    # Quality Gate
                    quality_gate_passed = len(criticals) == 0
                    
                    st.success("Analysis completed successfully")
                    
                    # Score
                    st.markdown("### Architectural Score")
                    
                    if score >= 80:
                        score_class = "score-excellent"
                    elif score >= 50:
                        score_class = "score-good"
                    else:
                        score_class = "score-poor"
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f'<div style="text-align: center;"><span class="{score_class}" style="font-size: 4rem; font-weight: 700;">{score}</span><span style="font-size: 2rem; color: #666;">/100</span></div>', unsafe_allow_html=True)
                        st.progress(score / 100)
                    
                    # Métriques
                    st.markdown("### Metrics")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Critical", len(criticals))
                    
                    with col2:
                        st.metric("Warning", len(warnings))
                    
                    with col3:
                        st.metric("Total", len(violations))
                    
                    # Quality Gate
                    if quality_gate_passed:
                        st.markdown('<div class="quality-gate quality-pass">QUALITY GATE PASSED</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="quality-gate quality-fail">QUALITY GATE FAILED</div>', unsafe_allow_html=True)
                    
                    # Violations
                    if violations:
                        st.markdown("### Detected Violations")
                        
                        for i, v in enumerate(violations):
                            severity_badge = "CRITICAL" if v["severity"] == "CRITICAL" else "WARNING"
                            severity_color = "#ef4444" if v["severity"] == "CRITICAL" else "#f59e0b"
                            
                            with st.expander(f"{v['type']} — {severity_badge}", expanded=(i < 3)):
                                st.markdown(f"**Message:** {v['message']}")
                                st.markdown(f"**Affected Services:** {', '.join(v['services'])}")
                                if v.get('source'):
                                    st.markdown(f"**Source:** `{v['source']}`")
                    else:
                        st.success("No anti-patterns detected. Your architecture is clean.")
                    
                    # Télécharger le rapport
                    st.markdown("---")
                    report_path = "report.html"
                    if os.path.exists(report_path):
                        with open(report_path, "rb") as f:
                            st.download_button(
                                label="Download HTML Report",
                                data=f.read(),
                                file_name="antipattern-report.html",
                                mime="text/html",
                                use_container_width=True
                            )
                
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")
else:
    # Message d'accueil
    st.info("Upload a ZIP file of your microservices project to start the analysis")
    
    st.markdown("### How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 1. Upload")
        st.markdown("Upload a ZIP containing your project")
    
    with col2:
        st.markdown("#### 2. Analysis")
        st.markdown("Automatic anti-pattern detection")
    
    with col3:
        st.markdown("#### 3. Report")
        st.markdown("Score + violations + recommendations")
    
    st.markdown("---")
    st.markdown("### Expected ZIP Structure")
    st.code("""
microservices-project.zip
├── docker-compose.yml
├── service-a/
│   ├── openapi.yaml
│   └── src/
│       └── *.java
├── service-b/
│   └── application.properties
└── ...
    """, language="text")
