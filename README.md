# Financial-News-Insight

# 📈 FinBot Intelligence System & Web Interface

A containerized microservice pipeline built with **FastAPI** and **Streamlit** to extract financial web articles, scale sentiment output on a `[0, 1]` range, and isolate Named Entities (NER) using SpaCy.

![Application interface](/images/interface.png)

## 🚀 Features

- **🌐 Web Article Scraping**: Provide any web link (e.g., Reuters, Bloomberg) to parse and process context instantly.
- **😊 Sentiment Normalization**: Transforms standard VADER compound score polarity metrics onto an intuitive `[0, 1]` scale (from extremely bearish to bullish).
- **🔍 Entity Extraction**: Leverages SpaCy's natural language processing models to extract key players, locations, currencies, and organizations.
- **🐳 Production Ready**: Fully configured using Multi-stage Docker optimization to compile and deploy both backend and frontend applications seamlessly.

## 🛠️ How to Deploy Locally with Docker Compose

1. Ensure you have Docker and Docker Compose installed on your host system.
2. Start the services together in detached mode:
   ```bash
   docker compose up --build -d
   ```
3. View running container logs:
   ```bash
   docker compose logs -f
   ```
4. Open your browser to the Web UI at **`http://localhost:8501`**!
5. Shut down the microservice stack:
   ```bash
   docker compose down
   ```

## 📁 Code Architecture

- `app.py`: FastAPI server handling web extraction, NLP tokenization, and pipeline execution.
- `frontend.py`: Streamlit-based interactive web dashboard.
- `Dockerfile`: Container environment specification.
- `docker-compose.yml`: Multi-container service orchestrator.
- `requirements.txt`: Python package dependency manifest.

![News Article Preview](/images/link_response.png)
