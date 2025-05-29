# ---------- 2_news_summary.py — Modern UI for News & AI Summary ----------

import streamlit as st
import requests
import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os

# --------------------------
# Setup & API Keys
# --------------------------
load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

st.set_page_config(page_title="📰 News and AI Summary", layout="wide")

# --------------------------
# Custom CSS Styling
# --------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
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
    background: #e0f2fe;
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
    font-size: 1.1rem;
    color: #374151;
}
.article-title {
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
    color: #1e40af;
}
.article-desc {
    font-size: 1rem;
    color: #374151;
    margin-bottom: 0.5rem;
}
.url-link {
    font-size: 0.9rem;
    color: #2563eb;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# Page Header
# --------------------------
with st.container():
    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown('''
    <div class="title-card">
        <h1 class="title">📰 Stock News & AI Summary</h1>
        <div class="subtitle">Get the latest news headlines and a smart AI-generated summary for any company ticker.</div>
    </div>
    ''', unsafe_allow_html=True)

    ticker = st.text_input("Enter Stock Ticker", value="AAPL")

    if ticker:
        today = datetime.date.today()
        from_date = today - datetime.timedelta(days=30)

        url = (
            f"https://newsapi.org/v2/everything?q={ticker}&from={from_date}&to={today}"
            f"&sortBy=publishedAt&language=en&apiKey={news_api_key}"
        )

        response = requests.get(url)

        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                st.markdown('<div class="section-title">📢 Latest News</div>', unsafe_allow_html=True)

                for article in articles[:5]:
                    st.markdown(f'<div class="article-title">{article["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="article-desc">{article["description"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<a class="url-link" href="{article["url"]}" target="_blank">{article["url"]}</a>', unsafe_allow_html=True)
                    st.markdown("---")

                st.markdown('<div class="section-title">🤖 AI-Generated Summary</div>', unsafe_allow_html=True)

                combined_text = "\n\n".join(
                    f"{article.get('title', '')}\n{article.get('description', '')}" for article in articles[:5]
                )

                if combined_text.strip():
                    prompt = f"Summarize the following news and present them in bullet points. Add a short summary paragraph after the bullet indicating wether it is good or bad for the stock price. {ticker}:\n\n{combined_text}"
                    try:
                        summary_response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        summary = summary_response.choices[0].message.content
                        st.success(summary)
                    except Exception as e:
                        st.error(f"OpenAI API Error: {e}")
                else:
                    st.info("No content available for summarization.")
            else:
                st.warning("No news articles found for this ticker.")
        else:
            st.error("Failed to fetch news.")

    st.markdown('</div>', unsafe_allow_html=True)
