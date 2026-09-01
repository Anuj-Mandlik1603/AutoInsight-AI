import React from 'react';
import Plot from 'react-plotly.js';

export default function ChartsPanel({ chartsData }) {
  if (!chartsData) return null;

  const { sales_profit, regional, pie, pie_title } = chartsData;

  const getSalesProfitData = () => {
    if (!sales_profit || !sales_profit.x || sales_profit.x.length === 0) return [];
    
    const data = [];
    if (sales_profit.y1_name) {
      data.push({
        x: sales_profit.x,
        y: sales_profit.y1,
        name: sales_profit.y1_name,
        type: 'bar',
        marker: { color: 'rgba(79, 70, 229, 0.75)' }
      });
    }
    
    if (sales_profit.y2_name) {
      data.push({
        x: sales_profit.x,
        y: sales_profit.y2,
        name: sales_profit.y2_name,
        type: 'scatter',
        mode: 'lines+markers',
        yaxis: 'y2',
        line: { color: '#ec4899', width: 3 },
        marker: { size: 8 }
      });
    }
    
    return data;
  };

  const salesLayout = {
    title: { text: "Trend Analysis", font: { family: 'Outfit', size: 18 } },
    margin: { l: 40, r: 40, t: 50, b: 40 },
    height: 350,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    legend: { orientation: 'h', y: 1.15 },
    hovermode: 'x unified',
    yaxis: { gridcolor: '#f3f4f6' },
    yaxis2: { overlaying: 'y', side: 'right', showgrid: false },
    font: { family: 'Inter' }
  };

  const getRegionalData = () => {
    if (!regional || !regional.regions) return [];
    return [{
      x: regional.regions,
      y: regional.percentages,
      type: 'bar',
      text: regional.percentages.map(p => `${p > 0 ? '+' : ''}${p}%`),
      textposition: 'outside',
      marker: { color: ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6'] }
    }];
  };

  const regionalLayout = {
    title: { text: "Regional Performance", font: { family: 'Outfit', size: 18 } },
    margin: { l: 20, r: 20, t: 50, b: 40 },
    height: 250,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    yaxis: { showticklabels: false, showgrid: false },
    xaxis: { showgrid: false },
    font: { family: 'Inter' }
  };

  const getPieData = () => {
    if (!pie || !pie.labels) return [];
    return [{
      labels: pie.labels,
      values: pie.values,
      type: 'pie',
      hole: 0.4,
      marker: { colors: ['#4f46e5', '#10b981', '#f59e0b', '#ec4899'] },
      textinfo: 'percent'
    }];
  };

  const pieLayout = {
    title: { text: pie_title || "Distribution", font: { family: 'Outfit', size: 18 } },
    margin: { l: 20, r: 20, t: 50, b: 20 },
    height: 250,
    paper_bgcolor: 'rgba(0,0,0,0)',
    font: { family: 'Inter' }
  };

  return (
    <div className="charts-container">
      {sales_profit?.x?.length > 0 && (
        <div className="chart-wrapper">
          <Plot 
            data={getSalesProfitData()} 
            layout={salesLayout} 
            useResizeHandler={true} 
            style={{ width: '100%', height: '100%' }} 
            config={{ displayModeBar: false }}
          />
        </div>
      )}
      
      <div className="chart-row">
        {regional?.regions?.length > 0 && (
          <div className="chart-wrapper">
            <Plot 
              data={getRegionalData()} 
              layout={regionalLayout} 
              useResizeHandler={true} 
              style={{ width: '100%', height: '100%' }} 
              config={{ displayModeBar: false }}
            />
          </div>
        )}
        
        {pie?.labels?.length > 0 && (
          <div className="chart-wrapper">
            <Plot 
              data={getPieData()} 
              layout={pieLayout} 
              useResizeHandler={true} 
              style={{ width: '100%', height: '100%' }} 
              config={{ displayModeBar: false }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
