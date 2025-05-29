import streamlit as st
import base64
import os

def get_image_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.set_page_config(
    page_title="StockSense AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

image_path = os.path.join("images", "landing_page.png")
image_base64 = get_image_base64(image_path)

# ---------- CSS ----------
st.markdown(f"""
<style>
    html {{
        scroll-behavior: smooth;
    }}
    body {{
        background: linear-gradient(135deg, #f0f4ff, #eef1f7);
        font-family: 'Segoe UI', sans-serif;
        color: #1e293b;
        margin: 0;
        padding: 0;
    }}
    .navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2.5rem;
        background: rgba(255, 255, 255, 0.9);
        border-bottom: 1px solid #cbd5e1;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        backdrop-filter: blur(10px);
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    .nav-links a {{
        margin: 0 1.2rem;
        text-decoration: none;
        font-weight: 500;
        color: #1e293b;
        transition: 0.25s;
    }}
    .nav-links a:hover {{
        color: #6366f1;
    }}
    .hero {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6rem 3rem 4rem 3rem;
        background: linear-gradient(135deg, #edf0fc, #f7f9fe);
        border-radius: 20px;
        margin: 3rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
    }}
    .hero-title {{
        font-size: 3.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 1.2rem;
        line-height: 1.25;
    }}
    .hero-desc {{
        font-size: 1.25rem;
        margin-bottom: 2rem;
        color: #475569;
    }}
    .hero-buttons a {{
        padding: 0.9rem 1.6rem;
        margin-right: 1rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        text-decoration: none;
        transition: 0.25s;
    }}
    .btn-primary {{
        background: linear-gradient(to right, #4f46e5, #6366f1);
        color: white !important;
        border: none;
    }}
    .btn-primary:hover {{
        background: linear-gradient(to right, #4338ca, #4f46e5);
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }}
    .btn-outline {{
        border: 2px solid #6366f1;
        color: #6366f1;
        background: transparent;
    }}
    .btn-outline:hover {{
        background-color: #e0e7ff;
    }}
    .features {{
        text-align: center;
        padding: 3.5rem 2rem;
    }}
    .features h2 {{
        font-size: 2.4rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 1rem;
    }}
    .feature-grid {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
    }}
    .card {{
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
        width: 280px;
        text-align: left;
        transition: all 0.3s ease-in-out;
        border: 1px solid #e2e8f0;
        cursor: pointer;
    }}
    .card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.08);
    }}
    .card h4 {{
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        color: #1e293b;
    }}
</style>
""", unsafe_allow_html=True)

# ---------- NAVBAR ----------
st.markdown("""
<div class="navbar">
    <div style="font-weight:bold; font-size: 1.5rem; color:#0d6efd;">StockSense <span style="font-size: 0.8rem; background: #e0e7ff; padding: 2px 6px; border-radius: 5px;">AI</span></div>
    <div class="nav-links">
        <a href="/">Home</a>
        <a href="/Dashboard">Dashboard</a>
        <a href="/Watchlist">Watchlist</a>
        <a href="/About">About</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown(f"""
<div class="hero">
    <div class="hero-text">
        <div class="hero-title">AI-Powered Stock<br>Analysis & Investment Insights</div>
        <div class="hero-desc">
            Make smarter investment decisions with our advanced<br>
            AI stock predictions and sentiment analysis of market news.
        </div>
        <div class="hero-buttons">
            <a href="#features" class="btn-primary">Analyze Stocks</a>
            <a href="/About" class="btn-outline">Learn More</a>
        </div>
    </div>
    <div>
        <img src="data:image/png;base64,{image_base64}" 
             style="border-radius: 12px; box-shadow: 0px 8px 20px rgba(0,0,0,0.05); max-width: 400px;" />
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- FEATURES ----------
st.markdown("""
<div id="features" class="features">
    <h2>Key Features</h2>
    <p>Explore the four core pillars of our AI-powered investment assistant:</p>
    <div class="feature-grid">
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <h4>🧠 Market Intelligence</h4>
        <p>Stay informed with AI-curated summaries of real-time financial news and market sentiment, all tailored to your selected stock.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore →", key="market"):
        st.warning("Please use the sidebar to navigate to '📰 News and AI Summary'")

with col2:
    st.markdown("""
    <div class="card">
        <h4>📊 Financial Snapshot</h4>
        <p>Quickly access a company’s most critical metrics, from P/E ratio to market cap, distilled for fast, smart decisions.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore →", key="snapshot"):
        st.warning("Please use the sidebar to navigate to '📊 Financial Snapshot'")

with col3:
    st.markdown("""
    <div class="card">
        <h4>🔮 AI Price Forecast</h4>
        <p>Powered by a decade of data and deep learning, our LSTM model forecasts tomorrow’s closing price with precision.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore →", key="forecast"):
        st.warning("Please use the sidebar to navigate to '🔮 AI Price Forecast'")

with col4:
    st.markdown("""
    <div class="card">
        <h4>📈 Interactive Charting</h4>
        <p>Explore historical price trends with smooth, zoomable charts — from 1-year insights to 10-year performance views.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore →", key="charting"):
        st.warning("Please use the sidebar to navigate to '📈 Interactive Charting'")


st.markdown("</div></div>", unsafe_allow_html=True)
