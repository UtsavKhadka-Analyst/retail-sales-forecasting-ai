import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from openai import OpenAI
from datetime import datetime
import io

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION - Optimized for UX Portfolio & Epic Design Principles
# ═══════════════════════════════════════════════════════════════════════════
CONFIG = {
    "MAX_CHAT_HISTORY": 10,
    "OPENAI_MODEL": "gpt-3.5-turbo",
    "MAX_TOKENS": 500,
}

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Retail AI Analytics Pro",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# PROFESSIONAL UX-FOCUSED CSS DESIGN
# Design Principles: Clarity, Contrast, Accessibility, Joy to Use
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    /* ===== GOOGLE FONTS - Professional Typography ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* ===== GLOBAL THEME - Clean Professional Background ===== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a1929 0%, #1a2332 50%, #132030 100%);
        color: #e3f2fd;
    }
    
    /* ===== MAIN CONTENT CONTAINER - Improved Readability ===== */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* ===== HEADER STYLING - Professional Button-like Headers ===== */
    h1 {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        color: #ffffff !important;
        padding: 24px 32px;
        border-radius: 16px;
        margin: 0 0 24px 0 !important;
        box-shadow: 
            0 10px 30px rgba(21, 101, 192, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.1);
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
        letter-spacing: -0.5px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    h1:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 15px 40px rgba(21, 101, 192, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    h2 {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        color: #ffffff !important;
        padding: 16px 24px;
        border-radius: 12px;
        margin: 32px 0 16px 0 !important;
        box-shadow: 
            0 6px 20px rgba(25, 118, 210, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-weight: 700;
        font-size: 1.6rem;
        transition: all 0.2s ease;
    }
    
    h2:hover {
        transform: translateX(4px);
        box-shadow: 
            0 8px 25px rgba(25, 118, 210, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    h3 {
        background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
        color: #ffffff !important;
        padding: 12px 20px;
        border-radius: 10px;
        margin: 24px 0 12px 0 !important;
        box-shadow: 
            0 4px 15px rgba(66, 165, 245, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        font-weight: 600;
        font-size: 1.3rem;
        transition: all 0.2s ease;
    }
    
    h3:hover {
        box-shadow: 
            0 6px 20px rgba(66, 165, 245, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* ===== METRIC CARDS - High Contrast for Readability ===== */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%) !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 
            0 8px 24px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stMetric:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 
            0 16px 40px rgba(255, 152, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 1) !important;
        border-color: #ff9800 !important;
    }
    
    .stMetric label {
        color: #616161 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin-bottom: 8px !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #0d47a1 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: #2e7d32 !important;
        font-weight: 600 !important;
    }
    
    /* ===== BUTTONS - Clear Call-to-Actions ===== */
    .stButton > button {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 
            0 6px 20px rgba(255, 152, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 10px 30px rgba(255, 152, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #fb8c00 0%, #ef6c00 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 
            0 4px 12px rgba(255, 152, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* ===== SIDEBAR - Professional Navigation ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2332 0%, #0f1b2d 100%);
        border-right: 2px solid rgba(255, 152, 0, 0.2);
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e3f2fd;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 1.1rem;
        padding: 10px 16px;
        margin: 12px 0 !important;
    }
    
    /* ===== TABS - Clear Section Navigation ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.05);
        padding: 12px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        color: #b0bec5;
        font-weight: 600;
        font-size: 1.05rem;
        border: 2px solid transparent;
        transition: all 0.2s ease;
        padding: 0 24px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 152, 0, 0.15);
        color: #ff9800;
        border-color: rgba(255, 152, 0, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        color: #ffffff;
        border-color: #1565c0;
        box-shadow: 
            0 6px 20px rgba(21, 101, 192, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* ===== INPUT FIELDS - Clear User Interaction ===== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stDateInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
        color: #212121 !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stDateInput > div > div > input:focus {
        border-color: #1565c0 !important;
        box-shadow: 0 0 0 3px rgba(21, 101, 192, 0.1) !important;
        background: #ffffff !important;
    }
    
    /* ===== CHAT MESSAGES - Clear Communication ===== */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin: 8px 0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%) !important;
        border-color: #1565c0 !important;
        color: #ffffff !important;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: #ffffff !important;
        border-color: #e0e0e0 !important;
        color: #212121 !important;
    }
    
    /* ===== DATAFRAME - Professional Data Display ===== */
    .stDataFrame {
        background: #ffffff;
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* ===== EXPANDER - Clear Expandable Sections ===== */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        color: #1565c0 !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #ffffff !important;
        border-color: #1565c0 !important;
        box-shadow: 0 4px 12px rgba(21, 101, 192, 0.15) !important;
    }
    
    /* ===== FILE UPLOADER - Clear Upload Interface ===== */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.95);
        border: 2px dashed #bdbdbd;
        border-radius: 12px;
        padding: 24px;
        transition: all 0.2s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #1565c0;
        background: #ffffff;
        box-shadow: 0 4px 16px rgba(21, 101, 192, 0.1);
    }
    
    /* ===== ALERTS - Clear Feedback ===== */
    .stSuccess {
        background: #e8f5e9 !important;
        border-left: 4px solid #4caf50 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        color: #1b5e20 !important;
    }
    
    .stError {
        background: #ffebee !important;
        border-left: 4px solid #f44336 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        color: #b71c1c !important;
    }
    
    .stWarning {
        background: #fff3e0 !important;
        border-left: 4px solid #ff9800 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        color: #e65100 !important;
    }
    
    .stInfo {
        background: #e3f2fd !important;
        border-left: 4px solid #2196f3 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        color: #0d47a1 !important;
    }
    
    /* ===== SCROLLBAR - Subtle but Usable ===== */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1565c0, #0d47a1);
        border-radius: 6px;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1976d2, #1565c0);
    }
    
    /* ===== ACCESSIBILITY - Focus Indicators ===== */
    *:focus-visible {
        outline: 3px solid #1565c0;
        outline-offset: 2px;
    }
    
    /* ===== LOADING SPINNER ===== */
    .stSpinner > div {
        border-top-color: #1565c0 !important;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        h1 { font-size: 1.6rem; padding: 16px 20px; }
        h2 { font-size: 1.3rem; padding: 12px 16px; }
        h3 { font-size: 1.1rem; padding: 10px 14px; }
        .stMetric [data-testid="stMetricValue"] { font-size: 1.6rem !important; }
        .main .block-container { padding: 1rem; }
    }
    
    /* ===== SUBTITLE STYLING ===== */
    .subtitle {
        text-align: center;
        color: #90caf9;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: -16px;
        margin-bottom: 24px;
        padding: 12px 24px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        display: inline-block;
        width: 100%;
    }
    
    .caption-text {
        text-align: center;
        color: #b0bec5;
        font-size: 0.9rem;
        margin: -8px 0 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_demo_data():
    """Load demo data with error handling."""
    try:
        df_f = pd.read_csv("forecast_results.csv")
        df_a = pd.read_csv("anomalies.csv")
        try:
            with open("summary.md", "r") as f:
                txt = f.read()
        except:
            txt = "Summary not available."
        return df_f, df_a, txt, None
    except FileNotFoundError as e:
        return None, None, None, f"Demo files not found: {str(e)}"
    except Exception as e:
        return None, None, None, f"Error loading demo data: {str(e)}"

def load_uploaded_data(up_f, up_a, up_s):
    """Load uploaded data with validation."""
    try:
        if not (up_f and up_a):
            return None, None, None, "Please upload all required files"
        
        df_f = pd.read_csv(up_f)
        df_a = pd.read_csv(up_a)
        txt = up_s.read().decode("utf-8") if up_s else "No summary provided."
        
        return df_f, df_a, txt, None
    except Exception as e:
        return None, None, None, f"Error loading uploaded data: {str(e)}"

def export_to_excel(forecast_df, anomalies_df):
    """Export data to Excel with multiple sheets."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        forecast_df.to_excel(writer, sheet_name='Forecasts', index=False)
        anomalies_df.to_excel(writer, sheet_name='Anomalies', index=False)
    return output.getvalue()

@st.cache_resource
def get_openai_client(api_key):
    """Cached OpenAI client."""
    if api_key:
        return OpenAI(api_key=api_key)
    return None

def trim_chat_history(messages, max_messages=10):
    """Keep only recent messages to save tokens."""
    if len(messages) <= max_messages + 1:
        return messages
    return [messages[0]] + messages[-(max_messages):]

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ⚙️ Configuration Panel")
    
    data_source = st.radio(
        "📂 Data Source:", 
        ["Demo Data", "Upload Files"],
        help="Choose your data source"
    )
    
    st.divider()
    
    st.markdown("### 🤖 AI Assistant")
    api_key = st.text_input(
        "OpenAI API Key:", 
        type="password",
        help="Your key is secure",
        placeholder="sk-..."
    )
    
    if api_key:
        st.success("✅ API Connected", icon="🔑")
        
        with st.expander("💰 Token Settings"):
            max_history = st.slider(
                "Chat History", 
                5, 20, CONFIG["MAX_CHAT_HISTORY"],
                help="Messages to keep"
            )
            max_tokens = st.slider(
                "Max Tokens",
                100, 1000, CONFIG["MAX_TOKENS"],
                help="Response length"
            )
            CONFIG["MAX_CHAT_HISTORY"] = max_history
            CONFIG["MAX_TOKENS"] = max_tokens
    
    st.divider()
    
    st.markdown("### 📊 Display Options")
    show_grid = st.checkbox("Show Grid Lines", value=True)
    show_legend = st.checkbox("Show Legend", value=True)
    
    st.divider()
    st.caption("💡 **Tip:** Adjust settings for optimal experience")

# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════

with st.spinner("🔄 Loading data..."):
    if data_source == "Demo Data":
        forecast_df, anomalies_df, summary_context, error = load_demo_data()
        if error:
            st.error(f"⚠️ {error}", icon="❌")
            st.info("💡 Switch to 'Upload Files' mode or check your repository.")
            st.stop()
    else:
        st.markdown("### 📤 Upload Data Files")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            up_f = st.file_uploader("Forecast CSV", type="csv")
        with col2:
            up_a = st.file_uploader("Anomalies CSV", type="csv")
        with col3:
            up_s = st.file_uploader("Summary (Optional)", type=["md", "txt"])
        
        forecast_df, anomalies_df, summary_context, error = load_uploaded_data(up_f, up_a, up_s)
        
        if error:
            st.error(f"⚠️ {error}", icon="❌")
            st.stop()

# Preprocess data
try:
    forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
    anomalies_df['Date'] = pd.to_datetime(anomalies_df['Date'])
    forecast_df = forecast_df.sort_values('Date').reset_index(drop=True)
    anomalies_df = anomalies_df.sort_values('Date').reset_index(drop=True)
    st.success("✅ Data validated successfully!", icon="🎉")
except Exception as e:
    st.error(f"❌ Error: {str(e)}", icon="⚠️")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("# 🛍️ Retail AI Analytics Platform")
st.markdown('<p class="subtitle">Hybrid Forecasting Engine • Prophet + LSTM Neural Networks</p>', unsafe_allow_html=True)

date_range = f"{forecast_df['Date'].min().strftime('%Y-%m-%d')} to {forecast_df['Date'].max().strftime('%Y-%m-%d')}"
st.markdown(f'<p class="caption-text">📅 Analysis Period: {date_range}</p>', unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ═══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 AI Assistant", "📥 Data Export"])

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("## 📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    avg_sales = forecast_df['Hybrid'].mean()
    next_week = forecast_df['Hybrid'].iloc[0]
    max_forecast = forecast_df['Hybrid'].max()
    min_forecast = forecast_df['Hybrid'].min()
    total_anoms = len(anomalies_df)
    
    col1.metric("Average", f"${avg_sales:,.0f}")
    col2.metric("Next Week", f"${next_week:,.0f}")
    col3.metric("Peak", f"${max_forecast:,.0f}")
    col4.metric("Trough", f"${min_forecast:,.0f}")
    col5.metric("⚠️ Anomalies", f"{total_anoms}")
    
    st.markdown("---")
    
    # Date Filter
    st.markdown("## 📅 Time Period Filter")
    col_d1, col_d2, col_d3 = st.columns([2, 2, 1])
    
    min_date = forecast_df['Date'].min().date()
    max_date = forecast_df['Date'].max().date()
    
    with col_d1:
        start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    with col_d2:
        end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
    with col_d3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
    
    # Filter data
    mask = (forecast_df['Date'].dt.date >= start_date) & (forecast_df['Date'].dt.date <= end_date)
    filtered_forecast = forecast_df[mask]
    filtered_anomalies = anomalies_df[
        (anomalies_df['Date'].dt.date >= start_date) & 
        (anomalies_df['Date'].dt.date <= end_date)
    ]
    
    st.markdown("---")
    
    # Main Chart
    st.markdown("## 📊 Sales Forecast Visualization")
    
    # View mode selector
    col_v1, col_v2 = st.columns([3, 1])
    with col_v2:
        view_mode = st.selectbox(
            "Chart View:",
            ["Hybrid Only", "All Models", "With Anomalies"],
            index=2
        )
    
    # Create chart with optimal colors for dark blue background
    fig = go.Figure()
    
    # Add models based on view mode
    if view_mode == "All Models" or view_mode == "With Anomalies":
        # Prophet - Light Blue (visible on dark background)
        fig.add_trace(go.Scatter(
            x=filtered_forecast['Date'],
            y=filtered_forecast['Prophet'],
            name='Prophet Model',
            line=dict(color='#64B5F6', width=2, dash='dot'),
            hovertemplate='<b>Prophet</b><br>Date: %{x}<br>Sales: $%{y:,.0f}<extra></extra>'
        ))
        
        # LSTM - Orange (high contrast)
        fig.add_trace(go.Scatter(
            x=filtered_forecast['Date'],
            y=filtered_forecast['LSTM'],
            name='LSTM Model',
            line=dict(color='#FF9800', width=2, dash='dash'),
            hovertemplate='<b>LSTM</b><br>Date: %{x}<br>Sales: $%{y:,.0f}<extra></extra>'
        ))
    
    # Hybrid - White/Light (main focus, always visible)
    fig.add_trace(go.Scatter(
        x=filtered_forecast['Date'],
        y=filtered_forecast['Hybrid'],
        name='Hybrid Forecast',
        line=dict(color='#FFFFFF', width=4),
        fill='tozeroy',
        fillcolor='rgba(255, 255, 255, 0.1)',
        hovertemplate='<b>Hybrid Forecast</b><br>Date: %{x}<br>Sales: $%{y:,.0f}<extra></extra>'
    ))
    
    # Add anomalies if selected
    if view_mode == "With Anomalies" and not filtered_anomalies.empty:
        fig.add_trace(go.Scatter(
            x=filtered_anomalies['Date'],
            y=filtered_anomalies['Weekly_Sales'],
            mode='markers',
            name='Anomaly Detected',
            marker=dict(
                color='#FF5252',
                size=14,
                symbol='x',
                line=dict(width=2, color='#FFFFFF')
            ),
            hovertemplate='<b>⚠️ Anomaly</b><br>Date: %{x}<br>Sales: $%{y:,.0f}<extra></extra>'
        ))
    
    # Chart layout - optimized for dark blue background with high contrast
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(13, 25, 41, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=550,
        hovermode='x unified',
        showlegend=show_legend,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor='rgba(255, 255, 255, 0.1)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1,
            font=dict(color='#FFFFFF', size=11)
        ),
        margin=dict(l=60, r=40, t=40, b=60)
    )
    
    # Update axes separately
    fig.update_xaxes(
        title='Date',
        title_font=dict(color='#FFFFFF', size=14),
        tickfont=dict(color='#E3F2FD', size=11),
        showgrid=show_grid,
        gridcolor='rgba(255, 255, 255, 0.1)',
        gridwidth=1,
        zeroline=False
    )
    
    fig.update_yaxes(
        title='Weekly Sales ($)',
        title_font=dict(color='#FFFFFF', size=14),
        tickfont=dict(color='#E3F2FD', size=11),
        showgrid=show_grid,
        gridcolor='rgba(255, 255, 255, 0.1)',
        gridwidth=1,
        zeroline=False
    )
    
    st.plotly_chart(fig, use_container_width=True, key="main_chart")
    
    # Download chart
    col_dl1, col_dl2 = st.columns([3, 1])
    with col_dl2:
        try:
            img_bytes = fig.to_image(format="png", width=1400, height=700)
            st.download_button(
                "📸 Download Chart",
                data=img_bytes,
                file_name=f"forecast_{datetime.now().strftime('%Y%m%d')}.png",
                mime="image/png",
                use_container_width=True
            )
        except:
            st.caption("Install kaleido for chart export: pip install kaleido")
    
    st.markdown("---")
    
    # Data Tables
    st.markdown("## 📋 Data Tables")
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        with st.expander("📊 Forecast Data", expanded=False):
            st.dataframe(
                filtered_forecast.style.format({
                    "Prophet": "${:,.2f}",
                    "LSTM": "${:,.2f}",
                    "Hybrid": "${:,.2f}"
                }),
                use_container_width=True,
                height=300
            )
    
    with col_t2:
        with st.expander("⚠️ Anomalies Detected", expanded=False):
            if not filtered_anomalies.empty:
                st.dataframe(
                    filtered_anomalies.style.format({
                        "Weekly_Sales": "${:,.2f}"
                    }),
                    use_container_width=True,
                    height=300
                )
            else:
                st.info("No anomalies in selected period")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: AI ASSISTANT
# ═══════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("## 💬 AI Business Analyst")
    
    col_chat1, col_chat2 = st.columns([2, 1])
    
    with col_chat2:
        st.markdown("### 💡 Sample Questions")
        st.info("""
        - "Summarize the forecast trends"
        - "What caused the anomalies?"
        - "Compare Prophet vs LSTM"
        - "What's the sales outlook?"
        - "Identify seasonal patterns"
        - "Risk factors to watch?"
        """)
        
        if api_key and "messages" in st.session_state:
            msg_count = len([m for m in st.session_state.messages if m["role"] != "system"])
            est_tokens = msg_count * 150
            est_cost = (est_tokens / 1000) * 0.002
            
            st.metric("Messages Sent", msg_count)
            st.metric("Est. Cost", f"${est_cost:.4f}")
        
        if st.button("🔄 Clear Chat", use_container_width=True):
            if "messages" in st.session_state:
                st.session_state.messages = [st.session_state.messages[0]]
                st.success("Chat cleared!")
                st.rerun()
    
    with col_chat1:
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to use the AI assistant.")
            st.markdown("""
            **Why do I need an API key?**
            - Direct communication with OpenAI's GPT models
            - You control your usage and costs
            - Secure - no intermediary storage
            
            **Get your key:** [OpenAI Platform](https://platform.openai.com/api-keys)
            """)
        else:
            client = get_openai_client(api_key)
            
            if not client:
                st.error("❌ Failed to initialize OpenAI client. Check your API key.")
            else:
                # Initialize chat
                if "messages" not in st.session_state:
                    system_prompt = f"""You are an expert retail data analyst. Answer questions concisely and professionally.

REPORT CONTEXT:
{summary_context}

DATA SUMMARY:
- Forecast Period: {date_range}
- Average Forecast: ${avg_sales:,.0f}
- Total Anomalies: {total_anoms}
- Models Used: Prophet, LSTM, Hybrid Ensemble

Be concise (2-3 paragraphs max), use bullet points when appropriate, and provide actionable insights.
"""
                    st.session_state.messages = [{"role": "system", "content": system_prompt}]
                
                # Display chat
                for message in st.session_state.messages:
                    if message["role"] != "system":
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])
                
                # User input
                if prompt := st.chat_input("Ask about the forecast data..."):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    
                    # Generate response
                    with st.chat_message("assistant"):
                        try:
                            trimmed_messages = trim_chat_history(
                                st.session_state.messages,
                                CONFIG["MAX_CHAT_HISTORY"]
                            )
                            
                            with st.spinner("Analyzing..."):
                                stream = client.chat.completions.create(
                                    model=CONFIG["OPENAI_MODEL"],
                                    messages=[
                                        {"role": m["role"], "content": m["content"]} 
                                        for m in trimmed_messages
                                    ],
                                    max_tokens=CONFIG["MAX_TOKENS"],
                                    stream=True,
                                )
                                response = st.write_stream(stream)
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response
                            })
                        
                        except Exception as e:
                            error_msg = str(e)
                            if "insufficient_quota" in error_msg:
                                st.error("❌ API quota exceeded. Check your OpenAI billing.")
                            elif "invalid_api_key" in error_msg:
                                st.error("❌ Invalid API key. Please check your key.")
                            else:
                                st.error(f"❌ Error: {error_msg}")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 3: DATA EXPORT
# ═══════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("## 📥 Data Export Center")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        st.markdown("### 📊 Forecast Data")
        
        # Export to Excel
        excel_data = export_to_excel(forecast_df, anomalies_df)
        st.download_button(
            label="📥 Download Excel Report",
            data=excel_data,
            file_name=f"forecast_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        # Export forecast CSV
        csv_forecast = forecast_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Forecast CSV",
            data=csv_forecast,
            file_name=f"forecast_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.dataframe(forecast_df.head(10), use_container_width=True)
    
    with col_exp2:
        st.markdown("### ⚠️ Anomaly Data")
        
        # Export anomalies CSV
        csv_anomalies = anomalies_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Anomalies CSV",
            data=csv_anomalies,
            file_name=f"anomalies_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.dataframe(anomalies_df.head(10), use_container_width=True)
    
    st.markdown("---")
    
    # Data Summary
    st.markdown("### 📋 Data Summary")
    col_sum1, col_sum2 = st.columns(2)
    
    with col_sum1:
        st.json({
            "Total Forecast Points": len(forecast_df),
            "Date Range": date_range,
            "Average Forecast": f"${avg_sales:,.2f}",
            "Models": ["Prophet", "LSTM", "Hybrid"]
        })
    
    with col_sum2:
        st.json({
            "Total Anomalies": len(anomalies_df),
            "Data Source": data_source,
            "Last Updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #90caf9; font-size: 0.9rem;">'
    '🛍️ Retail AI Analytics Platform | '
    '🎨 UX Portfolio Project | '
    f'⏰ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    '</p>',
    unsafe_allow_html=True
)
