---
title: "opencode_initial"
date: "2026-04-27T09:10:23.261Z"
source: "C:\Users\ライズコーポレーション\Desktop\context\exports\opencode_initial.md"
category: "tools"
---

---
category: instruction
generated_at: "2026-04-27T15:45:00+09:00"
title: "OpenCode 初期指示書"
---

# OpenCode 初期指示書

## 目的
- 本ファイルは **OpenCode が最初に実行すべき手順と全体方針** を定義します。
- 以後のすべてのユーザー要求は、処理開始前に必ずこのファイルを読み取り、指示に従います。

## 全体アーキテクチャ
1. **マスターエージェント**（現在の高精度モデル）
   - `opencode_initial.md` を `read` し、全体方針・区分情報を取得。
   - 必要に応じて **`task`** ツールでサブエージェントを並列起動。
2. **サブエージェントの役割**
   - `explore`（軽量・高速）: データ取得、簡易加工、ファイル書き込み。
   - `general`（高精度）: 詳細分析、シナリオ作成、コード生成。
3. **出力ポリシー**
   - すべての Markdown は `md_output_policy.md` に定義された **YAML Front‑Matter**（`category`, `generated_at`, `title`）を必ず付与。
   - `category` により後続エージェントが自動的に内容を振り分け可能。

## 実装フロー（マスタ―エージェント側）
1. `read` → `opencode_initial.md`（取得）
2. `task`（並列）
   - **Task A**（`explore`）: 最新株価取得 → `latest_price.md` 作成
   - **Task B**（`general`）: 取得済みデータと過去分析フローを統合 → `advantes_scenario.md` 作成
3. 必要に応じて **Git** 操作や **PR 作成** を追加タスクで実行。

## 更新方法
- 任意のテキストエディタで `opencode_initial.md` を直接編集してください。
- 編集後は次回のリクエストから自動的に新しい指示が反映されます。

## 注意点
- 本フローは **フリーミアム / 無料トークン** のみで完結します。外部有料 API は使用しません。
- `explore` サブエージェントは高速取得に特化し、`general` は高精度分析に特化します。
- すべてのファイルは `C:\Users\ライズコーポレーション\Desktop\context\exports\` に保存されます。

---
