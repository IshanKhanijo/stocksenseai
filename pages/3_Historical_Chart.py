# ---------- 3_Historical_Chart.py — Modern UI for Historical Stock Price Chart ----------

import streamlit as st
import yfinance as yf

# --------------------------
# Page Setup
# --------------------------
st.set_page_config(page_title="📉 Historical Chart", layout="wide")

# --------------------------
# Custom Styling
# --------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #f8f9fa, #e0eafc);
    font-family: 'Segoe UI', sans-serif;
}
.block {
    background-color: #ffffffdd;
    padding: 2rem 2.5rem;
    margin: 2rem auto;
    border-radius: 18px;
    max-width: 1300px;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.08);
}
.title-card {
    background: #e3f2fd;
    padding: 2rem;
    text-align: center;
    border-radius: 14px;
    margin-bottom: 2rem;
}
h1.title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #1f2937;
}
.subtitle {
    font-size: 1.05rem;
    color: #374151;
}
.radio-label {
    font-size: 1rem;
    font-weight: 600;
    color: #1d4ed8;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# UI Layout
# --------------------------
with st.container():
    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown('''
    <div class="title-card">
        <h1 class="title">📉 Historical Stock Price Chart</h1>
        <div class="subtitle">Visualize daily closing prices for your selected stock over multiple timeframes.</div>
    </div>
    ''', unsafe_allow_html=True)

    ticker = st.text_input("Enter Stock Ticker", value="AAPL")

    if ticker:
        st.markdown('<div class="radio-label">Select Timeframe</div>', unsafe_allow_html=True)
        chart_period = st.radio(
            label="",
            options=["1y", "2y", "5y", "10y"],
            index=3,
            horizontal=True
        )

        chart_data = yf.download(ticker, period=chart_period, interval="1d")[['Close']].dropna()

        if not chart_data.empty:
            st.line_chart(chart_data['Close'])
        else:
            st.warning("No data available for the selected period.")

    st.markdown('</div>', unsafe_allow_html=True)
