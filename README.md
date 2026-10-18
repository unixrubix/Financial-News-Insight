# 📈 FinBot Intelligence System with Local LLM (Ollama)

A fully containerized pipeline built with **FastAPI**, **Streamlit**, and **Ollama** that pulls financial web articles, calculates sentiment on a `[0, 1]` scale, performs Named Entity Recognition (NER), and delivers AI summaries running on a local, secure LLM.

![Application interface](/images/interface.png)

## 🚀 Features

- **🌐 Web Article Scraping**: Instantly extracts and parses text contents from any public financial URL.
- **😊 Sentiment Normalization**: Scales VADER polarity metrics to a `[0, 1]` range (extremely bearish to bullish).
- **🔍 Entity Recognition**: Identifies companies, dates, names, and organizations using SpaCy.
- **🤖 Local LLM Summaries**: Uses **Ollama** (`tinyllama`) running completely offline in your local environment to generate bulleted briefings.
- **🐳 Production Ready**: Fully configured using Docker Compose with persistent model storage volume caching.

## 🛠️ How to Deploy Locally with Docker Compose

1. Ensure you have Docker and Docker Compose installed.
2. Navigate into the app folder and Spin up the container cluster (Frontend, Backend, and Ollama services):
   ```bash
   cd app
   docker compose up --build -d
   ```
3. Upon first startup, the backend automatically instructs Ollama to download and pull the `tinyllama` model.
4. Open your browser and view the interactive UI dashboard at **`http://localhost:8501`**!
5. Shut down the microservice stack:
   ```bash
   docker compose down
   ```

## 📁 Code Architecture

- `app.py`: FastAPI server containing scraper rules, SpaCy entity recognition, and Ollama client routines.
- `frontend.py`: Streamlit-based interactive web interface with dual-column layout.
- `docker-compose.yml`: Multi-container orchestrator creating a shared virtual network and persistent storage volumes.

### News Article Preview

![News Article Preview](/images/link_response.png)

### News Article Response with Ollama integration

![News Article Preview](/images/link_response_with_ollama.png)

### News Article Response with layman Ollama explanation

![News Article Preview](/images/link_response_with_ollama_layman.png)
