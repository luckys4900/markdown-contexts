# Context Management System

## 概要
投資戦略の調査・分析・学習を体系的に管理するシステムです。

## ディレクトリ構造
```
context/
├── inbox/         # ★MDファイルをここに保存する
├── analysis/      # 分析・調査レポート
├── strategy/      # 戦略フレームワーク
├── memory/        # 学習・ノウハウ
├── reports/       # 定期レポート・サマリー
├── dashboard/     # マルチエージェント可視化ダッシュボード
├── logs/          # エージェントログ
├── AGENTS.md      # OpenCode用ルール
└── README.md      # このファイル
```

## 使用手順

### 1. コンテキストを保存
- `inbox/` ディレクトリにMDファイルを保存する
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
| strategy | 戦略, ストラテジー, フレームワーク, アプローチ, 方針 |
| analysis | 分析, 調査, 研究, データ, 検証, テスト |
| memory | 記憶, 学習, ノウハウ, 知見, メモ, 備忘 |
| reports | レポート, 報告, サマリー, 結論, まとめ |

## YAMLフロントマター形式
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
