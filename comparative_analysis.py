def aggregate_sentiments(articles):
    """
    Aggregates sentiment counts from a list of article dictionaries.
    
    Each article is expected to have a "Sentiment" field with a label like 'positive', 'neutral', or 'negative'.
    
    Returns:
        sentiment_counts (dict): Dictionary with sentiment labels as keys and counts as values.
    """
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    for article in articles:
        # Normalize the label to lowercase for consistency.
        sentiment_label = article.get("Sentiment", "").lower()
        if sentiment_label in sentiment_counts:
            sentiment_counts[sentiment_label] += 1
    return sentiment_counts


def generate_final_sentiment_summary(articles, company_name="the company"):
    """
    Generates an overall sentiment summary from a list of articles.
    Returns a more accurate text summary considering ties.
    """
    sentiment_counts = aggregate_sentiments(articles)
    total = sum(sentiment_counts.values())

    if total == 0:
        return "No articles to analyze."

    pos = sentiment_counts.get("positive", 0)
    neu = sentiment_counts.get("neutral", 0)
    neg = sentiment_counts.get("negative", 0)

    # Find the sentiment with the highest count
    max_sentiment = max(pos, neu, neg)

    # Handle ties by prioritizing positive > neutral > negative
    if pos == max_sentiment and pos > neu and pos > neg:
        sentiment_summary = "mostly positive"
        implication = "Potential stock growth expected."
    elif neg == max_sentiment and neg > pos and neg > neu:
        sentiment_summary = "mostly negative"
        implication = "Potential stock decline expected."
    elif neu == max_sentiment and neu > pos and neu > neg:
        sentiment_summary = "mostly neutral"
        implication = "Stock likely to remain stable."

    # Handle ties gracefully
    elif pos == neu and pos > neg:
        sentiment_summary = "balanced between positive and neutral"
        implication = "Mixed signals, but generally stable."
    elif pos == neg and pos > neu:
        sentiment_summary = "divided between positive and negative"
        implication = "Uncertain outlook with contrasting views."
    elif neu == neg and neu > pos:
        sentiment_summary = "balanced between neutral and negative"
        implication = "Caution advised, potential risks present."
    else:
        sentiment_summary = "equally distributed across sentiments"
        implication = "Highly mixed sentiment, unpredictable trend."

    # Return the improved summary
    return f"{company_name.capitalize()}'s latest news coverage is {sentiment_summary}. {implication}"
def find_common_topics(articles):
    """
    Identifies common topics across all articles.
    Each article is expected to have a "Topics" key containing a list of topics.
    
    Returns:
        common_topics (list): List of topics that are common to all articles.
    """
    topics_sets = [set(article.get("Topics", [])) for article in articles if article.get("Topics")]
    if not topics_sets:
        return []
    common_topics = set.intersection(*topics_sets)
    return list(common_topics) 