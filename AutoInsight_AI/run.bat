@echo off
title AutoInsight AI - Starting...
echo.
echo  ============================================
echo    AutoInsight AI - BI Report Generator
echo  ============================================
echo.
echo  Starting the application...
echo  Browser will open at: http://localhost:8501
echo.
cd /d "%~dp0"
streamlit run app.py
pause
