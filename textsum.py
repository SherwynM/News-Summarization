
from transformers import pipeline

# Initialize the summarization pipeline with a deterministic decoding strategy (beam search)
summarizer = pipeline(
    "summarization",
    model="Falconsai/text_summarization"
)

def summarize_article(article_text, final_summary=False):
    # Clean the article text: remove extraneous whitespace
    cleaned_text = ' '.join(article_text.split())
    if len(cleaned_text.split()) < 50:
        return "Article too short to summarize."
    
    word_count = len(cleaned_text.split())
    
    if final_summary:
        # For a final combined summary, adjust parameters based on input length.
        if word_count < 100:
            min_len = 30
            max_len = 70
        else:
            min_len = max(80, int(0.15 * word_count))
            # Ensure max_len is always at least min_len + 20
            max_len = max(min_len + 20, min(250, int(0.3 * word_count) + 20))
    else:
        # Settings for individual articles.
        min_len = max(50, int(0.1 * word_count))
        max_len = max(min_len + 20, min(150, int(0.2 * word_count) + 20))
    
    summary_output = summarizer(
        cleaned_text,
        min_length=min_len,
        max_length=max_len,
        num_beams=4,
        do_sample=False
    )
    summary_text = summary_output[0]['summary_text']
    
    # Post-process: Ensure the summary ends with proper punctuation.
    if summary_text and summary_text[-1] not in '.!?':
        summary_text += '.'
    
    # If generating a final combined summary, cut off the text at the last full stop.
    if final_summary:
        last_period = summary_text.rfind('.')
        if last_period != -1:
            summary_text = summary_text[:last_period+1]
    
    return summary_text

if __name__ == "__main__":
    sample_text = (
        "Tesla's innovative approach to electric vehicles has transformed the auto industry. "
        "The company has consistently pushed the boundaries of technology, leading to significant market disruptions. "
        "However, recent market volatility has raised concerns among investors about the sustainability of Tesla's growth trajectory."
    )
    # Test the regular summary.
    print("Regular summary:")
    print(summarize_article(sample_text))
    
    # Test the final combined summary.
    aggregated_text = (
        "Tesla's innovative approach to electric vehicles has transformed the auto industry. "
        "The company has consistently pushed the boundaries of technology, leading to significant market disruptions. "
        "However, recent market volatility has raised concerns among investors about the sustainability of Tesla's growth trajectory."
    )
    print("\nFinal combined summary:")
    print(summarize_article(aggregated_text, final_summary=True))

