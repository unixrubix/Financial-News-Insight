# Use a lightweight python base image
FROM python:3.10-slim

WORKDIR /app

# Install system requirements for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement file first to cache layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download SpaCy models and NLTK assets
RUN python -m spacy download en_core_web_sm
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('vader_lexicon')"

# Copy source codes
COPY app.py .
COPY frontend.py .

# Expose default API & Web interface ports
EXPOSE 8000
EXPOSE 8501
