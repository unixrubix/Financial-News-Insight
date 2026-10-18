import streamlit as st
import requests
import os

st.set_page_config(page_title="FinBot Web Insights + Ollama", layout="wide")
st.title("📈 Financial News Link Analyzer with Local LLM")
st.write("Paste any financial article link from the web to run sentiment scaling, entity recognition, and local Ollama-powered contextual summaries.")

backend_host = os.getenv("BACKEND_URL", "http://localhost:8000")
api_url = f"{backend_host}/analyze"

url_input = st.text_input("Article URL:", placeholder="https://www.reuters.com/business/...")

if st.button("Analyze Article"):
    if not url_input:
        st.warning("Please enter a valid URL first.")
    else:
        with st.spinner("Running full pipeline (Scraping -> VADER Sentiment -> SpaCy NER -> Local Ollama LLM Insight)... This may take up to 20 seconds."):
            try:
                response = requests.post(api_url, json={"url": url_input}, timeout=45)
                if response.status_code == 200:
                    data = response.json()

                    st.success("Analysis complete!")
                    st.subheader(f"📰 {data['title']}")

                    # Main Content Partitioning
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("### 🤖 Local Ollama Smart Briefing")
                        st.write(data.get('ai_briefing', 'No AI summary available.'))

                        st.write("### 😊 Sentiment Matrix")
                        compound = data['sentiment']['compound']
                        label = data['sentiment']['label'].upper()

                        st.metric(label=f"Scaled Compound Sentiment ({label})", value=f"{compound:.3f}")
                        st.progress(compound)
                        st.info("*Note: Sentiment compound score is normalized on a scale from 0.0 (Extremely Bearish) to 1.0 (Extremely Bullish).* ")

                    with col2:
                        st.write("### 💡 Actionable Insights")
                        for insight in data['insights']:
                            st.write(f"- {insight}")

                        st.write("### 🔍 Key Extracted Entities")
                        if data['entities']:
                            for ent in data['entities']:
                                st.write(f"🔹 **{ent['text']}** ({ent['label']}) — *{ent['description']}*")
                        else:
                            st.write("No key entities detected in this article.")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unable to analyze the website link.')}")
            except Exception as e:
                st.error(f"Could not reach backend API at {api_url}. Please ensure your services are fully running via docker-compose.")
