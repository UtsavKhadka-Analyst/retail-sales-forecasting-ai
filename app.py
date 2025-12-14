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
# 2. ULTRA-MODERN CSS (FIXED & IMPROVED)
# ==========================================
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* ANIMATED BACKGROUND (Main App) */
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

    /* SIDEBAR STYLING (New!) */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85); /* Semi-transparent white */
        backdrop-filter: blur(12px); /* Glass blur effect */
        border-right: 1px solid rgba(255,255,255,0.5);
    }
    
    /* SIDEBAR TEXT & INPUTS */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #1e3c72;
    }
    
    /* HEADER CARDS (Fixed Width & Centered) */
    .header-container {
        display: flex;
        justify_content: center;
        margin-bottom: 20px;
    }
    
    .header-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 20px 40px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
        text-align: center;
        width: auto; /* Fits text */
        display: inline-block; /* Fits text */
    }
    
    .header-title {
        color: #1e3c72;
        font-weight: 800;
        font-size: 32px;
        margin: 0;
        background: -webkit-linear-gradient(#1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        color: #555;
        font-size: 14px;
        margin-top: 5px;
        font-weight: 500;
    }

    /* KPI CARDS (Interactive) */
    .kpi-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
        border-color: #e73c7e;
    }
    
    .kpi-value {
        font-size: 32px;
        font-weight: 800;
        color: #1e3c72;
    }
    
    .kpi-label {
        font-size: 12px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    /* CUSTOM TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.6);
        padding: 8px;
        border-radius: 12px;
        backdrop-filter: blur(5px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        border-radius: 8px;
        color: #1e3c72;
        font-weight: 600;
        flex: 1; /* Tabs stretch evenly */
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e3c72 !important;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=60)
    st.markdown("### Control Panel")
    
    # Styled Toggle
    data_source = st.selectbox(
        "Source Selection", 
        ["Use Demo Data (GitHub)", "Upload Custom Files"],
    )
    
    st.markdown("---")
    api_key = st.text_input("🔑 OpenAI API Key", type="password")
    
    st.markdown("---")
    with st.container():
        st.markdown("""
        <div style="background: rgba(30, 60, 114, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(30, 60, 114, 0.2);">
            <small style="color: #1e3c72;"><b>System Status:</b> 🟢 Online</small><br>
            <small style="color: #555;">v2.1 Enterprise Build</small>
        </div>
        """, unsafe_allow_html=True)

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

# HEADER (CENTERED & FITTED)
st.markdown("""
<div class="header-container">
    <div class="header-card">
        <h1 class="header-title">🛍️ Retail AI Analyst</h1>
        <p class="header-subtitle">Hybrid Forecasting Architecture (Prophet + LSTM)</p>
    </div>
</div>
""", unsafe_allow_html=True)

tab_dash, tab_chat, tab_data = st.tabs(["📊 Live Dashboard", "🤖 AI Consultant", "💾 Data Export"])

# --- TAB 1: EXECUTIVE DASHBOARD ---
with tab_dash:
    # KPI CARDS
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

    display_kpi(col1, "Average Sales", f"${avg_sales:,.0f}")
    display_kpi(col2, "Next Week Forecast", f"${next_week:,.0f}")
    display_kpi(col3, "Anomalies Detected", str(total_anoms))
    
    st.write("---")

    # CHART
    st.markdown('<div style="text-align: center; margin-bottom: 20px;"><span style="background: white; padding: 5px 15px; border-radius: 20px; font-weight: 600; color: #1e3c72; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">📈 Sales Trajectory</span></div>', unsafe_allow_html=True)
    
    view_mode = st.radio("Display Mode:", ["Hybrid View", "Detailed Comparison"], horizontal=True, label_visibility="collapsed")
    
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
        plot_bgcolor='rgba(255,255,255,0.5)', # Semi-transparent chart bg
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        hovermode="x unified",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center")
    )
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: AI CONSULTANT ---
with tab_chat:
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 15px;">
            <h3 style="color: #1e3c72; margin: 0;">💬 AI Business Analyst</h3>
            <p style="color: #666; font-size: 14px;">Ask questions about your sales data.</p>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        if not api_key:
            st.warning("🔐 Please enter OpenAI API Key in the sidebar.")
        else:
            client = OpenAI(api_key=api_key)
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "system", "content": f"Context: {summary_context}"}]

            for msg in st.session_state.messages:
                if msg["role"] != "system":
                    st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input("Ex: Why did sales drop in November?"):
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
    st.markdown("""
    <div class="header-container">
        <div class="header-card" style="padding: 15px 30px;">
            <h3 style="margin:0; color: #1e3c72;">💾 Data Download Center</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button("📥 Download Forecast CSV", forecast_df.to_csv(), "forecast.csv", "text/csv", use_container_width=True)
        st.dataframe(forecast_df.head(), use_container_width=True)
    with col_d2:
        st.download_button("📥 Download Anomalies CSV", anomalies_df.to_csv(), "anomalies.csv", "text/csv", use_container_width=True)
        st.dataframe(anomalies_df.head(), use_container_width=True)
