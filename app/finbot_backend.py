import os
import re
import spacy
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

# Ensure resources are downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('vader_lexicon', quiet=True)

# Initialize dependencies
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer()

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    os.system('python -m spacy download en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

app = FastAPI(title="Financial News Intelligence API with Ollama", version="2.0.0")

class LinkRequest(BaseModel):
    url: str

def clean_and_preprocess(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_ollama_insight(title, content):
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_name = "tinyllama"

    prompt = f"""Explain this financial news article to a layman who has no prior knowledge of finance, business, or complex stock market terminology. Keep the language highly accessible, use simple analogies if helpful, and summarize the core message in 3 simple bullet points:

    TITLE: {title}
    CONTENT: {content[:3000]}
    """

    try:
        requests.post(f"{ollama_host}/api/pull", json={"name": model_name}, timeout=5)
        response = requests.post(
            f"{ollama_host}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=25
        )
        if response.status_code == 200:
            return response.json().get("response", "No summary generated.")
    except Exception as e:
        return f"Ollama analysis unavailable ({str(e)}). Ensure Ollama is running and has downloaded the '{model_name}' model."
    return "Ollama model was unable to generate a response."

@app.post("/analyze")
def analyze_link(request: LinkRequest):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(request.url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Could not retrieve content from URL")

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "Extracted Article Link"

        for script in soup(["script", "style"]):
            script.decompose()

        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])

        if len(content.strip()) < 10:
            raise HTTPException(status_code=400, detail="Webpage has insufficient extractable text")

        full_text = f"{title} {content}"

        # 1. Scaled Sentiment compound score [0, 1]
        scores = sia.polarity_scores(full_text)
        scaled_compound = (scores['compound'] + 1.0) / 2.0

        if scaled_compound >= 0.525:
            label = 'positive'
        elif scaled_compound <= 0.475:
            label = 'negative'
        else:
            label = 'neutral'

        # 2. NER extraction
        doc = nlp(full_text[:100000])
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'description': spacy.explain(ent.label_)
            })

        unique_entities = list({e['text']: e for e in entities}.values())

        # 3. Generate traditional rule-based insights
        insights = []
        insights.append(f"Sentiment Score: {scaled_compound:.3f} ({label.upper()})")
        if unique_entities:
            insights.append(f"Extracted {len(unique_entities)} distinct financial entities.")
            key_orgs = [e['text'] for e in unique_entities if e['label'] == 'ORG'][:3]
            if key_orgs:
                insights.append(f"Key Organizations: {', '.join(key_orgs)}")

        # 4. Generate local Ollama LLM insights
        ai_briefing = get_ollama_insight(title, content)

        return {
            "title": title.strip(),
            "sentiment": {
                "compound": scaled_compound,
                "label": label,
                "details": scores
            },
            "entities": unique_entities[:15],
            "insights": insights,
            "ai_briefing": ai_briefing
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
