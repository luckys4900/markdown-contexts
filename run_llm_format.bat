@echo off
chcp 65001 >nul
cd /d "C:\Users\user\Desktop\cursor\context"

echo Loading environment variables...
if exist .env (
    for /f "tokens=*" %%a in ('type .env ^| findstr /v "^#"') do set %%a
    echo Environment variables loaded.
) else (
    echo WARNING: .env file not found. Please copy .env.example to .env and add your API keys.
    echo Using rule-based formatting only.
)

echo.
echo ================================================================================
echo                    Context Management System
echo ================================================================================
echo.

REM Pythonスクリプトを実行
python context_organizer.py

echo.
echo ================================================================================
echo                           All Steps Completed!
echo ================================================================================
echo.
pause
