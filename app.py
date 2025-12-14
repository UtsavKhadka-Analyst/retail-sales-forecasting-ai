st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ===== DARK ENTERPRISE BACKGROUND ===== */
.stApp {
    background: radial-gradient(circle at top left, #0b1220, #020617);
    color: #e5e7eb;
}

/* ===== SECTION HEADER (CHECKBOX STYLE) ===== */
.section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    background: linear-gradient(90deg, #1e40af, #0284c7);
    padding: 14px 20px;
    border-radius: 14px;
    font-weight: 700;
    font-size: 18px;
    color: white;
    margin: 28px 0 16px 0;
    box-shadow: 0 12px 30px rgba(2,132,199,0.45);
}
.section-header::before {
    content: "✓";
    background: white;
    color: #1e40af;
    font-weight: 900;
    width: 26px;
    height: 26px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ===== KPI CARDS ===== */
.metric-card {
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 22px;
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 15px 35px rgba(0,0,0,0.45);
    transition: all 0.25s ease;
}
.metric-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.6);
}

/* ===== TITLES ===== */
h1 {
    background: linear-gradient(90deg, #60a5fa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    color: white;
    border-radius: 10px;
    padding: 12px 26px;
    font-weight: 600;
    border: none;
    transition: all 0.25s ease;
}
.stButton > button: hover {
    transform: scale(1.05);
    box-shadow: 0 14px 35px rgba(56,189,248,0.5);
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid rgba(148,163,184,0.18);
}

/* ===== CHAT ===== */
.chat-user {
    background: linear-gradient(135deg, #2563eb, #38bdf8);
    color: white;
    padding: 12px 16px;
    border-radius: 16px 16px 0 16px;
    margin-bottom: 12px;
    max-width: 75%;
}
.chat-bot {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid rgba(148,163,184,0.2);
    padding: 12px 16px;
    border-radius: 16px 16px 16px 0;
    margin-bottom: 12px;
    max-width: 75%;
}

/* ===== PLOTLY TRANSPARENT ===== */
.js-plotly-plot {
    background: transparent! important;
}
</style>
""", unsafe_allow_html=True)
