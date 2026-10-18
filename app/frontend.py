import streamlit as st
import requests
import os

st.set_page_config(page_title="FinBot Web Insights", layout="wide")
st.title("📈 Financial News Link Analyzer")
st.write("Paste any financial article link from the web to run comprehensive sentiment scaling & entity recognition.")

# Dynamically read the backend URL from environment variables for container network compatibility
backend_host = os.getenv("BACKEND_URL", "http://localhost:8000")
api_url = f"{backend_host}/analyze"

url_input = st.text_input("Article URL:", placeholder="https://www.reuters.com/business/...")

if st.button("Analyze Article"):
    if not url_input:
        st.warning("Please enter a valid URL first.")
    else:
        with st.spinner("Fetching webpage content and running NLP analysis pipeline..."):
            try:
                response = requests.post(api_url, json={"url": url_input}, timeout=15)
                if response.status_code == 200:
                    data = response.json()

                    st.success("Analysis complete!")
                    st.subheader(f"📰 {data['title']}")

                    # Split display columns
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("### 😊 Sentiment Matrix")
                        compound = data['sentiment']['compound']
                        label = data['sentiment']['label'].upper()

                        st.metric(label=f"Scaled Compound Sentiment ({label})", value=f"{compound:.3f}")
                        st.progress(compound)
                        st.info("*Note: Sentiment compound score is normalized on a scale from 0.0 (Extremely Bearish) to 1.0 (Extremely Bullish).* ")

                        st.write("### 💡 Actionable Insights")
                        for insight in data['insights']:
                            st.write(f"- {insight}")

                    with col2:
                        st.write("### 🔍 Key Extracted Entities")
                        if data['entities']:
                            for ent in data['entities']:
                                st.write(f"🔹 **{ent['text']}** ({ent['label']}) — *{ent['description']}*")
                        else:
                            st.write("No key entities detected in this article.")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unable to analyze the website link.')}")
            except Exception as e:
                st.error(f"Could not reach backend API at {api_url}. Please ensure your Docker container backend service is running.")
