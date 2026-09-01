import React from 'react';

export default function MetricCard({ label, value, colorClass, delayClass = '' }) {
  // Format large numbers
  const formatValue = (val) => {
    if (typeof val !== 'number') return val;
    if (Math.abs(val) >= 1_000_000) return `$${(val / 1_000_000).toFixed(2)}M`;
    if (Math.abs(val) >= 1_000) return `$${(val / 1_000).toFixed(1)}K`;
    return val.toFixed(1);
  };

  return (
    <div className={`metric-card animate-slide-up ${delayClass}`} style={{ borderBottomColor: colorClass }}>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{formatValue(value)}</div>
    </div>
  );
}
