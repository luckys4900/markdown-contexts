@echo off
chcp 65001 >nul
echo ========================================
echo マルチエージェントシステム停止スクリプト
echo ========================================

echo.
echo [1/3] Ollamaプロセスの停止...

taskkill /f /im ollama.exe 2>nul
if %errorlevel% equ 0 (
    echo ✓ Ollamaプロセス停止完了
) else (
    echo ℹ Ollamaプロセスは実行中ではありません
)

echo.
echo [2/3] Pythonオーケストレーターの停止...

taskkill /f /im python.exe 2>nul
if %errorlevel% equ 0 (
    echo ✓ Pythonプロセス停止完了
) else (
    echo ℹ Pythonプロセスは実行中ではありません
)

echo.
echo [3/3] Streamlitダッシュボードの停止...

taskkill /f /im streamlit.exe 2>nul
if %errorlevel% equ 0 (
    echo ✓ Streamlitダッシュボード停止完了
) else (
    echo ℹ Streamlitダッシュボードは実行中ではありません
)

echo.
echo ========================================
echo ✅ マルチエージェントシステム完全停止
echo ========================================
echo.
echo すべてのコンポーネントが正常に停止されました
echo.
pause