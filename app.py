import os
from collections import OrderedDict
from flask import Flask, request, jsonify, send_file
from scraper import extract_news
from textsum import summarize_article
from sentiment_analysis import analyze_sentiment
from topic_extraction import extract_topics
from comparative_analysis import (
    generate_final_sentiment_summary,
    find_common_topics
)
from tts import translate_text, save_translated_text, text_to_speech, play_audio
import nltk
from nltk.tokenize import sent_tokenize

# Ensure necessary NLTK data is downloaded
nltk.download('punkt_tab')

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <html>
      <head>
        <title>News Analysis</title>
      </head>
      <body>
        <h1>News Analysis</h1>
        <form action="/api/extract" method="get">
          <label for="company">Enter Company Name:</label>
          <input type="text" id="company" name="company" placeholder="e.g., apple">
          <input type="submit" value="Submit">
        </form>
      </body>
    </html>
    '''

@app.route('/api/extract', methods=['GET'])
def extract_company_news():
    company = request.args.get('company')
    if not company:
        return jsonify({'error': 'Please provide a company name in the query parameter (e.g., ?company=apple).'}), 400
    company = company.replace(' ', '+')
    news_articles = extract_news(company)
    processed_articles = []
    individual_summaries = []
    
    for article in news_articles:
        content = article.get("Full Content", "")
        if content:
            summary = summarize_article(content)
            sentiment_result = analyze_sentiment(content)
            topics = extract_topics(content)
            article["Summary"] = summary
            article["Sentiment"] = sentiment_result["label"]
            article["Sentiment_Prob"] = sentiment_result["probability"]
            article["Topics"] = topics
            individual_summaries.append(summary)
        processed_articles.append(article)
    
    if individual_summaries:
        aggregated_text = " ".join(individual_summaries)
        final_combined_summary = summarize_article(aggregated_text, final_summary=True)
        sentences = sent_tokenize(final_combined_summary)
        if sentences and not sentences[-1].strip().endswith('.'):
            sentences = sentences[:-1]
        final_combined_summary = " ".join(sentences)
    else:
        final_combined_summary = ""
    
    final_sentiment_summary = generate_final_sentiment_summary(processed_articles, company)
    common_topics = find_common_topics(processed_articles)
    
    # Translate final combined summary to Hindi.
    hindi_summary = translate_text(final_combined_summary, dest_lang='hi')
    
    # Save the translated Hindi text in the static/Text folder.
    text_dir = os.path.join(app.root_path, 'static', 'Text')
    os.makedirs(text_dir, exist_ok=True)
    translated_filename = f"{company.lower()}_translated.txt"
    translated_filepath = os.path.join(text_dir, translated_filename)
    save_translated_text(hindi_summary, filename=translated_filename)
    
    # Convert the Hindi summary to speech and save as an MP3 file.
    audio_dir = os.path.join(app.root_path, 'static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    audio_filename = f"{company.lower()}_tts.mp3"
    audio_filepath = os.path.join(audio_dir, audio_filename)
    text_to_speech(hindi_summary, lang='hi', filename=audio_filepath)
    
    response = OrderedDict()
    response["company"] = company
    response["articles"] = processed_articles
    response["final_sentiment_summary"] = final_sentiment_summary
    response["final_combined_summary"] = final_combined_summary
    response["common_topics"] = common_topics
    response["audio_url"] = f"/static/audio/{audio_filename}"
    response["translated_text_file"] = f"/static/Text/{translated_filename}"
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
