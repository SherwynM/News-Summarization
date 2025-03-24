# News Analysis Flask App

## Overview
This repository contains a Flask-based web application that performs a comprehensive analysis of news articles related to a specified company. The application integrates multiple NLP tasks including:
- **Web Scraping:** Extracts news articles from MoneyControl.
- **Text Summarization:** Generates concise summaries for each article and an aggregated final summary.
- **Sentiment Analysis:** Analyzes the sentiment (positive, neutral, negative) of each article using FinBERT.
- **Topic Extraction:** Extracts key topics from articles using KeyBERT.
- **Comparative Analysis:** Aggregates sentiment data and identifies common topics.
- **Text-to-Speech (TTS):** Translates the final summary into Hindi and converts it to speech, saving the output as an MP3 file.
- **API Interface:** A Flask API endpoint is provided along with a simple home page with a search bar.

## Features
- **Modular Design:** Each task is separated into distinct modules (e.g., `scraper.py`, `textsum.py`, `sentiment_analysis.py`, etc.).
- **Robust Pipeline:** The pipeline processes input company names (even with spaces or special characters), aggregates data from multiple news pages, and performs several NLP tasks.
- **TTS Integration:** Generates Hindi speech from the final combined summary and saves the output for playback.
- **Flask API:** Exposes the full functionality via an API endpoint, making it easy to integrate with other systems or a frontend.

## Directory Structure


## Installation and Setup

### Prerequisites
- Python 3.8 or higher.
- Git.
- Virtual environment (recommended).
- Optional: Docker (for containerized deployment).

### Clone the Repository
Clone the project repository using Git:
```bash

git clone https://github.com/your-username/news-analysis-flask.git
cd news-analysis-flask

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


### Install Dependencies
pip install -r requirements.txt


### Download NLTK Resources
python -c "import nltk; nltk.download('punkt')"


###Running the Flask Application
python app.py
