import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Pie, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
} from 'chart.js';
import './App.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

function App() {
  const [sentiment, setSentiment] = useState(null);
  const [trending, setTrending] = useState([]);
  const [topComments, setTopComments] = useState([]);
  const [weekly, setWeekly] = useState(null);
  const [wordFreq, setWordFreq] = useState(null);
  const [loading, setLoading] = useState(true);
  const API_URL = 'http://localhost:8000';

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const [sentimentRes, trendingRes, commentsRes, weeklyRes, wordcloudRes] = await Promise.all([
          axios.get(`${API_URL}/sentiment/summary`),
          axios.get(`${API_URL}/topics/trending`),
          axios.get(`${API_URL}/comments/top`, { params: { n: 10 } }),
          axios.get(`${API_URL}/sentiment/weekly`),
          axios.get(`${API_URL}/wordcloud`)
        ]);
        setSentiment(sentimentRes.data.summary);
        setTrending(trendingRes.data.trending);
        setTopComments(commentsRes.data.top_comments);
        setWeekly(weeklyRes.data);
        setWordFreq(wordcloudRes.data.word_freq);
      } catch (err) {
        setSentiment(null);
        setTrending([]);
        setTopComments([]);
        setWeekly(null);
        setWordFreq(null);
      }
      setLoading(false);
    }
    fetchData();
  }, []);

  // Pie chart (sentiment summary)
  const pieData = sentiment ? {
    labels: Object.keys(sentiment),
    datasets: [
      {
        data: Object.values(sentiment),
        backgroundColor: ['#22c55e', '#facc15', '#ef4444'],
        borderWidth: 1,
      },
    ],
  } : null;

  // Bar chart (weekly sentiment)
  let barData = null;
  if (weekly) {
    const weekLabels = Object.keys(weekly);
    const sentiments = Object.keys(weekly[weekLabels[0]] || {});
    const datasets = sentiments.map((s, idx) => ({
      label: s,
      data: weekLabels.map(w => weekly[w][s] || 0),
      backgroundColor: ['#22c55e', '#facc15', '#ef4444'][idx % 3],
    }));
    barData = {
      labels: weekLabels,
      datasets,
    };
  }

  // Word count bar chart (top 20 words)
  let wordBarData = null;
  if (wordFreq) {
    const sorted = Object.entries(wordFreq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20);
    wordBarData = {
      labels: sorted.map(([word]) => word),
      datasets: [
        {
          label: 'Word Count',
          data: sorted.map(([, count]) => count),
          backgroundColor: '#60a5fa',
        },
      ],
    };
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Instagram Sentiment & Trend Dashboard</h1>
        {loading ? <p>Loading data...</p> : (
          <>
            <section>
              <h2>Sentiment Distribution</h2>
              {pieData ? <Pie data={pieData} /> : <p>No sentiment data.</p>}
            </section>
            <section>
              <h2>Weekly Sentiment Trend</h2>
              {barData ? <Bar data={barData} /> : <p>No weekly trend data.</p>}
            </section>
            <section>
              <h2>Word Count (Top 20)</h2>
              {wordBarData ? <Bar data={wordBarData} options={{
                plugins: { legend: { display: false } },
                indexAxis: 'y',
                scales: { x: { beginAtZero: true } },
                responsive: true,
                maintainAspectRatio: false,
                height: 400
              }} /> : <p>No word count data.</p>}
            </section>
            <section>
              <h2>Top Comments</h2>
              <ol>
                {topComments.map((c, i) => (
                  <li key={i}>
                    <b>{c.sentiment}</b> ({(c.confidence * 100).toFixed(1)}%): {c.comment_text}
                  </li>
                ))}
              </ol>
            </section>
            <section>
              <h2>Trending Keywords</h2>
              <ol>
                {trending.map(([word, count]) => (
                  <li key={word}>{word} ({count})</li>
                ))}
              </ol>
            </section>
          </>
        )}
      </header>
    </div>
  );
}

export default App;
