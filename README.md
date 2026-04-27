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
- `受信トレイ/` ディレクトリにファイルを保存する
- **MDファイル**: 直接保存可能
- **TXTファイル**: LLMのやり取りをそのまま保存可能（自動でMD変換）
- ファイル名は英語推奨（例: `rsi_analysis_20260427.md`）
- 内容に沿って自動で振り分けられるため、カテゴリ指定は不要

### 2. 自動振り分け
以下のコマンドを実行：
```bash
python context_organizer.py
```
または
```bash
run.bat
```

**自動処理内容**:
- TXTファイル → MDファイルへ変換（LLMのやり取りを構造化）
- YAMLフロントマターが自動付与（階層化・わかりやすい）
- キーワードベースで適切なカテゴリへ振り分け
- TXTファイルは自動削除

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

## TXTファイル処理

### TXTファイルの保存
`受信トレイ/` にLLMのやり取りをTXT形式で保存します。

### サンプルTXTファイル
```
User: 投資戦略について教えてください

Assistant: 投資戦略にはいくつかのアプローチがあります...
```

### 自動変換機能

#### 方法1: LLMフォーマットを使用（推奨）
LLMを使って高度な整形を行います：

```bash
run_llm_format.bat
```

**LLMフォーマットの特徴**:
- **z.ai coding plan** または **OpenRouterのフリーミアムモデル** を使用
- 高度な要約・抽出・構造化
- 重要ポイント、アクションアイテム、洞察の自動抽出
- トークン切れ時は自動フォールバック

**モデルの優先順位**:
1. z.ai coding planのモデル
2. OpenRouterのフリーミアムモデル（Gemini Flash, Llama 3.1/3.2）
3. ルールベースフォーマット

**詳細なセットアップ手順**: [LLM_FORMATTING_GUIDE.md](LLM_FORMATTING_GUIDE.md)

#### 方法2: ルールベースフォーマット
ルールベースで自動処理されます：

```bash
run.bat
```

**処理内容**:
1. **LLMのやり取りを解析**: ユーザーとアシスタントのメッセージを抽出
2. **構造化**: Markdown形式に変換
3. **タイトル自動生成**: 最初の質問からタイトルを生成
4. **トピック自動抽出**: 投資戦略、技術分析、AI/ML など
5. **洞察自動抽出**: 発見、結論、推奨事項などを抽出
6. **YAMLフロントマター付与**: 階層化されたメタ情報
7. **自動振り分け**: キーワードベースで適切なカテゴリへ
8. **TXTファイル削除**: 変換後、元のTXTファイルは削除

### 変換後のMDファイル例（LLMフォーマット）
```markdown
# 投資戦略について教えてください

## 📊 ドキュメント情報

**作成日時**: 2026-04-28 01:00:00
**対話数**: 8 回
**トピック**: 投資戦略, 技術分析, データ分析

## 📋 実行要約

この対話では投資戦略の主要なアプローチについて議論しました。
バリュー投資、成長投資、トレンド追従、逆張りの4つの方針を比較検討し、
それぞれの特徴と適用シーンについて明確にしました。

## 🔑 重要ポイント

1. バリュー投資: 割安な株を探す
2. 成長投資: 成長性の高い株に投資
3. トレンド追従: トレンドに乗る
4. 逆張り: トレンドの逆を行く

## ✅ アクションアイテム

1. 投資スタイルとリスク許容度を明確にする
2. 適切な戦略を選択する
3. データの品質チェックを徹底する

## 💡 主な洞察

- 長期投資ならバリュー投資が適している
- 短期投資ならトレンド追従が有効
- ボラティリティの高い相場では逆張りがチャンスになる

## 💬 会話内容

### 1. 👤 **ユーザー**

投資戦略について教えてください

---

### 2. 🤖 **アシスタント**

投資戦略にはいくつかのアプローチがあります。主なものは以下の通りです：

1. バリュー投資: 割安な株を探す
2. 成長投資: 成長性の高い株に投資
3. トレンド追従: トレンドに乗る
4. 逆張り: トレンドの逆を行く

---

## 🔗 関連情報

- **投資戦略**: このトピックに関する詳細情報は上記の会話を参照

## 🔍 検索用キーワード

投資, 戦略, バリュー, 成長, トレンド, 逆張り, リスク管理
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
