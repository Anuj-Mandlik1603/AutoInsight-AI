# pyrefly: ignore [missing-import]
from google import genai
from typing import Dict, Any, List
import json

class AIInsightGenerator:
    """Generate business insights using Google Gemini AI"""
    
    def __init__(self, api_key: str):
        """Initialize with Gemini API key"""
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.0-flash'
    
    def generate_insights(self, processed_data: Dict[str, Any], 
                         analysis_type: str = "Comprehensive Analysis",
                         depth: str = "Detailed") -> Dict[str, Any]:
        """Generate AI-powered business insights"""
        
        # Prepare context from processed data
        context = self._prepare_context(processed_data)
        
        # Create prompt based on analysis type
        prompt = self._create_prompt(context, analysis_type, depth)
        
        try:
            # Generate insights using Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # Parse and structure the response
            insights = self._parse_response(response.text)
            
            return insights
        
        except Exception as e:
            return {
                'executive_summary': f"Error generating insights: {str(e)}",
                'key_findings': ["Unable to generate AI insights. Please check API key."],
                'recommendations': ["Verify Gemini API key is valid"],
                'risks': []
            }
    
    def _prepare_context(self, data: Dict[str, Any]) -> str:
        """Prepare structured context from processed data"""
        
        summary = data.get('summary', {})
        kpis = data.get('kpis', {})
        trends = data.get('trends', {})
        anomalies = data.get('anomalies', {})
        correlations = data.get('correlations', {})
        
        context = f"""
DATASET SUMMARY:
- Total Records: {summary.get('total_rows', 'N/A')}
- Total Columns: {summary.get('total_columns', 'N/A')}
- Numeric Columns: {summary.get('numeric_columns', 'N/A')}
- Missing Values: {summary.get('missing_values', 0)}

KEY PERFORMANCE INDICATORS:
"""
        
        # Add KPI details
        if kpis:
            for kpi_name, kpi_data in kpis.items():
                context += f"\n{kpi_name.upper()}:\n"
                for key, value in kpi_data.items():
                    if key != 'column':
                        context += f"  - {key}: {value}\n"
        else:
            context += "No specific KPIs detected\n"
        
        context += "\nTREND ANALYSIS:\n"
        if trends:
            for col, trend_data in trends.items():
                direction = trend_data.get('direction', 'stable')
                growth = trend_data.get('growth_rate', 0)
                context += f"- {col}: {direction} trend, {growth:.2f}% growth rate\n"
        else:
            context += "No clear trends detected\n"
        
        context += "\nANOMALIES DETECTED:\n"
        if anomalies:
            for col, anomaly_data in anomalies.items():
                count = anomaly_data.get('count', 0)
                percentage = anomaly_data.get('percentage', 0)
                context += f"- {col}: {count} anomalies found ({percentage:.2f}% of data)\n"
        else:
            context += "No significant anomalies detected\n"
        
        context += "\nCORRELATION INSIGHTS:\n"
        if correlations and 'strong_correlations' in correlations:
            strong_corrs = correlations['strong_correlations']
            if strong_corrs:
                for corr in strong_corrs[:5]:  # Top 5 correlations
                    context += f"- {corr['var1']} and {corr['var2']}: {corr['correlation']:.2f} ({corr['strength']})\n"
            else:
                context += "No strong correlations found\n"
        else:
            context += "Correlation analysis not available\n"
        
        return context
    
    def _create_prompt(self, context: str, analysis_type: str, depth: str) -> str:
        """Create detailed prompt for Gemini"""
        
        base_prompt = f"""You are a senior business intelligence analyst. Analyze the following data and provide professional business insights.

{context}

ANALYSIS TYPE: {analysis_type}
DEPTH LEVEL: {depth}

Generate a comprehensive business intelligence report with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
   - High-level overview of the data
   - Most critical insight
   - Overall business health assessment

2. KEY FINDINGS (4-6 bullet points)
   - Specific numerical insights
   - Important trends and patterns
   - Notable achievements or concerns
   - Data-backed observations

3. BUSINESS RECOMMENDATIONS (4-5 actionable items)
   - Specific actions to take
   - Priority areas for improvement
   - Growth opportunities
   - Cost optimization suggestions

4. RISK ALERTS (if any)
   - Potential risks or red flags
   - Anomalies that need attention
   - Warning signs in the data

IMPORTANT INSTRUCTIONS:
- Be specific with numbers and percentages
- Use business-friendly language (avoid technical jargon)
- Provide actionable, practical recommendations
- Base all insights strictly on the provided data
- If data is limited, acknowledge it
- Format your response clearly with section headers
- Be concise but thorough

Generate the report now:
"""
        
        return base_prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        
        insights = {
            'executive_summary': '',
            'key_findings': [],
            'recommendations': [],
            'risks': []
        }
        
        try:
            # Split response into sections
            sections = response_text.split('\n')
            
            current_section = None
            
            for line in sections:
                line = line.strip()
                
                if not line:
                    continue
                
                # Detect sections
                if 'EXECUTIVE SUMMARY' in line.upper():
                    current_section = 'summary'
                    continue
                elif 'KEY FINDING' in line.upper():
                    current_section = 'findings'
                    continue
                elif 'RECOMMENDATION' in line.upper() or 'ACTION' in line.upper():
                    current_section = 'recommendations'
                    continue
                elif 'RISK' in line.upper() or 'ALERT' in line.upper() or 'WARNING' in line.upper():
                    current_section = 'risks'
                    continue
                
                # Parse content
                if current_section == 'summary':
                    if line and not line.startswith('#'):
                        insights['executive_summary'] += line + ' '
                
                elif current_section == 'findings':
                    if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                        insights['key_findings'].append(line.lstrip('-•* '))
                    elif line[0].isdigit() and '.' in line[:3]:
                        insights['key_findings'].append(line.split('.', 1)[1].strip())
                
                elif current_section == 'recommendations':
                    if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                        insights['recommendations'].append(line.lstrip('-•* '))
                    elif line[0].isdigit() and '.' in line[:3]:
                        insights['recommendations'].append(line.split('.', 1)[1].strip())
                
                elif current_section == 'risks':
                    if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                        insights['risks'].append(line.lstrip('-•* '))
                    elif line[0].isdigit() and '.' in line[:3]:
                        insights['risks'].append(line.split('.', 1)[1].strip())
            
            # Clean up
            insights['executive_summary'] = insights['executive_summary'].strip()
            
            # Ensure we have some content
            if not insights['executive_summary']:
                # Take first few lines as summary
                lines = [l for l in sections if l.strip() and not l.strip().startswith('#')]
                insights['executive_summary'] = ' '.join(lines[:3])
            
            if not insights['key_findings']:
                insights['key_findings'] = ["Analysis completed - review visualizations for detailed insights"]
            
            if not insights['recommendations']:
                insights['recommendations'] = ["Continue monitoring key metrics", "Analyze trends over time"]
        
        except Exception as e:
            insights['executive_summary'] = response_text[:500]
            insights['key_findings'] = ["See executive summary for details"]
            insights['recommendations'] = ["Review the full analysis"]
        
        return insights
