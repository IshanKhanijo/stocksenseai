import streamlit as st
from datetime import datetime
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import load_dotenv
import os

# Load .env if running locally
load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

fd = FundamentalData(key=api_key, output_format='json')

st.set_page_config(page_title="📊 Company Snapshot", layout="wide")

with st.container():
    st.markdown("""
        <div style='
            width: 100%;
            background: #e0f7fa;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            text-align: center;
            font-size: 0.9rem;
            color: #0f172a;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
            margin-top: 1.5rem;
            margin-bottom: -1.5rem;
        '>
            🔍 Powered by Alpha Vantage API | <strong>{date}</strong>
        </div>
    """.format(date=datetime.today().strftime('%A, %d %B %Y')), unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #fdfcfb, #f8f3f3);
        font-family: 'Segoe UI', sans-serif;
    }
    .block {
        background-color: #ffffffee;
        padding: 2.5rem;
        margin: 2rem auto;
        border-radius: 20px;
        max-width: 1400px;
        box-shadow: 0 12px 45px rgba(0, 0, 0, 0.1);
    }
    .header-card {
        background: #e0f2fe;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.07);
        text-align: center;
    }
    .title {
        font-size: 2.6rem;
        font-weight: 900;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #475569;
    }
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1d3557;
        margin: 2rem 0 1rem;
        border-bottom: 3px solid #4f46e5;
        display: inline-block;
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 0.25rem;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #111827;
    }
    .stTextInput>div>input {
        background-color: #fff;
        border: 1.8px solid #cbd5e1;
        padding: 0.75rem 1.1rem;
        font-size: 1rem;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown('''
    <div class="header-card">
        <div class="title">📊 Company Financial Snapshot</div>
        <div class="subtitle">Search any stock ticker to retrieve financial highlights instantly.</div>
    </div>
    ''', unsafe_allow_html=True)

    ticker = st.text_input("Enter Stock Ticker", value="AAPL").upper()

    if ticker:
        try:
            data, _ = fd.get_company_overview(ticker)
        except Exception as e:
            st.error("❌ Failed to fetch data from Alpha Vantage.")
            st.stop()

        st.markdown('<div class="section-title">Key Financial Metrics</div>', unsafe_allow_html=True)

        metrics = [
            {
                "Company": data.get("Name", "N/A"),
                "Sector": data.get("Sector", "N/A"),
                "Market Cap": data.get("MarketCapitalization", "N/A")
            },
            {
                "PE Ratio": data.get("PERatio", "N/A"),
                "EPS": data.get("EPS", "N/A"),
                "Dividend Yield": data.get("DividendYield", "N/A")
            },
            {
                "ROE": data.get("ReturnOnEquityTTM", "N/A"),
                "Beta": data.get("Beta", "N/A"),
                "Currency": data.get("Currency", "USD")
            }
        ]

        for row in metrics:
            cols = st.columns(len(row))
            for i, (label, value) in enumerate(row.items()):
                with cols[i]:
                    st.markdown(f'''
                    <div class="card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
