
import sys
import json
from collections import OrderedDict
import nltk
from nltk.tokenize import sent_tokenize
from scraper import extract_news
from textsum import summarize_article
from sentiment_analysis import analyze_sentiment
from topic_extraction import extract_topics  # Assuming you implemented this as shown earlier
from comparative_analysis import (
    aggregate_sentiments,
    visualize_sentiments_bar,
    generate_final_sentiment_summary,
    find_common_topics
)
from tts import translate_text, text_to_speech, play_audio

# Download required NLTK resource
nltk.download('punkt_tab')

# If run as a standalone script, accept company tags from command line arguments.
if len(sys.argv) > 1:
    company_tags = sys.argv[1:]
else:
    company_tags = ['tesla']  # default if none provided

all_news = {}

# Process each company tag.
for tag in company_tags:
    print(f"\nExtracting news for tag: {tag}")
    all_news[tag] = extract_news(tag)

# Process articles for each company.
for company, articles in all_news.items():
    print(f"\nNews for {company.capitalize()}:")
    individual_summaries = []  # List to store each article's summary.
    processed_articles = []
    
    for article in articles:
        title = article['Title']
        url = article['URL']
        content = article['Full Content']
        print(f"Title: {title}")
        print(f"URL: {url}")
        if content:
            summary = summarize_article(content)
            sentiment_result = analyze_sentiment(content)
            topics = extract_topics(content)
            # Update the article dictionary with new fields.
            article['Summary'] = summary
            article['Sentiment'] = sentiment_result['label']
            article['Sentiment_Prob'] = sentiment_result['probability']
            article['Topics'] = topics
            individual_summaries.append(summary)
            print(f"Summary: {summary}")
            print(f"Sentiment: {sentiment_result['label']} (Prob: {sentiment_result['probability']:.2f})")
            print(f"Topics: {topics}\n")
        else:
            print("No content to process.\n")
        processed_articles.append(article)
    
    # Comparative Sentiment Analysis:
    sentiment_counts = aggregate_sentiments(articles)
    print(f"\nComparative Sentiment Analysis for {company.capitalize()}:")
    print(sentiment_counts)
    visualize_sentiments_bar(sentiment_counts, company)
    
    # Generate final sentiment summary using the company name.
    final_sentiment_summary = generate_final_sentiment_summary(articles, company)
    print(f"Final Sentiment Analysis: {final_sentiment_summary}\n")
    
    # Identify common topics among the articles.
    common_topics = find_common_topics(articles)
    print(f"Common Topics across articles for {company.capitalize()}: {common_topics}\n")
    
    # Aggregate individual summaries into one long text.
    if individual_summaries:
        aggregated_text = " ".join(individual_summaries)
        # Generate a final combined summary from the aggregated summaries.
        final_combined_summary = summarize_article(aggregated_text, final_summary=True)
        
        # Post-process: split into sentences and remove an incomplete last sentence.
        sentences = sent_tokenize(final_combined_summary)
        if sentences and not sentences[-1].strip().endswith('.'):
            sentences = sentences[:-1]
        final_combined_summary = " ".join(sentences)
        
        print("Final Combined Summary:")
        print(final_combined_summary)
        
        # Translate the final combined summary to Hindi.
        hindi_summary = translate_text(final_combined_summary, dest_lang='hi')
        print("Hindi Translation of Final Combined Summary:")
        print(hindi_summary)
        
        # Convert the Hindi summary to speech and play it.
        audio_filename = text_to_speech(hindi_summary, lang='hi')
        play_audio(audio_filename)
    else:
        final_combined_summary = ""
        print("No summaries available for aggregation.")
    
    # OrderDict to enforce key order.
    final_response = OrderedDict()
    final_response["company"] = company
    final_response["articles"] = processed_articles
    final_response["final_sentiment_summary"] = final_sentiment_summary
    final_response["final_combined_summary"] = final_combined_summary
    final_response["common_topics"] = common_topics
    
    print("\nFinal Response:")
    print(json.dumps(final_response, indent=2))