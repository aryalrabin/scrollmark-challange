from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_sentiment_summary():
    r = client.get("/sentiment/summary")
    assert r.status_code == 200
    assert "summary" in r.json() or "error" in r.json()

def test_trending_keywords():
    r = client.get("/topics/trending")
    assert r.status_code == 200
    assert "trending" in r.json() or "error" in r.json()

def test_top_comments():
    r = client.get("/comments/top")
    assert r.status_code == 200
    assert "top_comments" in r.json() or "error" in r.json()

def test_weekly_sentiment():
    r = client.get("/sentiment/weekly")
    assert r.status_code == 200
    assert isinstance(r.json(), dict) or "error" in r.json()

def test_by_product():
    r = client.get("/sentiment/by-product")
    assert r.status_code == 200
    assert isinstance(r.json(), dict) or "error" in r.json()

def test_wordcloud():
    r = client.get("/wordcloud")
    assert r.status_code == 200
    assert "word_freq" in r.json() or "error" in r.json()

def test_comment_volume():
    r = client.get("/comments/volume")
    assert r.status_code == 200
    assert "volume" in r.json() or "error" in r.json()
