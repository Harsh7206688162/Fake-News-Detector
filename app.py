
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="Fake News Detector",
    layout="wide",
    page_icon="🎯",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Header Styles */
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 50%, #00f5ff 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
        letter-spacing: -0.02em;
        animation: gradient-shift 3s ease infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Card Styles */
    .card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.1), 0 0 60px rgba(255, 0, 255, 0.05);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .card:hover {
        border-color: rgba(0, 245, 255, 0.4);
        box-shadow: 0 12px 40px rgba(0, 245, 255, 0.15), 0 0 80px rgba(255, 0, 255, 0.1);
    }
    
    /* Text Area Styles - MINT/CYAN BACKGROUND */
    .stTextArea > label {
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #00f5ff !important;
        margin-bottom: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stTextArea textarea {
        background: #e3f6f5 !important;
        border: 2px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 16px !important;
        color: #000000 !important;
        font-size: 1rem !important;
        padding: 1.25rem !important;
        min-height: 400px !important;
        line-height: 1.7 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00f5ff !important;
        box-shadow: 0 0 0 3px rgba(0, 245, 255, 0.2) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }
    
    /* Button Styles */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.05em !important;
        box-shadow: 0 8px 24px rgba(0, 245, 255, 0.3) !important;
        transition: all 0.3s ease !important;
        margin-top: 1.5rem !important;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(0, 245, 255, 0.5), 0 0 40px rgba(255, 0, 255, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Result Styles */
    .result-container {
        text-align: center;
        padding: 1.5rem 0;
    }
    
    .result-verdict {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        text-transform: uppercase;
    }
    
    .verdict-real {
        color: #00ff87;
        text-shadow: 0 0 40px rgba(0, 255, 135, 0.7);
    }
    
    .verdict-fake {
        color: #ff0080;
        text-shadow: 0 0 40px rgba(255, 0, 128, 0.7);
    }
    
    .verdict-unsure {
        color: #ffaa00;
        text-shadow: 0 0 40px rgba(255, 170, 0, 0.7);
    }
    
    /* Confidence Meter */
    .confidence-container {
        margin: 2rem 0;
    }
    
    .confidence-label {
        font-size: 0.9rem;
        color: #8b9dc3;
        font-weight: 700;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        text-align: center;
    }
    
    .confidence-bar-bg {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50px;
        height: 20px;
        overflow: hidden;
        position: relative;
        border: 1px solid rgba(0, 245, 255, 0.2);
    }
    
    .confidence-bar {
        height: 100%;
        border-radius: 50px;
        transition: width 1s ease;
        position: relative;
        overflow: hidden;
    }
    
    .confidence-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .confidence-text {
        text-align: center;
        margin-top: 0.75rem;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
    }
    
    /* Reason Box */
    .reason-box {
        background: rgba(0, 245, 255, 0.05);
        border-left: 4px solid #00f5ff;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    .reason-title {
        font-size: 0.9rem;
        font-weight: 800;
        color: #00f5ff;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    .reason-text {
        font-size: 1rem;
        color: #e2e8f0;
        line-height: 1.7;
    }
    
    /* Spinner Override */
    .stSpinner > div {
        border-color: #00f5ff transparent transparent transparent !important;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #8b9dc3;
    }
    
    .empty-state-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        opacity: 0.6;
    }
    
    .empty-state-text {
        font-size: 1.2rem;
        font-weight: 500;
        color: #8b9dc3;
        line-height: 1.6;
    }
    
    /* Column styling */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1.5rem;
        color: #64748b;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

if 'result' not in st.session_state:
    st.session_state.result = None

API_URL = os.getenv("FNND_API_URL", "http://localhost:8000")

st.markdown("""
<div class="main-header">
    <div class="main-title">🎯 Fake News Detector</div>
</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns([1, 1], gap="large")


with col1:

    

    text_input = st.text_area(
        "📝 Enter News Article",
        placeholder="Paste your news article here...\n\nTip: Try articles that seem too sensational or unusual to test the detector.",
        height=400,
        key="news_input"
    )
    
    
    analyze_clicked = st.button("🔍 Analyze Article", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


with col2:
   
    if analyze_clicked and text_input.strip():
        with st.spinner(" Analyzing..."):
            try:
               
                response = requests.post(
                    f"{API_URL.rstrip('/')}/classify",
                    json={"text": text_input, "model": "llama-3.1-8b-instant"},
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    verdict = data.get("verdict", "UNSURE").upper()
                    confidence = int(data.get("confidence", 0))
                    reason = data.get("reason", "")
                    
                    
                    st.session_state.result = {
                        "verdict": verdict,
                        "confidence": confidence,
                        "reason": reason
                    }
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.session_state.result = None
                    
            except Exception as e:
                st.error(f"❌ Connection Error: {str(e)}")
                st.session_state.result = None
    
    if st.session_state.result:
        result = st.session_state.result
        verdict = result["verdict"]
        confidence = result["confidence"]
        reason = result["reason"]
        
        if verdict == "REAL":
            verdict_class = "verdict-real"
            bar_color = "linear-gradient(90deg, #00ff87 0%, #00d9ff 100%)"
        elif verdict == "FAKE":
            verdict_class = "verdict-fake"
            bar_color = "linear-gradient(90deg, #ff0080 0%, #ff00ff 100%)"
        else:
            verdict_class = "verdict-unsure"
            bar_color = "linear-gradient(90deg, #ffaa00 0%, #ff6600 100%)"
        
        
        
        
        st.markdown(f"""
        <div class="result-container">
            <div class="result-verdict {verdict_class}">{verdict}</div>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown(f"""
        <div class="confidence-container">
            <div class="confidence-label">Confidence Level</div>
            <div class="confidence-bar-bg">
                <div class="confidence-bar" style="width: {confidence}%; background: {bar_color};"></div>
            </div>
            <div class="confidence-text">{confidence}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        
        if reason:
            st.markdown(f"""
            <div class="reason-box">
                <div class="reason-title">💡 Analysis</div>
                <div class="reason-text">{reason}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        
        st.markdown("""
        <div class="card">
            <div class="empty-state">
                <div class="empty-state-icon">📰</div>
                <div class="empty-state-text">
                    Your analysis results will appear here<br><br>
                    Paste an article and click "Analyze" to get started
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("""
<div class="footer">
    • Powered by Harsh & Shubham • 
</div>
""", unsafe_allow_html=True)