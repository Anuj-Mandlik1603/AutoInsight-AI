# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
import pandas as pd
import io

from data_processor import DataProcessor
from ai_insights import AIInsightGenerator

app = FastAPI(title="AutoInsight AI API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "AIzaSyC_MuHH5duRNUncA28gDF-d4uEcmaJ9Z4U"

def process_dataframe(df: pd.DataFrame):
    try:
        processor = DataProcessor(df)
        processed_data = processor.process()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")
        
    try:
        ai_gen = AIInsightGenerator(API_KEY)
        ai_insights = ai_gen.generate_insights(
            processed_data, "Comprehensive Analysis", "Detailed"
        )
    except Exception as e:
        ai_insights = {
            'executive_summary': str(e),
            'key_findings': ["Unable to generate insights. Check API key."],
            'recommendations': ["Verify your internet connection and API key."],
            'risks': []
        }

    # Clean the pandas types so they can be JSON serialized properly
    # pyrefly: ignore [missing-import]
    import numpy as np
    
    # To avoid JSON serialization errors from NaN or Infinity
    df_clean = df.replace([np.inf, -np.inf], np.nan).fillna("")

    # Extract charts data
    numeric_cols = processed_data['column_info']['numeric']
    cat_cols = processed_data['column_info']['categorical']
    
    sales_profit_data = {}
    if len(numeric_cols) > 0:
        x_col = df.index.astype(str).tolist()
        for c in df.columns:
            if df[c].dtype == 'object' or str(df[c].dtype).startswith('datetime'):
                x_col = df[c].fillna("").astype(str).tolist()
                break
        
        y1 = numeric_cols[0] if numeric_cols else None
        y2 = numeric_cols[1] if len(numeric_cols) > 1 else None
        
        sales_profit_data = {
            "x": x_col,
            "y1_name": y1,
            "y1": df_clean[y1].tolist() if y1 else [],
            "y2_name": y2,
            "y2": df_clean[y2].tolist() if y2 else []
        }

    regional_data = {}
    if 'Region' in df.columns and numeric_cols:
        grp = df.groupby('Region')[numeric_cols[0]].sum().reset_index()
        total = grp[numeric_cols[0]].sum()
        grp['pct'] = ((grp[numeric_cols[0]] / total - 0.25) * 100).round(1)
        regional_data = {
            "regions": grp['Region'].tolist(),
            "percentages": grp['pct'].tolist()
        }

    pie_data = {}
    pie_col = None
    for c in cat_cols:
        if df[c].nunique() <= 10: 
            pie_col = c
            break
    if pie_col and numeric_cols:
        grp = df.groupby(pie_col)[numeric_cols[0]].sum().reset_index().nlargest(4, numeric_cols[0])
        pie_data = {
            "labels": grp[pie_col].tolist(),
            "values": grp[numeric_cols[0]].tolist()
        }

    # kpi vals
    kpi_vals = {}
    for col in numeric_cols[:4]:
        kpi_vals[col] = float(df[col].sum())

    return {
        "kpis": kpi_vals,
        "ai_insights": ai_insights,
        "charts": {
            "sales_profit": sales_profit_data,
            "regional": regional_data,
            "pie": pie_data,
            "pie_title": f"Top Products by {numeric_cols[0]}" if pie_col else ""
        }
    }

@app.post("/api/analyze")
async def analyze_data(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV or Excel file.")
    
    contents = await file.read()
    
    try:
        if file.filename.endswith('.csv'):
            for enc in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    df = pd.read_csv(io.BytesIO(contents), encoding=enc)
                    break
                except Exception:
                    continue
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
        
    return process_dataframe(df)

@app.get("/api/demo")
async def get_demo_data():
    # pyrefly: ignore [missing-import]
    import numpy as np
    np.random.seed(42)
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    sales  = [320,380,290,410,450,390,480,520,460,540,580,620]
    profit = [60,75,45,90,95,70,100,110,85,120,130,150]
    df = pd.DataFrame({
        'Month': months, 'Sales': sales, 'Profit': profit,
        'Region': ['North','South','East','West','North','South','East','West','North','South','East','West'],
        'Product': ['Product A','Product B','Product C','Others']*3,
        'Discount': np.random.uniform(5,30,12).round(1)
    })
    return process_dataframe(df)

if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
