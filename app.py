import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Retail AI Analyst Pro",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ULTRA-MODERN CSS (ANIMATED)
# ==========================================
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* ANIMATED BACKGROUND */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* HEADER "CHECKBOX" STYLE CARDS */
    .header-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 20px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 6px solid #1e3c72;
    }
    
    .header-title {
        color: #1e3c72;
        font-weight: 800;
        font-size: 28px;
        margin: 0;
    }
    
    .header-subtitle {
        color: #555;
        font-size: 14px;
        margin-top: 5px;
    }

    /* INTERACTIVE METRIC CARDS */
    .kpi-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .kpi-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 30px rgba(0,0,0,0.2);
        border: 1px solid #23a6d5;
    }
    
    .kpi-value {
        font-size: 36px;
        font-weight: 800;
        color: #1e3c72;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 13px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* CUSTOM TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255,255,255,0.5);
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255,255,255,0.8);
        border-radius: 8px;
        border: none;
        color: #495057;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e3c72 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. DATA LOGIC (UNCHANGED)
# ==========================================
@st.cache_data
def load_demo_data():
    try:
        df_f = pd.read_csv("forecast_results.csv")
        df_a = pd.read_csv("anomalies.csv")
        with open("summary.md", "r") as f:
            txt = f.read()
        return df_f, df_a, txt
    except FileNotFoundError:
        return None, None, None

def load_uploaded_data(up_f, up_a, up_s):
    try:
        df_f = pd.read_csv(up_f)
        df_a = pd.read_csv(up_a)
        txt = up_s.read().decode("utf-8")
        return df_f, df_a, txt
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None, None

# ==========================================
# 4. SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    
    # Styled Toggle
    data_source = st.selectbox(
        "Source Selection", 
        ["Use Demo Data (GitHub)", "Upload Custom Files"],
    )
    
    st.markdown("---")
    api_key = st.text_input("🔑 OpenAI API Key", type="password")
    
    st.info("System Status: 🟢 Online")

# ==========================================
# 5. DATA LOADING
# ==========================================
if data_source == "Use Demo Data (GitHub)":
    forecast_df, anomalies_df, summary_context = load_demo_data()
    if forecast_df is None:
        st.error("⚠️ Demo files not found.")
        st.stop()
else:
    col_u1, col_u2 = st.columns(2)
    up_f = col_u1.file_uploader("Forecast CSV", type="csv")
    up_a = col_u2.file_uploader("Anomalies CSV", type="csv")
    up_s = st.file_uploader("Summary MD", type="md")
    
    if up_f and up_a and up_s:
        forecast_df, anomalies_df, summary_context = load_uploaded_data(up_f, up_a, up_s)
    else:
        st.info("Please upload files to proceed.")
        st.stop()

# Dates
forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
anomalies_df['Date'] = pd.to_datetime(anomalies_df['Date'])

# ==========================================
# 6. MAIN INTERFACE
# ==========================================

# HEADER WITH "CHECKBOX" CARD STYLE
st.markdown("""
<div class="header-card">
    <h1 class="header-title">🛍️ Retail AI Analyst Pro</h1>
    <p class="header-subtitle">Advanced Hybrid Forecasting • Prophet + LSTM • Anomaly Detection</p>
</div>
""", unsafe_allow_html=True)

tab_dash, tab_chat, tab_data = st.tabs(["📊 Live Dashboard", "🤖 AI Consultant", "💾 Data Export"])

# --- TAB 1: EXECUTIVE DASHBOARD ---
with tab_dash:
    # KPI CARDS (Interactive HTML)
    avg_sales = forecast_df['Hybrid'].mean()
    next_week = forecast_df['Hybrid'].iloc[0]
    total_anoms = len(anomalies_df)
    
    col1, col2, col3 = st.columns(3)
    
    def display_kpi(col, label, value):
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    display_kpi(col1, "Average Projected Sales", f"${avg_sales:,.0f}")
    display_kpi(col2, "Next Week Forecast", f"${next_week:,.0f}")
    display_kpi(col3, "Detected Anomalies", str(total_anoms))
    
    st.write("---")

    # MAIN CHART WITH GLASS CONTAINER
    st.markdown('<div class="header-card"><h3 style="margin:0; color:#1e3c72;">📈 Forecast Trajectory</h3></div>', unsafe_allow_html=True)
    
    view_mode = st.radio("Display Mode:", ["Hybrid View", "Detailed Comparison"], horizontal=True)
    
    fig = go.Figure()
    
    if view_mode == "Detailed Comparison":
        fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Prophet'], name='Prophet', line=dict(color='blue', dash='dot')))
        fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['LSTM'], name='LSTM', line=dict(color='orange', dash='dot')))
        
    fig.add_trace(go.Scatter(
        x=forecast_df['Date'], y=forecast_df['Hybrid'], 
        name='Hybrid Forecast',
        line=dict(color='#23d5ab', width=4),
        fill='tozeroy',
        fillcolor='rgba(35, 213, 171, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=anomalies_df['Date'], y=anomalies_df['Weekly_Sales'],
        mode='markers', name='Anomaly',
        marker=dict(color='#e73c7e', size=12, symbol='diamond')
    ))

    fig.update_layout(
        template="plotly_white",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: AI CONSULTANT ---
with tab_chat:
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.markdown('<div class="header-card"><h3 style="margin:0;">💬 Ask the Data</h3></div>', unsafe_allow_html=True)
        
        if not api_key:
            st.warning("🔐 Please enter OpenAI API Key in the sidebar.")
        else:
            client = OpenAI(api_key=api_key)
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "system", "content": f"Context: {summary_context}"}]

            for msg in st.session_state.messages:
                if msg["role"] != "system":
                    st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input("Ask about sales trends..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)

# --- TAB 3: DATA EXPORT ---
with tab_data:
    st.markdown('<div class="header-card"><h3 style="margin:0;">💾 Download Center</h3></div>', unsafe_allow_html=True)
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button("📥 Download Forecast CSV", forecast_df.to_csv(), "forecast.csv", "text/csv")
        st.dataframe(forecast_df.head())
    with col_d2:
        st.download_button("📥 Download Anomalies CSV", anomalies_df.to_csv(), "anomalies.csv", "text/csv")
        st.dataframe(anomalies_df.head())
