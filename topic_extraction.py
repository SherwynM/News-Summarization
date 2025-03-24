
from keybert import KeyBERT

# Initialize KeyBERT model
kw_model = KeyBERT()

def extract_topics(text, top_n=5):
    """
    Extracts key topics from text using KeyBERT.
    
    Parameters:
        text (str): The input article text.
        top_n (int): Number of top keywords to extract.
    
    Returns:
        topics (list): A list of extracted keywords/topics.
    """
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    topics = [kw[0] for kw in keywords]
    return topics
