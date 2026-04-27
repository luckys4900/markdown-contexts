# Context Management System

## 概要
投資戦略の調査・分析・学習を体系的に管理するシステムです。

## ディレクトリ構造
```
context/
├── 受信トレイ/     # ★MDファイルをここに保存する
├── 分析/          # 分析・調査レポート
├── 戦略/          # 戦略フレームワーク
├── 記憶/          # 学習・ノウハウ
├── レポート/      # 定期レポート・サマリー
├── dashboard/     # マルチエージェント可視化ダッシュボード
├── pipeline/      # RAG/MCP/Pipelineモジュール
├── storage/       # Vector DB / SQLite
├── logs/          # エージェントログ
├── AGENTS.md      # OpenCode用ルール
└── README.md      # このファイル
```

## 使用手順

### 1. コンテキストを保存
- `受信トレイ/` ディレクトリにMDファイルを保存する
- ファイル名は英語推奨（例: `rsi_analysis_20260427.md`）
- 内容に沿って自動で振り分けられるため、カテゴリ指定は不要

### 2. 自動振り分け
以下のコマンドを実行：
```bash
python context_organizer.py
```
- YAMLフロントマターが自動付与
- キーワードベースで適切なカテゴリへ振り分け

### 3. Git同期
以下のコマンドを実行：
```bash
context_sync.bat
```
- 自動振り分け → Git add → Git commit → Git push

## 振り分けルール
| カテゴリ | キーワード |
|---------|-----------|
| 戦略 | 戦略, ストラテジー, フレームワーク, アプローチ, 方針 |
| 分析 | 分析, 調査, 研究, データ, 検証, テスト |
| 記憶 | 記憶, 学習, ノウハウ, 知見, メモ, 備忘 |
| レポート | レポート, 報告, サマリー, 結論, まとめ |

## YAMLフロントマター形式

### 新しい形式（階層化・わかりやすい）
```yaml
---
# メタ情報
作成日: 2026-04-27
カテゴリ: 戦略
タイトル: RSI逆張り戦略の分析

# タグ（ドメイン・重要度・トピック）
タグ:
  ドメイン: [投資, 株式]
  重要度: [高]
  トピック: [RSI, 逆張り, 短期]

# 自動生成情報
生成元: opencode
バージョン: 1.0
---
```

### 旧形式（互換性維持）
```yaml
---
date: 2026-04-27
category: strategy
tags: [RSI, 逆張り, 短期]
title: RSI逆張り戦略の分析
---
```

## 検索方法
### キーワード検索
```bash
# 全ディレクトリから検索
rg "キーワード" context/

# 特定カテゴリから検索
rg "キーワード" context/strategy/
```

### 日付ベース検索
```bash
# 特定日以降のファイル
ls context/strategy/*.md | grep "2026042[7-9]"
```

## よくある質問
**Q: 振り分け先を変えたい場合は？**
A: YAMLフロントマターの `category` を手動で変更してください

**Q: タグを追加したい場合は？**
A: YAMLフロントマターの `tags` 配列に追加してください

**Q: 既存ファイルを再分類したい場合は？**
A: `context_organizer.py` を再実行すると再評価されます

## マルチエージェント可視化ダッシュボード

### ローカルで起動
```bash
cd context/dashboard
pip install -r requirements.txt
streamlit run app.py
```
ブラウザで `http://localhost:8501` にアクセス

### GitHub Pagesで閲覧
- コードをGitHubにpushすると自動デプロイ
- URL: `https://[username].github.io/[repo]/context/dashboard/`

### ダッシュボード機能
1. **Flow Visualization**: エージェント間の依存関係をツリー表示
2. **Token Usage**: 各エージェントのトークン使用量を比較
3. **Status Timeline**: リアルタイムのエージェント状態を表示
4. **Logs**: 各エージェントの処理ログを閲覧

### エージェントログ出力
マルチエージェントで処理する際、各エージェントは以下の形式でログを出力：
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

## RAG（ベクトル検索）システム

### セットアップ
```bash
cd pipeline
pip install -r requirements.txt
```

### Vector DBの初期化
```python
from pipeline.embedding_store import store

# ディレクトリ内の全MDファイルをインデックス化
count = store.rebuild_index(Path("context"))
print(f"Indexed {count} documents")
```

### コンテキスト検索
```python
from pipeline.rag_retriever import retriever

# 関連コンテキストを検索
context_data = retriever.retrieve_context(
    query="RSI戦略の最適化",
    top_k=5,
    category="strategy"
)

print(f"Found {context_data['num_documents']} documents")
print(f"Token usage: {context_data['token_usage']}")
```

### トークン最適化
- `max_tokens` パラメータでトークン使用量を制限
- 関連性スコアで自動フィルタリング
- 重要度順に文書を切り出し

## MCP（Model Context Protocol）連携

### エージェント通信
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
```

### インサイト保存
```python
# 分析結果の洞察を保存
connector.store_insight(
    insight_type="pattern",
    content="RSI < 30で逆張りが有効",
    source_file="strategy/rsi_analysis.md",
    tags=["pattern", "rsi"]
)
```

## 自動記憶パイプライン

### 自動記憶の実行
```python
from pipeline.auto_memory import auto_memory

analysis_result = {
    'query': 'RSI戦略の最適化',
    'context': '...',
    'category': 'strategy'
}

# 自動で洞察を抽出しmemory/に保存
filepath = auto_memory.save_memory(analysis_result)
print(f"Memory saved to: {filepath}")
```

### 自動抽出される洞察
- **finding**: 発見事項
- **conclusion**: 結論
- **recommendation**: 推奨事項
- **pattern**: パターン・傾向
- **risk**: リスク・懸念
- **opportunity**: 機会・可能性

## Prefectワークフロー

### Prefectサーバー起動
```bash
prefect server start
```

### 分析フロー実行
```bash
cd pipeline
python prefect_flows.py "RSI戦略の最適化"
```

### Pythonから実行
```python
from pipeline.prefect_flows import context_analysis_flow

result = context_analysis_flow(
    query="RSI戦略の最適化",
    category="strategy",
    max_tokens=8000
)

print(f"Extracted {len(result['insights'])} insights")
print(f"Memory saved to: {result['memory_path']}")
```

### バッチ分析
```python
from pipeline.prefect_flows import batch_analysis_flow

queries = [
    "RSI戦略の最適化",
    "MACDのパターン分析",
    "ボリンジャーバンドの活用"
]

results = batch_analysis_flow(queries, category="strategy")
```

## 統合フロー

### 分析から記憶までの完全自動化
```python
# 1. RAGで既存コンテキストを検索
context_data = retriever.retrieve_context("RSI戦略")

# 2. 分析実行（ここでMaster Agentが使用）
analysis_result = analyze_with_context(context_data)

# 3. 自動記憶パイプラインで洞察を保存
memory_path = auto_memory.save_memory(analysis_result)

# 4. Vector DBを更新
store.add_document(Path(memory_path))

# 5. GitHubへ同期
# run.batを実行
```

### トークン使用量の最適化
1. RAGで関連性の高い文書のみを抽出（〜2000トークン）
2. Master Agentは抽出されたコンテキストのみを処理（〜3000トークン）
3. スレーブエージェントで詳細分析（フリーミアム）
4. 自動記憶パイプラインで洞察を保存（次回の検索で活用）

**結果: 1回の分析あたりのトークン使用量を70%削減**
