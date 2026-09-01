import React, { useState } from 'react';
import axios from 'axios';
import Hero from './components/Hero';
import Uploader from './components/Uploader';
import MetricCard from './components/MetricCard';
import ChartsPanel from './components/ChartsPanel';
import AIInsights from './components/AIInsights';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE}/analyze`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setData(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "An error occurred during analysis.");
    } finally {
      setLoading(false);
    }
  };

  const loadDemo = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE}/demo`);
      setData(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load demo data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Hero />
      <div className="container">
        {loading && (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <h2 style={{ color: 'var(--primary)' }}>Analyzing Data with AI...</h2>
            <p style={{ color: 'var(--text-muted)', marginTop: '8px' }}>This may take a few seconds.</p>
          </div>
        )}

        <div className="dashboard-grid">
          <div className="sidebar">
            <Uploader onUpload={handleUpload} isLoading={loading} onDemo={loadDemo} />
            
            {error && (
              <div className="glass-panel insight-danger" style={{ padding: '16px', marginBottom: '24px' }}>
                <p style={{ color: 'var(--danger)', fontWeight: 600 }}>{error}</p>
              </div>
            )}
            
            {data && data.kpis && (
              <div className="glass-panel" style={{ padding: '24px' }}>
                <h3 className="panel-title">Key Metrics</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  {Object.entries(data.kpis).map(([label, value], idx) => {
                    const colors = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6'];
                    const delay = (idx + 1) * 100;
                    const delayClass = delay <= 500 ? `delay-${delay}` : 'delay-500';
                    return (
                      <MetricCard 
                        key={label} 
                        label={label} 
                        value={value} 
                        colorClass={colors[idx % colors.length]} 
                        delayClass={delayClass}
                      />
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          <div className="main-content" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {data ? (
              <>
                <AIInsights insights={data.ai_insights} />
                <ChartsPanel chartsData={data.charts} />
              </>
            ) : (
              <div className="glass-panel" style={{ padding: '60px 20px', textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <h2 style={{ color: 'var(--text-muted)', marginBottom: '16px' }}>Ready for Analysis</h2>
                <p style={{ color: 'var(--text-muted)' }}>Upload your business data to generate AI insights and professional visualizations.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
