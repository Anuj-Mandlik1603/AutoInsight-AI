# pyrefly: ignore [missing-import]
import plotly.express as px
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go
# pyrefly: ignore [missing-import]
from plotly.subplots import make_subplots
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
from typing import Dict, Any

class VisualizationEngine:
    """Generate interactive visualizations using Plotly"""
    
    def __init__(self, processed_data: Dict[str, Any]):
        self.data = processed_data
        self.df = processed_data['dataframe']
        self.color_scheme = px.colors.qualitative.Set3
    
    def generate_all_charts(self) -> Dict[str, go.Figure]:
        """Generate all relevant charts"""
        charts = {}
        
        # Generate appropriate charts based on data
        numeric_cols = self.data['column_info']['numeric']
        categorical_cols = self.data['column_info']['categorical']
        date_cols = self.data['column_info']['date']
        
        # KPI Overview Chart
        if self.data['kpis']:
            charts['KPI Overview'] = self.create_kpi_chart()
        
        # Trend Charts
        if date_cols and numeric_cols:
            charts['Trend Analysis'] = self.create_trend_chart(date_cols[0], numeric_cols[:3])
        
        # Distribution Charts
        if numeric_cols:
            charts['Distribution Analysis'] = self.create_distribution_chart(numeric_cols[0])
        
        # Categorical Analysis
        if categorical_cols and numeric_cols:
            charts['Category Comparison'] = self.create_category_chart(categorical_cols[0], numeric_cols[0])
        
        # Correlation Heatmap
        if len(numeric_cols) > 1:
            charts['Correlation Matrix'] = self.create_correlation_heatmap()
        
        # Top Performers
        if categorical_cols and numeric_cols:
            charts['Top Performers'] = self.create_top_performers_chart(categorical_cols[0], numeric_cols[0])
        
        return charts
    
    def create_kpi_chart(self) -> go.Figure:
        """Create KPI overview chart"""
        kpis = self.data['kpis']
        
        kpi_names = []
        kpi_values = []
        
        for kpi_name, kpi_data in kpis.items():
            if 'total' in kpi_data:
                kpi_names.append(kpi_name.title())
                kpi_values.append(kpi_data['total'])
        
        fig = go.Figure(data=[
            go.Bar(
                x=kpi_names,
                y=kpi_values,
                marker=dict(
                    color=kpi_values,
                    colorscale='Viridis',
                    showscale=True
                ),
                text=[f'${v:,.0f}' if v > 1000 else f'{v:.2f}' for v in kpi_values],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title='Key Performance Indicators Overview',
            xaxis_title='Metrics',
            yaxis_title='Value',
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_trend_chart(self, date_col: str, value_cols: list) -> go.Figure:
        """Create time-series trend chart"""
        df_sorted = self.df.sort_values(by=date_col)
        
        fig = go.Figure()
        
        for col in value_cols:
            fig.add_trace(go.Scatter(
                x=df_sorted[date_col],
                y=df_sorted[col],
                mode='lines+markers',
                name=col,
                line=dict(width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title='Trend Analysis Over Time',
            xaxis_title='Date',
            yaxis_title='Value',
            template='plotly_white',
            height=400,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_distribution_chart(self, column: str) -> go.Figure:
        """Create distribution histogram with KDE"""
        fig = go.Figure()
        
        # Histogram
        fig.add_trace(go.Histogram(
            x=self.df[column],
            name='Distribution',
            marker_color='rgba(102, 126, 234, 0.6)',
            nbinsx=30
        ))
        
        fig.update_layout(
            title=f'Distribution of {column}',
            xaxis_title=column,
            yaxis_title='Frequency',
            template='plotly_white',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_category_chart(self, category_col: str, value_col: str) -> go.Figure:
        """Create category comparison chart"""
        
        # Group by category and sum values
        grouped = self.df.groupby(category_col)[value_col].sum().sort_values(ascending=False).head(10)
        
        fig = go.Figure(data=[
            go.Bar(
                x=grouped.index,
                y=grouped.values,
                marker=dict(
                    color=grouped.values,
                    colorscale='Blues',
                    showscale=False
                ),
                text=[f'{v:,.0f}' for v in grouped.values],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title=f'{value_col} by {category_col} (Top 10)',
            xaxis_title=category_col,
            yaxis_title=value_col,
            template='plotly_white',
            height=400,
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_correlation_heatmap(self) -> go.Figure:
        """Create correlation heatmap"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        corr_matrix = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Correlation Matrix',
            template='plotly_white',
            height=500,
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_top_performers_chart(self, category_col: str, value_col: str) -> go.Figure:
        """Create top performers chart"""
        
        # Get top 10 performers
        top_performers = self.df.groupby(category_col)[value_col].sum().sort_values(ascending=True).tail(10)
        
        fig = go.Figure(go.Bar(
            y=top_performers.index,
            x=top_performers.values,
            orientation='h',
            marker=dict(
                color=top_performers.values,
                colorscale='Greens',
                showscale=False
            ),
            text=[f'{v:,.0f}' for v in top_performers.values],
            textposition='outside'
        ))
        
        fig.update_layout(
            title=f'Top 10 {category_col} by {value_col}',
            xaxis_title=value_col,
            yaxis_title=category_col,
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_pie_chart(self, category_col: str, value_col: str) -> go.Figure:
        """Create pie chart for distribution"""
        
        grouped = self.df.groupby(category_col)[value_col].sum().head(8)
        
        fig = go.Figure(data=[go.Pie(
            labels=grouped.index,
            values=grouped.values,
            hole=0.3,
            marker=dict(colors=self.color_scheme)
        )])
        
        fig.update_layout(
            title=f'{value_col} Distribution by {category_col}',
            template='plotly_white',
            height=400
        )
        
        return fig
