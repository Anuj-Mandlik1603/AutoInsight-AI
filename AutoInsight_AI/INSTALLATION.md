# AutoInsight AI - Installation & Deployment Guide

## Quick Start Guide

### 1. Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Google Gemini API Key (Free at: https://makersuite.google.com/app/apikey)

### 2. Installation Steps

```bash
# Navigate to project directory
cd "C:\Users\Anuj\OneDrive\Desktop\Coding Languages\Mini Project\CEMP\AutoInsight_AI"

# Install dependencies
pip install -r requirements.txt
```

### 3. Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the API key (keep it secure)

### 4. Run the Application

```bash
# Run Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 5. Using AutoInsight AI

1. **Enter API Key**: Paste your Gemini API key in the sidebar
2. **Upload Data**: Upload a CSV or Excel file
3. **Configure Analysis**: Select analysis type and depth
4. **Generate Report**: Click "Generate Analysis Report"
5. **Review Insights**: View AI-generated insights and visualizations

### 6. Test with Sample Data

Use the provided `sample_data.csv` to test the application:
- Upload `sample_data.csv`
- Select "Sales Analysis"
- Set depth to "Detailed"
- Generate the report

---

## Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "AutoInsight AI initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Configure Secrets**
   - In Streamlit Cloud dashboard
   - Go to App Settings > Secrets
   - Add: `GEMINI_API_KEY = "your-api-key"`

### Option 2: Local Deployment

Already done! Just run:
```bash
streamlit run app.py
```

### Option 3: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t autoinsight-ai .
docker run -p 8501:8501 autoinsight-ai
```

### Option 4: Heroku Deployment

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create autoinsight-ai
   git push heroku main
   ```

---

## Project Structure

```
AutoInsight_AI/
│
├── app.py                  # Main Streamlit application
├── data_processor.py       # Data processing and analysis
├── ai_insights.py         # AI insight generation
├── visualizations.py      # Chart generation
│
├── requirements.txt       # Python dependencies
├── sample_data.csv       # Sample dataset for testing
│
├── README.md             # Project documentation
└── INSTALLATION.md       # This file
```

---

## Troubleshooting

### Issue: Module not found
**Solution**: 
```bash
pip install -r requirements.txt --upgrade
```

### Issue: API key error
**Solution**: 
- Verify API key is correct
- Check internet connection
- Ensure API key has permissions

### Issue: File upload fails
**Solution**: 
- Check file format (CSV or Excel only)
- Ensure file has headers
- Maximum file size: 200MB

### Issue: Streamlit won't start
**Solution**: 
```bash
# Clear Streamlit cache
streamlit cache clear

# Try different port
streamlit run app.py --server.port=8502
```

---

## For Academic Submission

### Files to Submit:
1. Complete source code (all .py files)
2. requirements.txt
3. Sample data files
4. README.md (project documentation)
5. Screenshots of working application
6. PPT presentation (create from README)

### Demo Preparation:
1. Run application locally before demo
2. Keep sample data ready
3. Have backup API key
4. Prepare 3-5 minute walkthrough
5. Explain the AI integration clearly

### Viva Questions to Prepare:
1. How does Generative AI work in your project?
2. What is prompt engineering?
3. How do you handle data preprocessing?
4. What algorithms detect anomalies?
5. How is this different from existing BI tools?
6. What are the limitations?
7. How would you scale this for enterprise?

---

## Additional Resources

- **Gemini API Documentation**: https://ai.google.dev/docs
- **Streamlit Documentation**: https://docs.streamlit.io
- **Plotly Charts**: https://plotly.com/python/
- **Pandas Guide**: https://pandas.pydata.org/docs/

---

## Support & Contact

For issues or questions:
- Check README.md for detailed explanations
- Review code comments
- Test with sample_data.csv first
- Ensure all dependencies are installed

**Built for B.Tech Project & Hackathons**
**MIT License - Free to use and modify**
