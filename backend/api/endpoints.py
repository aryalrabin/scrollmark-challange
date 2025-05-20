from fastapi import APIRouter
import pandas as pd
from pathlib import Path
from collections import Counter
import re

# Define stopwords set
stopwords = {"i", "this", "the", "me", "so", "and", "a", "an", "to", "of", "in", "on", "for", "with", "is", "it",
             "that", "at", "as", "but", "by", "from", "or", "be", "are", "was", "were", "has", "have", "had", "not",
             "if", "we", "you", "he", "she", "they", "them", "my", "your", "our", "their", "s", "t", "all", "m"}

router = APIRouter()

DATA_PATH = Path(__file__).parent.parent / "data" / "processed_sentiment.csv"
df = None

def get_df():
    global df
    if df is None:
        if DATA_PATH.exists():
            df_local = pd.read_csv(DATA_PATH)
        else:
            df_local = pd.DataFrame()
        return df_local
    return df

@router.get("/sentiment/summary")
def sentiment_summary():
    df_local = get_df()
    if df_local is None or df_local.empty:
        return {"error": "No data loaded"}
    summary = df_local["sentiment"].value_counts(normalize=True).to_dict()
    return {"summary": summary}

@router.get("/sentiment/weekly")
def sentiment_weekly():
    df_local = get_df()
    if df_local is None or df_local.empty or "timestamp" not in df_local.columns:
        return {"error": "No data loaded or missing timestamp"}
    df_local["date"] = pd.to_datetime(df_local["timestamp"], errors="coerce", utc=True, format=None, infer_datetime_format=True)
    df_local["week"] = df_local["date"].dt.to_period("W").astype(str)
    result = df_local.groupby(["week", "sentiment"]).size().unstack(fill_value=0)
    return result.to_dict()

@router.get("/topics/trending")
def topics_trending():
    df_local = get_df()
    if df_local is None or df_local.empty or "comment_text" not in df_local.columns:
        return {"error": "No data loaded or missing comment_text"}
    words = []
    for text in df_local["comment_text"].dropna():
        words += [w for w in re.findall(r"\w+", str(text).lower()) if w not in stopwords]
    common = Counter(words).most_common(20)
    return {"trending": common}

@router.get("/comments/top")
def comments_top(page: int = 1, page_size: int = 10, sentiment: str = None, min_confidence: float = 0.9, n: int = 1000):
    df_local = get_df()
    if df_local is None or df_local.empty:
        return {"error": "No data loaded"}
    subset = df_local.copy()
    if sentiment:
        subset = subset[subset["sentiment"] == sentiment]
    subset = subset[subset["confidence"] >= min_confidence]
    top_comments = subset.nlargest(n, "confidence")[["comment_text", "sentiment", "confidence"]].to_dict(orient="records")
    total = len(top_comments)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = top_comments[start:end]
    return {"top_comments": paginated, "total": total, "page": page, "page_size": page_size}

@router.get("/sentiment/by-product")
def sentiment_by_product():
    df_local = get_df()
    if df_local is None or df_local.empty or "caption" not in df_local.columns:
        return {"error": "No data loaded or missing caption"}
    result = df_local.groupby(["caption", "sentiment"]).size().unstack(fill_value=0)
    return result.to_dict()

@router.get("/wordcloud")
def wordcloud():
    df_local = get_df()
    if df_local is None or df_local.empty or "comment_text" not in df_local.columns:
        return {"error": "No data loaded or missing comment_text"}

    words = []
    for text in df_local["comment_text"].dropna():
        words += [w for w in re.findall(r"\w+", str(text).lower()) if w not in stopwords]
    freq = Counter(words)
    return {"word_freq": dict(freq)}

@router.get("/comments/volume")
def comments_volume():
    df_local = get_df()
    if df_local is None or df_local.empty or "timestamp" not in df_local.columns:
        return {"error": "No data loaded or missing timestamp"}
    df_local["date"] = pd.to_datetime(df_local["timestamp"], errors="coerce", utc=True, format=None, infer_datetime_format=True)
    df_local["day"] = df_local["date"].dt.date
    result = df_local.groupby("day").size().to_dict()
    return {"volume": result}
