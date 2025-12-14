# streamlit_app.py
# ------------------------------------------------------------
# Visually attractive, responsive Streamlit app with Figma-style
# design, dark blue theme, interactive components, accessibility,
# feedback, navigation, and Plotly data viz.
# ------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ==========================================
# 1) PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Figma-Style Interactive App",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2) ADVANCED CSS STYLING (Dark Blue Theme)
#    - Cohesive palette, typography, hover/transition effects
#    - Responsive media queries
#    - Checkbox-styled headers and subheaders
# ==========================================
st.markdown("""
<style>
  /* IMPORT FONTS */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

  :root {
    --bg-dark: #0b1a33;           /* Deep Navy */
    --bg-dark-2: #0f2347;         /* Slightly lighter navy */
    --primary: #6dcff6;           /* Cyan accent */
    --primary-2: #5ab3d6;
    --surface: rgba(255,255,255,0.08);
    --text: #e6edf3;              /* Light text */
    --muted: #a9b3c2;
    --success: #38d9a9;
    --warning: #f59f00;
    --error: #ff6b6b;
    --card-border: rgba(255,255,255,0.18);
  }

  /* GLOBAL THEME */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* APP BACKGROUND: dark blue gradient */
  .stApp {
    background: radial-gradient(1000px 600px at 10% 10%, var(--bg-dark-2), var(--bg-dark));
  }

  /* GLASSMORPHIC CARDS */
  .glass-card {
    background: var(--surface);
    backdrop-filter: blur(12px);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35);
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
  }
  .glass-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 36px rgba(0, 0, 0, 0.45);
    border-color: rgba(255,255,255,0.28);
  }

  /* BUTTONS */
  .stButton > button {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-2) 100%);
    color: #0b1a33;
    border: none !important;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 700;
    letter-spacing: .2px;
    transition: all .25s ease;
  }
  .stButton > button:hover {
    transform: translateY(-1px) scale(1.01);
    box-shadow: 0 10px 20px rgba(109, 207, 246, 0.25);
  }
  .stButton > button:focus-visible {
    outline: 3px solid #ffffff55;
  }

  /* INPUTS */
  .stTextInput > div > div > input,
  .stNumberInput input,
  .stSelectbox > div > div > div[role="combobox"],
  .stSlider > div > div > div > div {
    color: var(--text) !important;
  }

  /* SIDEBAR */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2347, #0b1a33);
    border-right: 1px solid var(--card-border);
  }
  [data-testid="stSidebar"] * {
    color: var(--text) !important;
  }

  /* TABS */
  .stTabs [data-baseweb="tab-list"] {
    gap: 10px;
  }
  .stTabs [data-baseweb="tab"] {
    height: 48px;
    white-space: pre-wrap;
    background: var(--surface);
    border-radius: 10px;
    color: var(--muted);
    font-weight: 600;
    border: 1px solid var(--card-border);
  }
  .stTabs [aria-selected="true"] {
    color: var(--text);
    border-color: rgba(255,255,255,0.28);
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.08);
  }

  /* CHECKBOX-STYLE HEADERS */
  .check-header {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 12px;
    align-items: center;
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid var(--card-border);
    background: linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0.06));
    color: var(--text);
  }
  .check-icon {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    background: linear-gradient(180deg, var(--primary), var(--primary-2));
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #0b1a33;
    font-weight: 900;
    box-shadow: 0 4px 8px rgba(109,207,246,.25);
  }
  .check-title {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.2px;
  }
  .check-subtitle {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 10px;
    align-items: center;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px dashed rgba(255,255,255,0.18);
    color: var(--muted);
    font-weight: 700;
  }

  /* TABLE TEXT CONTRAST IMPROVEMENTS */
  .stDataFrame, .stTable {
    color: var(--text) !important;
  }

  /* ACCESSIBILITY FOCUS RING FOR KEYBOARD USERS */
  *:focus-visible {
    outline: 3px solid #ffffff55;
    outline-offset: 2px;
    border-radius: 6px;
  }

  /* RESPONSIVE MEDIA QUERIES */
  @media (max-width: 1200px) {
    .glass-card { padding: 14px; }
    .check-title { font-size: 20px; }
  }
  @media (max-width: 768px) {
    .glass-card { padding: 12px; }
    .check-title { font-size: 18px; }
    .stTabs [data-baseweb="tab"] { height: 44px; }
  }
  @media (max-width: 480px) {
    .check-title { font-size: 16px; }
    .stButton > button { width: 100%; }
  }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3) ACCESSIBILITY NOTE (non-visual)
#    - Provide concise landmarks and ARIA where possible
# ==========================================
st.markdown("<div role='region' aria-label='Main content area'></div>", unsafe_allow_html=True)

# ==========================================
# 4) SIDEBAR NAVIGATION + FEEDBACK
#    - Clear navigation
#    - Real-time interactive controls
#    - Feedback (success/warning/toast)
# ==========================================
with st.sidebar:
    st.markdown("<div class='check-header'><div class='check-icon'>✓</div><div class='check-title'>App Controls</div></div>", unsafe_allow_html=True)
    st.caption("Use these controls to personalize the experience.")

    theme_toggle = st.toggle("High contrast accents", value=True, help="Enhances visual distinction for interactive elements.")
    show_toasts = st.toggle("Show action toasts", value=True, help="Visual feedback when actions occur.")
    st.markdown("---")

    nav = st.radio(
        "Navigate to",
        ["Dashboard", "Playground", "Data"],
        help="Choose a section to explore."
    )

    st.markdown("---")
    st.markdown("<div class='check-subtitle'><div class='check-icon'>✓</div><div>Demo data options</div></div>", unsafe_allow_html=True)
    rows = st.slider("Sample rows", min_value=50, max_value=500, value=200, step=50)
    noise = st.slider("Noise level", min_value=0.0, max_value=0.5, value=0.15, step=0.05)
    category = st.selectbox("Category", ["A - Retail", "B - Finance", "C - Healthcare"])

# ==========================================
# 5) SAMPLE DATA GENERATION (fast, deterministic)
# ==========================================
np.random.seed(7)
dates = pd.date_range("2024-01-01", periods=rows, freq="D")
signal = np.sin(np.linspace(0, 6 * np.pi, rows)) * 100 + 500
noise_vec = np.random.normal(0, 1, rows) * (noise * 100)
cat_factor = {"A - Retail": 1.0, "B - Finance": 1.08, "C - Healthcare": 0.92}[category]
y = (signal + noise_vec) * cat_factor
df = pd.DataFrame({"date": dates, "value": y})

# ==========================================
# 6) HEADER AND SUBHEADER IN "CHECKBOX TYPES"
#    - Styled headers that visually resemble checkbox modules
#    - Real-time toggles to show/hide sections
# ==========================================
st.markdown("<div class='check-header'><div class='check-icon'>✓</div><div class='check-title'>Figma-style interactive application</div></div>", unsafe_allow_html=True)
st.markdown("<div class='check-subtitle'><div class='check-icon'>✓</div><div>Dark blue theme • Responsive • Accessible • Animated</div></div>", unsafe_allow_html=True)
st.markdown("---")

# Control visibility of sections via checkboxes (user interaction)
show_kpis = st.checkbox("Show KPI cards", value=True)
show_chart = st.checkbox("Show interactive chart", value=True)
show_controls = st.checkbox("Show action controls", value=True)

# Small assistive text
st.caption("Tip: Toggle the controls above to tailor the page. All components update in real time.")

# ==========================================
# 7) MAIN TABS FOR NAVIGATION
# ==========================================
tab_dash, tab_play, tab_data = st.tabs(["📊 Dashboard", "🎛️ Playground", "💾 Data"])

# -----------------------------------------------------------
# DASHBOARD TAB
# -----------------------------------------------------------
with tab_dash:
    if show_kpis:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='glass-card' role='group' aria-label='Projected metric card'>", unsafe_allow_html=True)
            st.metric(label="Projected avg", value=f"{df.value.mean():,.1f}")
            st.progress(min(1.0, max(0.0, (df.value.mean() - 480) / 80)))
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='glass-card' role='group' aria-label='Peak metric card'>", unsafe_allow_html=True)
            st.metric(label="Recent peak", value=f"{df.value.iloc[-20:].max():,.1f}")
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='glass-card' role='group' aria-label='Volatility metric card'>", unsafe_allow_html=True)
            st.metric(label="Volatility (std)", value=f"{df.value.std():,.1f}")
            st.markdown("</div>", unsafe_allow_html=True)

    st.write("")  # spacing

    if show_chart:
        st.markdown("<div class='glass-card' role='figure' aria-label='Time series chart'>", unsafe_allow_html=True)
        color = "#6dcff6" if theme_toggle else "#9adbf8"
        fig = px.line(
            df, x="date", y="value",
            title=None,
            markers=True
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e6edf3"),
            margin=dict(l=10, r=10, t=10, b=10),
            hovermode="x unified"
        )
        fig.update_traces(line=dict(color=color, width=2), marker=dict(size=4))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if show_toasts:
        st.toast("Dashboard refreshed with your settings.", icon="✅")

# -----------------------------------------------------------
# PLAYGROUND TAB (Interactive controls + feedback)
# -----------------------------------------------------------
with tab_play:
    if show_controls:
        st.markdown("<div class='glass-card' role='form' aria-label='Interactive control panel'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,1])

        with c1:
            text = st.text_input("Annotation title", "Note")
        with c2:
            thresh = st.number_input("Highlight threshold", min_value=0.0, max_value=float(df.value.max()), value=float(df.value.mean()))
        with c3:
            mode = st.selectbox("Marker mode", ["Points", "Bars", "Area"])

        st.write("")
        btn_col1, btn_col2 = st.columns([1,1])
        with btn_col1:
            add_btn = st.button("Add annotation")
        with btn_col2:
            simulate_btn = st.button("Simulate server action")

        if add_btn:
            st.success(f"Annotation “{text}” added at threshold {thresh:,.1f}.")
            if show_toasts:
                st.toast("Annotation applied.", icon="✍️")

        if simulate_btn:
            with st.spinner("Running computation…"):
                time.sleep(1.2)
            st.info("Server action completed in ~1.2s.")
            if show_toasts:
                st.toast("Completed background task.", icon="🧠")

        # A second visualization reacting to controls
        st.write("")
        st.markdown("<div class='glass-card' role='figure' aria-label='Interactive highlight chart'>", unsafe_allow_html=True)
        dfd = df.copy()
        dfd["above_thresh"] = (dfd["value"] >= thresh).astype(int)

        if mode == "Points":
            fig2 = px.scatter(dfd, x="date", y="value", color="above_thresh",
                              color_discrete_map={0: "#a9b3c2", 1: "#38d9a9"})
        elif mode == "Bars":
            fig2 = px.bar(dfd, x="date", y="value", color="above_thresh",
                          color_discrete_map={0: "#a9b3c2", 1: "#38d9a9"})
        else:
            fig2 = px.area(dfd, x="date", y="value", color="above_thresh",
                           color_discrete_map={0: "#a9b3c2", 1: "#38d9a9"})

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e6edf3"),
            margin=dict(l=10, r=10, t=10, b=10),
            legend_title_text="Above threshold"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("Enable 'Show action controls' above to interact with the playground.")

# -----------------------------------------------------------
# DATA TAB (Tables, downloads, alerts)
# -----------------------------------------------------------
with tab_data:
    st.markdown("<div class='glass-card' role='region' aria-label='Data preview and export'>", unsafe_allow_html=True)
    st.write("Preview the generated dataset and export it if needed.")
    dc1, dc2 = st.columns([2,1])
    with dc1:
        st.dataframe(df.head(20), use_container_width=True)
    with dc2:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="sample_data.csv", mime="text/csv")
        st.success("Data ready for export.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 8) FOOTER / STATUS
# ==========================================
st.markdown("---")
st.caption("Built with Streamlit • Figma-inspired styling • Accessible and responsive by design")
