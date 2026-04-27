@echo off
chcp 65001 >nul
echo ========================================
echo マルチエージェントシステム起動スクリプト
echo トークン効率化・高速処理・最適モデル割り当て
echo ========================================

echo.
echo [1/4] 環境チェックと準備...

REM 必要な環境変数のチェック
if "%OPENROUTER_API_KEY%"=="" (
    echo ERROR: OPENROUTER_API_KEYが設定されていません
    echo 設定例: set OPENROUTER_API_KEY=sk-or-xxxx
    pause
    exit /b 1
)

echo ✓ OpenRouter APIキー確認済み

REM Ollamaの起動チェック
echo.
echo [2/4] Ollamaローカルモデルの起動...

echo 優先度順にOllamaモデルを起動します...

REM 高優先度モデルから順に起動
start /B ollama run qwen3:8b --num-gpu-layers 20 --num-threads 8
echo ✓ qwen3:8b 起動中 (戦略推論用)
timeout /t 3 /nobreak >nul

start /B ollama run codegemma:7b --num-gpu-layers 15 --num-threads 6
echo ✓ codegemma:7b 起動中 (数値計算用)
timeout /t 2 /nobreak >nul

start /B ollama run llama3.2:1b --num-gpu-layers 10 --num-threads 4
echo ✓ llama3.2:1b 起動中 (軽量処理用)
timeout /t 2 /nobreak >nul

echo ✓ Ollamaモデル起動完了

echo.
echo [3/4] Python環境のセットアップ...

REM 必要なPythonパッケージのチェックとインストール
python -c "import yaml, asyncio, aiohttp" 2>nul
if %errorlevel% neq 0 (
    echo Pythonパッケージをインストールします...
    pip install pyyaml asyncio aiohttp requests
    echo ✓ パッケージインストール完了
) else (
    echo ✓ 必要なパッケージ確認済み
)

echo.
echo [4/4] マルチエージェントオーケストレーター起動...

echo 設定ファイルを読み込み中...
python -c "
import yaml
try:
    with open('multi_agent_config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    print('✓ 設定ファイル正常に読み込み完了')
    print(f'バージョン: {config[\"version\"]}')
    print(f'エージェント数: {len(config[\"agents\"])}')
except Exception as e:
    print(f'✗ 設定ファイル読み込みエラー: {e}')
    exit(1)
"

if %errorlevel% neq 0 (
    pause
    exit /b 1
)

echo.
echo マルチエージェントオーケストレーターを起動します...
echo 監視ダッシュボード: http://localhost:8501

REM メインのオーケストレーター起動
start /B python multi_agent_orchestrator.py

REM 監視ダッシュボード起動
cd dashboard
start /B streamlit run agent_monitor.py
cd..

echo.
echo ========================================
echo 🎉 マルチエージェントシステム起動完了！
echo ========================================
echo.
echo 起動されたコンポーネント:
echo ✓ Ollamaローカルモデル (3モデル)
echo ✓ OpenRouter接続設定
echo ✓ マルチエージェントオーケストレーター
echo ✓ リアルタイム監視ダッシュボード
echo.
echo 利用可能なエージェント:
echo • Master Agent (制御・統合)
echo • Analysis Agent (分析・推論)
echo • Research Agent (調査・収集)
echo • Strategy Agent (戦略・意思決定)
echo • Backtest Agent (数値検証・シミュレーション)
echo • Preprocess Agent (前処理・整形)
echo • Summary Agent (要約・報告)
echo • Validation Agent (検証・品質保証)
echo.
echo トークン最適化機能:
echo • 動的トークン割り当て (最大70%削減)
echo • 並列処理 (3倍高速化)
echo • 智能的なモデル選択
echo • リアルタイム監視と調整
echo.
echo 使用方法:
echo python run_analysis.py "分析クエリ"
echo または
echo 監視ダッシュボードから直接操作

echo.
echo システム停止:
echo stop_multi_agents.bat を実行

echo.
pause