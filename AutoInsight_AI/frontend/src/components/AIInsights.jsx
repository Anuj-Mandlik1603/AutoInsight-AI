import React from 'react';
import { FiTrendingUp, FiAlertTriangle, FiCheckCircle, FiInfo } from 'react-icons/fi';

export default function AIInsights({ insights }) {
  if (!insights) return null;

  return (
    <div className="glass-panel animate-slide-up delay-100" style={{ padding: '24px' }}>
      <h3 className="panel-title" style={{ color: '#4f46e5' }}>
        <span style={{ fontSize: '1.5rem' }}>✨</span> AI-Generated Insights
      </h3>
      
      <div style={{ marginBottom: '24px' }}>
        <h4 style={{ marginBottom: '12px', fontSize: '1.1rem' }}>Executive Summary</h4>
        <p style={{ lineHeight: '1.6', fontSize: '1rem' }}>
          {insights.executive_summary}
        </p>
      </div>

      <div className="dashboard-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '24px', marginTop: 0 }}>
        <div>
          <h4 style={{ marginBottom: '16px', fontSize: '1.1rem' }}>Key Findings</h4>
          {insights.key_findings?.map((finding, idx) => (
            <div key={idx} className={`insight-item insight-info animate-slide-up delay-${Math.min((idx + 1) * 100, 500)}`}>
              <FiInfo className="insight-icon" style={{ color: 'var(--info)' }} />
              <div>{finding}</div>
            </div>
          ))}
        </div>

        <div>
          <h4 style={{ marginBottom: '16px', fontSize: '1.1rem' }}>Recommendations</h4>
          {insights.recommendations?.map((rec, idx) => (
            <div key={idx} className={`insight-item insight-success animate-slide-up delay-${Math.min((idx + 1) * 100, 500)}`}>
              <FiCheckCircle className="insight-icon" style={{ color: 'var(--success)' }} />
              <div>{rec}</div>
            </div>
          ))}

          {insights.risks && insights.risks.length > 0 && (
            <div style={{ marginTop: '24px' }}>
              <h4 style={{ marginBottom: '16px', fontSize: '1.1rem', color: 'var(--danger)' }}>Risk Alerts</h4>
              {insights.risks.map((risk, idx) => (
                <div key={idx} className={`insight-item insight-danger animate-slide-up delay-${Math.min((idx + 1) * 100, 500)}`}>
                  <FiAlertTriangle className="insight-icon" style={{ color: 'var(--danger)' }} />
                  <div>{risk}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
