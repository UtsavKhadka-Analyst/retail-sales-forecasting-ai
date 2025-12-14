import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
from datetime import datetime

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
# 2. ADVANCED CSS STYLING (The "Figma" Look)
# ==========================================
st.markdown("""
    <style>
    /* IMPORT GOOGLE FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* GLOBAL THEME */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* MAIN BACKGROUND */
    .stApp {
        background: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
    }

    /* CUSTOM CARDS (Glassmorphism) */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* TEXT STYLING */
    h1 {
        background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }
    h3 {
        color: #495057;
        font-weight: 600;
    }
    
    /* CUSTOM BUTTONS */
    .stButton > button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(42, 82, 152, 0.4);
        transform: scale(1.02);
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #f1f3f5;
    }
    
    /* TABS STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #495057;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e3f2fd;
        color: #1e3c72;
    }
    
    /* CHAT BUBBLES */
    .chat-user {
        background-color: #1e3c72;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        display: inline-block;
    }
    .chat-bot {
        background-color: #f1f3f5;
        color: #333;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin-bottom: 10px;
        border: 1px solid #e9ecef;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. ROBUST DATA LOGIC
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
# 4. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Custom Toggle Switch Styling
    data_source = st.radio(
        "Data Source", 
        ["Use Demo Data (GitHub)", "Upload Custom Files"],
        label_visibility="collapsed"
    )
    
    if data_source == "Use Demo Data (GitHub)":
        st.success("🟢 Demo Mode Active")
    else:
        st.warning("🟠 Custom Mode Active")

    st.markdown("---")
    
    st.markdown("### 🔑 AI Access")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    with st.expander("ℹ️ How it works"):
        st.caption("This system separates heavy computation (Colab) from visualization (Streamlit) for maximum performance.")

# ==========================================
# 5. DATA LOADING
# ==========================================
if data_source == "Use Demo Data (GitHub)":
    forecast_df, anomalies_df, summary_context = load_demo_data()
    if forecast_df is None:
        st.error("⚠️ System Error: Demo files not found in repository.")
        st.stop()
else:
    st.markdown("#### 📂 Upload Processed Data")
    col_u1, col_u2 = st.columns(2)
    up_f = col_u1.file_uploader("Forecast CSV", type="csv")
    up_a = col_u2.file_uploader("Anomalies CSV", type="csv")
    up_s = st.file_uploader("Summary MD", type="md")
    
    if up_f and up_a and up_s:
        forecast_df, anomalies_df, summary_context = load_uploaded_data(up_f, up_a, up_s)
    else:
        st.info("Waiting for files...")
        st.stop()

# Date Conversion
forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
anomalies_df['Date'] = pd.to_datetime(anomalies_df['Date'])

# ==========================================
# 6. MAIN INTERFACE
# ==========================================
st.title("🛍️ Retail AI Analyst")
st.markdown("**Hybrid Forecasting (Prophet + LSTM)** • *v2.0 Enterprise Edition*")
st.markdown("---")

# Navigation Tabs
tab_dash, tab_chat, tab_data = st.tabs(["📊 Executive Dashboard", "🤖 AI Consultant", "💾 Data Center"])

# --- TAB 1: EXECUTIVE DASHBOARD ---
with tab_dash:
    # 1. Custom Metric Cards (HTML/CSS Injection)
    avg_sales = forecast_df['Hybrid'].mean()
    next_week = forecast_df['Hybrid'].iloc[0]
    total_anoms = len(anomalies_df)
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    def display_card(title, value, subtext, col):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <p style="font-size: 14px; color: #6c757d; margin: 0;">{title}</p>
                <h2 style="font-size: 32px; margin: 5px 0; color: #1e3c72;">{value}</h2>
                <p style="font-size: 12px; color: #28a745; margin: 0;">{subtext}</p>
            </div>
            """, unsafe_allow_html=True)

    display_card("Projected Avg Sales", f"${avg_sales:,.0f}", "↑ 4.2% vs Last Quarter", col_kpi1)
    display_card("Next Week Forecast", f"${next_week:,.0f}", "Immediate Demand", col_kpi2)
    display_card("Critical Anomalies", str(total_anoms), "Requires Attention", col_kpi3)
    
    st.write("") # Spacer

    # 2. Main Chart Area
    st.subheader("📈 Forecast Trajectory")
    
    # Interactive Controls
    col_c1, col_c2 = st.columns([3, 1])
    with col_c2:
        view_mode = st.selectbox("View Layer", ["Hybrid (Recommended)", "All Models", "Anomalies Only"])
    
    # Advanced Plotly Chart
    fig = go.Figure()
    
    if view_mode == "All Models":
        fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Prophet'], name='Prophet', line=dict(color='#a5b4fc', width=2, dash='dot')))
        fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['LSTM'], name='LSTM', line=dict(color='#fca5a5', width=2, dash='dot')))
    
    # Main Hybrid Line (Always visible unless Anomalies Only)
    if view_mode != "Anomalies Only":
        fig.add_trace(go.Scatter(
            x=forecast_df['Date'], y=forecast_df['Hybrid'], 
            name='Hybrid Forecast',
            line=dict(color='#1e3c72', width=4),
            fill='tozeroy',
            fillcolor='rgba(30, 60, 114, 0.05)'
        ))
    
    # Anomalies
    fig.add_trace(go.Scatter(
        x=anomalies_df['Date'], y=anomalies_df['Weekly_Sales'],
        mode='markers', name='Anomaly',
        marker=dict(color='#ef4444', size=12, symbol='diamond', line=dict(color='white', width=2))
    ))

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=0, b=0),
        height=450,
        legend=dict(orientation="h", y=1.1, x=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: AI CONSULTANT ---
with tab_chat:
    col_chat_main, col_chat_sidebar = st.columns([2, 1])
    
    with col_chat_sidebar:
        st.markdown("""
        <div class="metric-card">
            <h4>💡 Quick Prompts</h4>
            <ul style="padding-left: 20px; font-size: 14px;">
                <li>"Why is there a spike in Dec?"</li>
                <li>"Compare Prophet vs LSTM."</li>
                <li>"Summarize the risk factors."</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_chat_main:
        if not api_key:
            st.warning("🔐 Please enter your OpenAI API Key in the settings sidebar.")
        else:
            client = OpenAI(api_key=api_key)
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "system", "content": f"Context: {summary_context}"}]

            for msg in st.session_state.messages:
                if msg["role"] != "system":
                    # Custom HTML for Chat Bubbles
                    div_class = "chat-user" if msg["role"] == "user" else "chat-bot"
                    align = "text-align: right;" if msg["role"] == "user" else ""
                    st.markdown(f"<div style='{align}'><div class='{div_class}'>{msg['content']}</div></div>", unsafe_allow_html=True)

            if prompt := st.chat_input("Ask the AI analyst..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.markdown(f"<div style='text-align: right;'><div class='chat-user'>{prompt}</div></div>", unsafe_allow_html=True)
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    ai_reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                    st.markdown(f"<div><div class='chat-bot'>{ai_reply}</div></div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- TAB 3: DATA CENTER ---
with tab_data:
    st.subheader("💾 Export & Downloads")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("##### Forecast Data")
        st.dataframe(forecast_df.head(), use_container_width=True)
        st.download_button("Download CSV", forecast_df.to_csv(), "forecast.csv", "text/csv")
        
    with col_d2:
        st.markdown("##### Anomalies List")
        st.dataframe(anomalies_df.head(), use_container_width=True)
        st.download_button("Download CSV", anomalies_df.to_csv(), "anomalies.csv", "text/csv")
