# Context Management System - OpenCode Rules

## 基本ルール
- 作業開始時は必ず `README.md` を読み、コンテキスト管理のルールを理解すること
- 新しい分析・調査を行う際は、既存のコンテキストを参照し、重複を避けること
- このシステムは投資戦略の調査・分析・学習を目的とする

## コンテキスト収集フロー

### Step 1: 作業開始
1. `inbox/` ディレクトリにMDファイルを保存
2. `context_organizer.py` を実行し、自動振り分け
3. YAMLフロントマターが自動付与される

### Step 2: 分析プロセス
1. 既存コンテキストを検索・参照（`analysis/`, `strategy/`, `memory/`）
2. 新しい洞察・分析結果を `inbox/` に保存
3. 自動振り分けで適切なカテゴリへ整理

### Step 3: 精度向上
1. 思考ベクトルの策定: `strategy/` に戦略フレームワークを保存
2. 情報参照: 過去のレポートからパターンを抽出
3. レポート作成: 学習した内容を `reports/` にまとめる

## YAMLフロントマター構造
```yaml
---
date: YYYY-MM-DD
category: analysis|strategy|memory|reports
tags: [keyword1, keyword2, ...]
title: タイトル
---
```

## 振り分けルール（自動）
- `strategy/`: 戦略、ストラテジー、フレームワーク、アプローチ
- `analysis/`: 分析、調査、研究、データ
- `memory/`: 記憶、学習、ノウハウ、知見
- `reports/`: レポート、報告、サマリー、結論

## Git同期
- 作業完了後は `context_sync.bat` を実行し、GitHubへpushすること
- 自動で振り分け・コミット・プッシュが行われる

## マルチエージェント運用ルール

### エージェント構成
- **Master Agent**: 高機能モデル、タスク調整・結果統合
- **Collector Agent**: フリーミアム、ファイル収集・監視
- **Organizer Agent**: フリーミアム、YAML付与・分類
- **Analyzer Agent**: フリーミアム、内容分析・重複排除
- **Reporter Agent**: フリーミアム、レポート生成・Git操作

### トークン削減原則
- Master Agentは指示・結果のみを扱う
- 詳細コンテキストはスレーブエージェントで処理
- 並列処理で処理時間を短縮
- ファイル内容はMasterへ送信しない

### 並列処理手順
1. Collectorがinboxを並列スキャン
2. Organizerが並列でYAML付与・分類
3. Analyzerが並列で分析・重複チェック
4. ReporterがGit操作を実行
5. Masterが結果を統合・報告

### 詳細設計
詳細は `memory/multi_agent_architecture.md` を参照

## マルチエージェント可視化ルール

### ダッシュボード起動
```bash
cd context/dashboard
pip install -r requirements.txt
streamlit run app.py
```

### GitHub Pagesへのデプロイ
- ダッシュボードはGitHub Pagesでホスティング
- コードpush時に自動デプロイ（GitHub Actions）
- URL: `https://[username].github.io/[repo]/context/dashboard/`

### 可視化機能
1. **フロー可視化**: エージェント間の依存関係をツリー表示
2. **トークン使用量**: Master vs Slavesの比較グラフ
3. **ステータスタイムライン**: リアルタイムのエージェント状態
4. **ログ表示**: 各エージェントの処理ログ

### エージェントログ出力
各エージェントは処理進捗を `logs/agent_[id].json` に出力
```json
{
  "agent_id": "master",
  "agent_name": "Master Agent",
  "status": "running",
  "task": "Orchestrating tasks",
  "message": "Task assigned to Research Agent",
  "tokens_used": 150,
  "timestamp": "2026-04-27T20:30:00"
}
```

### 詳細設計
- ダッシュボード: `dashboard/app.py`
- 監視モジュール: `dashboard/agent_monitor.py`
- 視覚化モジュール: `dashboard/visualizer.py`
- デプロイ設定: `.github/workflows/deploy-dashboard.yml`

## RAG（ベクトル検索）ルール

