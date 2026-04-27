@echo off
chcp 65001 >nul
cd /d "C:\Users\user\Desktop\cursor\context\pipeline"

echo Starting Prefect server...
start cmd /k "prefect server start"

timeout /t 3 /nobreak >nul

echo.
echo Prefect server started!
echo Open http://127.0.0.1:4200 in your browser
echo.
pause
