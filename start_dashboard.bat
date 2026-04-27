@echo off
chcp 65001 >nul
cd /d "C:\Users\user\Desktop\cursor\context\dashboard"

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting dashboard...
streamlit run app.py

pause
