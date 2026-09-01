import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

class DataProcessor:
    """Process and analyze uploaded business data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.insights = {}
    
    def process(self) -> Dict[str, Any]:
        """Main processing pipeline"""
        # Clean data
        self.clean_data()
        
        # Detect column types
        column_info = self.detect_column_types()
        
        # Calculate statistics
        statistics = self.calculate_statistics()
        
        # Detect KPIs
        kpis = self.detect_kpis()
        
        # Trend analysis
        trends = self.analyze_trends()
        
        # Anomaly detection
        anomalies = self.detect_anomalies()
        
        # Correlation analysis
        correlations = self.analyze_correlations()
        
        return {
            'dataframe': self.df,
            'column_info': column_info,
            'statistics': statistics,
            'kpis': kpis,
            'trends': trends,
            'anomalies': anomalies,
            'correlations': correlations,
            'summary': self.generate_summary()
        }
    
    def clean_data(self):
        """Clean and prepare data"""
        # Remove completely empty rows
        self.df.dropna(how='all', inplace=True)
        
        # Handle missing values
        for col in self.df.columns:
            if self.df[col].dtype in ['float64', 'int64']:
                # Fill numeric columns with median
                self.df[col].fillna(self.df[col].median(), inplace=True)
            else:
                # Fill categorical with mode or 'Unknown'
                mode_val = self.df[col].mode()
                if len(mode_val) > 0:
                    self.df[col].fillna(mode_val[0], inplace=True)
                else:
                    self.df[col].fillna('Unknown', inplace=True)
        
        # Convert date columns
        for col in self.df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                except:
                    pass
    
    def detect_column_types(self) -> Dict[str, List[str]]:
        """Detect and categorize column types"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        date_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        
        return {
            'numeric': numeric_cols,
            'categorical': categorical_cols,
            'date': date_cols
        }
    
    def calculate_statistics(self) -> pd.DataFrame:
        """Calculate comprehensive statistics"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return pd.DataFrame()
        
        stats = self.df[numeric_cols].describe().T
        stats['median'] = self.df[numeric_cols].median()
        stats['variance'] = self.df[numeric_cols].var()
        stats['skewness'] = self.df[numeric_cols].skew()
        
        return stats
    
    def detect_kpis(self) -> Dict[str, Any]:
        """Automatically detect Key Performance Indicators"""
        kpis = {}
        
        # Common business KPI column names
        revenue_keywords = ['revenue', 'sales', 'income', 'earnings']
        profit_keywords = ['profit', 'margin', 'net']
        quantity_keywords = ['quantity', 'units', 'count', 'volume']
        
        for col in self.df.columns:
            col_lower = col.lower()
            
            # Detect revenue metrics
            if any(keyword in col_lower for keyword in revenue_keywords):
                if self.df[col].dtype in ['float64', 'int64']:
                    kpis['revenue'] = {
                        'column': col,
                        'total': float(self.df[col].sum()),
                        'average': float(self.df[col].mean()),
                        'max': float(self.df[col].max()),
                        'min': float(self.df[col].min())
                    }
            
            # Detect profit metrics
            if any(keyword in col_lower for keyword in profit_keywords):
                if self.df[col].dtype in ['float64', 'int64']:
                    kpis['profit'] = {
                        'column': col,
                        'total': float(self.df[col].sum()),
                        'average': float(self.df[col].mean()),
                        'margin': float((self.df[col].sum() / self.df[self.df.columns[0]].count()) * 100) if len(self.df) > 0 else 0
                    }
            
            # Detect quantity metrics
            if any(keyword in col_lower for keyword in quantity_keywords):
                if self.df[col].dtype in ['float64', 'int64']:
                    kpis['quantity'] = {
                        'column': col,
                        'total': float(self.df[col].sum()),
                        'average': float(self.df[col].mean())
                    }
        
        return kpis
    
    def analyze_trends(self) -> Dict[str, Any]:
        """Analyze trends in time-series data"""
        trends = {}
        
        # Find date columns
        date_cols = self.df.select_dtypes(include=['datetime64']).columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(date_cols) > 0 and len(numeric_cols) > 0:
            date_col = date_cols[0]
            
            # Sort by date
            df_sorted = self.df.sort_values(by=date_col)
            
            for num_col in numeric_cols[:3]:  # Analyze first 3 numeric columns
                values = df_sorted[num_col].values
                
                if len(values) > 1:
                    # Calculate trend
                    x = np.arange(len(values))
                    slope = np.polyfit(x, values, 1)[0]
                    
                    # Calculate growth rate
                    if values[0] != 0:
                        growth_rate = ((values[-1] - values[0]) / abs(values[0])) * 100
                    else:
                        growth_rate = 0
                    
                    trends[num_col] = {
                        'slope': float(slope),
                        'direction': 'increasing' if slope > 0 else 'decreasing',
                        'growth_rate': float(growth_rate),
                        'volatility': float(np.std(values))
                    }
        
        return trends
    
    def detect_anomalies(self) -> Dict[str, List]:
        """Detect anomalies using statistical methods"""
        anomalies = {}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            # Using IQR method
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            
            if len(outliers) > 0:
                anomalies[col] = {
                    'count': len(outliers),
                    'percentage': (len(outliers) / len(self.df)) * 100,
                    'values': outliers[col].tolist()[:5]  # First 5 outliers
                }
        
        return anomalies
    
    def analyze_correlations(self) -> Dict[str, Any]:
        """Analyze correlations between numeric variables"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return {}
        
        corr_matrix = self.df[numeric_cols].corr()
        
        # Find strong correlations (> 0.7 or < -0.7)
        strong_correlations = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': float(corr_value),
                        'strength': 'strong positive' if corr_value > 0 else 'strong negative'
                    })
        
        return {
            'matrix': corr_matrix,
            'strong_correlations': strong_correlations
        }
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate overall data summary"""
        return {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'numeric_columns': len(self.df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(self.df.select_dtypes(include=['object']).columns),
            'date_columns': len(self.df.select_dtypes(include=['datetime64']).columns),
            'missing_values': int(self.df.isnull().sum().sum()),
            'duplicate_rows': int(self.df.duplicated().sum()),
            'memory_usage_kb': float(self.df.memory_usage(deep=True).sum() / 1024)
        }
