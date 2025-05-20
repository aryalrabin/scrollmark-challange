import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# Load data
df = pd.read_csv('engagements.csv')
df.dropna(subset=['comment_text'], inplace=True)

# Load model and tokenizer
MODEL = 'cardiffnlp/twitter-roberta-base-sentiment'
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
labels = ['negative', 'neutral', 'positive']

def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1).numpy().flatten()
    sentiment = labels[np.argmax(probs)]
    confidence = float(np.max(probs))
    return sentiment, confidence

# Apply sentiment analysis
df[['sentiment', 'confidence']] = df['comment_text'].apply(
    lambda x: pd.Series(get_sentiment(str(x)))
)

# Save processed data
df.to_csv('processed_sentiment.csv', index=False)
print('Processed data saved to processed_sentiment.csv')