### 基本原則
- **分析・調査開始時にRAGで既存コンテキストを参照**
- **ベクトル検索で最も関連性の高い文書を自動抽出**
- **トークン使用量を制限し、Master Agentへの負荷を軽減**

### RAG検索フロー
1. クエリをEmbeddingモデルでベクトル化
2. Vector DB（Chroma）で類似度検索
3. トークン制限に合わせて文書を切り詰め
4. Master Agentへ最適化されたコンテキストを提供

### 使用方法
```python
from pipeline.rag_retriever import retriever

# コンテキスト検索
context_data = retriever.retrieve_context(
    query="RSI戦略の最適化",
    top_k=5,
    category="strategy"
)

# コンテキストプロンプト生成
prompt = retriever.build_context_prompt(
    query="RSI戦略の最適化",
    max_context_docs=3
)
```

### トークン最適化
- `max_tokens` パラメータで使用トークンを制限（デフォルト: 8000）
- 関連性スコア（similarity）でフィルタリング（デフォルト: 0.3以上）
- 重要度順に文書を切り出し、効率的にコンテキストを構築

## MCP（Model Context Protocol）ルール

### 基本原則
- **外部データベース・エージェント間連携・ストレージ連携をMCPで実現**
- **通信履歴をSQLiteで永続化**
- **キャッシュ機構で重複検索を回避**

### MCP連携機能
1. **エージェント通信**: エージェント間のメッセージ送受信
2. **コンテキストキャッシュ**: 検索結果をキャッシュし再利用
3. **インサイト保存**: 分析結果の洞察をデータベースに保存
4. **ストレージ連携**: S3/MinIOとの連携

### 使用方法
```python
from pipeline.mcp_connector import connector

# エージェント登録
connector.register_agent(
    agent_id="analyzer_1",
    agent_name="Analyzer Agent",
    capabilities=["analysis", "pattern_detection"]
)

# メッセージ送信
connector.send_message(
    from_agent="analyzer_1",
    to_agent="master",
    message_type="analysis_complete",
    payload={"result": "..."}
)

# インサイト保存
connector.store_insight(
    insight_type="pattern",
    content="RSI < 30で逆張りが有効",
    source_file="strategy/rsi_analysis.md",
    tags=["pattern", "rsi"]
)
```

## 自動記憶パイプライン

### 基本原則
- **分析完了後に洞察を自動抽出**
- **YAMLフロントマターを自動生成**
- **memory/ディレクトリへ自動保存**
- **MCPコネクタでデータベースに永続化**

### 自動記憶フロー
1. 分析結果から洞察を抽出（パターン認識）
2. YAMLフロントマターを自動生成
3. memory/ディレクトリにMDファイルとして保存
4. MCPコネクタでSQLiteにインサイトを保存
5. Vector DBにインデックス追加

### 抽出される洞察タイプ
- `finding`: 発見事項
- `conclusion`: 結論
- `recommendation`: 推奨事項
- `pattern`: パターン・傾向
- `risk`: リスク・懸念
- `opportunity`: 機会・可能性

## Prefectワークフロー

### 基本原則
- **分析プロセスをワークフローとして定義**
- **タスクの依存関係を自動管理**
- **エラーハンドリング・再試行を実装**

### ワークフロー一覧
1. **context_analysis_flow**: 単一クエリの分析
2. **batch_analysis_flow**: 複数クエリのバッチ処理
3. **index_rebuild_flow**: Vector DBの再構築

### 使用方法
```bash
# Prefectサーバー起動
prefect server start

# 分析フロー実行
cd pipeline
python prefect_flows.py "RSI戦略の最適化"
```

### 詳細設計
- RAGモジュール: `pipeline/rag_retriever.py`
- Embeddingストア: `pipeline/embedding_store.py`
- MCPコネクタ: `pipeline/mcp_connector.py`
- 自動記憶: `pipeline/auto_memory.py`
- Prefectフロー: `pipeline/prefect_flows.py`
