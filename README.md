# 📊 Sentiment & Trend Reporting Dashboard for Instagram Comments

**Client:** Treehut (Skincare Brand)

## 🎯 Objective

Build a full-stack application that analyzes Instagram comments for sentiment and trends, and displays insights via an interactive dashboard.

---

## ✅ Deliverables

### 1. Modeling & NLP
- Use `cardiffnlp/twitter-roberta-base-sentiment` for  sentiment analysis
- Drop missing comments
- Extract sentiment, confidence
- save to `data/processed_sentiment.csv`

### 2. FastAPI Backend
- Process ~18,000 Instagram comments (with timestamp, media_id, caption, comment_text)
- Perform sentiment analysis
- Extract trending topics and keyword frequencies
- Group metrics over time (daily/weekly)
- API Endpoints:
    - `GET /sentiment/summary`
    - `GET /sentiment/weekly`
    - `GET /topics/trending`
    - `GET /comments/top`
    - `GET /sentiment/by-product`
    - `GET /wordcloud`
    - `GET /comments/volume`

### 3. React Frontend
- Interactive dashboard using React + Chart.js
- Features:
    - Line chart (weekly sentiment)
    - Pie chart (overall sentiment)
    - Word cloud
    - Trending keyword list
    - Top comments viewer
- Styling with Tailwind CSS

## Installation and Running the Project

### 1. Create and Activate Virtual Environment
- From the `backend` directory, run:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Data Preparation
- Ensure your processed Instagram sentiment data is available at `backend/data/processed_sentiment.csv`.
- To preprocess raw data, run:
```sh
python data/process_sentiment.py
```
- If you need to preprocess data, use the scripts in `backend/data/` as needed.

### 3. Backend Setup (FastAPI)
```sh
# Run FastAPI server from project root:
cd ..
uvicorn backend.main:app --reload
```

### 4. Frontend Setup (React)
- Requires Node.js and npm. Install from https://nodejs.org/ if not present.
```sh
cd frontend
npm install
npm start
```

### 5. Running Tests
- From the project root:
```sh
source backend/venv/bin/activate
pytest backend/test
```

### 6. Accessing the Dashboard
- Visit [http://localhost:3000](http://localhost:3000) for the React frontend.
- The FastAPI backend runs at [http://localhost:8000](http://localhost:8000).

---

For any issues, check the README sections below or open an issue.
