
import torch
from transformers import pipeline

# Initialize the sentiment analysis pipeline with FinBERT
sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_sentiment(text, chunk_size=512):
    # Tokenize the input text without truncation to get the full sequence
    tokens = sentiment_analyzer.tokenizer(text, return_tensors='pt', truncation=False)
    input_ids = tokens['input_ids'][0]
    attention_mask = tokens['attention_mask'][0]

    num_tokens = len(input_ids)
    num_chunks = (num_tokens + chunk_size - 1) // chunk_size
    sum_probs = None

    # Process text in chunks to avoid token length issues
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        input_id_chunk = input_ids[start:end].unsqueeze(0)
        attention_mask_chunk = attention_mask[start:end].unsqueeze(0)
        
        outputs = sentiment_analyzer.model(input_ids=input_id_chunk, attention_mask=attention_mask_chunk)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        
        if sum_probs is None:
            sum_probs = probs
        else:
            sum_probs += probs

    # Average the probabilities over all chunks
    avg_probs = sum_probs / num_chunks
    avg_probs_np = avg_probs.detach().numpy()[0]
    
    max_index = avg_probs_np.argmax()
    label = sentiment_analyzer.model.config.id2label[max_index]
    # Convert the probability to a native Python float
    probability = float(avg_probs_np[max_index])
    
    return {"label": label, "probability": probability}

if __name__ == "__main__":
    sample_text = "Tesla's stock is in a freefall. Its sales are plunging around the world. Even its most avid Wall Street bulls are turning cautious."
    result = analyze_sentiment(sample_text)
    print(f"Sentiment: {result['label']}, Probability: {result['probability']:.2f}")