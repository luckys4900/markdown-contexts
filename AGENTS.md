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
