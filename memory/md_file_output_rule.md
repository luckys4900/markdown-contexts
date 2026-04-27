---
date: 2026-04-28
category: memory
tags: [rule, file-output, inbox, workflow]
title: MDファイル出力ルール
generated_by: opencode
---

# MDファイル出力ルール

## 発見
MDファイルを直接カテゴリフォルダ（reports/、strategy/等）に出力すると、自動振り分けがスキップされ、YAMLフロントマターが付与されない。

## 結論
すべてのMDファイルは必ず `inbox/` フォルダに出力し、その後 `run.bat` を実行して自動振り分けさせる。

## ルール

### 基本ルール
**すべてのMDファイルは `inbox/` フォルダに出力すること**

### 出力先フォルダ
- ✅ 正しい出力先: `context/inbox/`
- ❌ 誤った出力先: `context/reports/`, `context/strategy/`, `context/analysis/` 等

### ワークフロー
```
1. MDファイル作成 → inbox/ に保存
2. run.bat 実行
   - 自動振り分け
   - YAMLフロントマター付与
   - Vector DB更新
   - Git push
3. 適切なカテゴリへ移動完了
```

### 推奨事項
- 分析レポート、戦略ドキュメント、メモ等、すべてのMDファイルをinbox/に出力
- OpenCodeでファイルを作成する際は、常に `context/inbox/` を指定
- 手動でカテゴリフォルダに保存しない

## パターン
正しいパターン:
```
OpenCode → inbox/ に保存 → run.bat → 自動振り分け → 完了
```

誤ったパターン:
```
OpenCode → reports/ に保存 → 自動振り分けスキップ → YAMLなし → 不完全
```

## リスク
inbox/以外に保存した場合のリスク:
- ❌ YAMLフロントマターが付与されない
- ❌ Vector DBが更新されない
- ❌ RAG検索で見つからない
- ❌ 自動記憶パイプラインが機能しない

## 機会
このルールを守ることで:
- ✅ 100%のファイルが自動処理される
- ✅ すべてのファイルが検索可能になる
- ✅ 自動記憶パイプラインが完全に機能する

## 記憶すべきポイント
1. **inbox/ が唯一の出力先**
2. **run.bat が唯一の実行コマンド**
3. **自動化が完了するまで待つ**

---

**重要**: このルールはOpenCodeの全プロジェクトで適用する
