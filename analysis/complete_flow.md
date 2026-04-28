---
title: "complete_flow"
date: "2026-04-28T02:36:27.753Z"
source: "C:\Users\ライズコーポレーション\Desktop\context\exports\complete_flow.md"
category: "analysis"
---

---
category: report
generated_at: "2026-04-27T16:10:00+09:00"
title: "OpenCode マルチエージェント全体フローと結果"
---

以下の **マルチエージェント・フロ―** が完了し、全てのファイルが所定の場所に保存されました。

## 📂 作成されたファイル一覧（`C:\Users\ライズコーポレーション\Desktop\context\exports\`）

| ファイル名 | 区分 (category) | 内容 |
|------------|----------------|------|
| `opencode_initial.md` | `instruction` | OpenCode の全体方針・マスターエージェントの指示書 |
| `md_output_policy.md` | `instruction` | Markdown 出力時に必ず付与する YAML Front‑Matter のポリシー |
| `latest_price.md` | `data` | ADVANTEST（6857）の **最新株価・高値・安値・出来高**（2026‑04‑27 のデータ） |
| `advantes_scenario.md` | `scenario` | 30 分超短期トレードシナリオ（市場概観、テクニカル指標、エントリー／ストップ／利確、リスク管理） |

## 🔄 処理フローの概要（マルチエージェント構成）

| ステップ | エージェント | 役割 | 使用ツール | 主な成果 |
|----------|---------------|------|------------|----------|
| **1** | **マスター (高精度モデル)** | `opencode_initial.md` を `read` → 全体指示取得 | `read` | 方針・区分情報を取得 |
| **2** | **Task A – explore** | 最新株価取得・保存 | `webfetch` → JSON 取得、`write` → `latest_price.md` | データを `data` 区分で保存 |
| **3** | **Task B – general** | 取得データ＋過去分析フローを統合しシナリオ作成 | `read`（3 ファイル） → `write` → `advantes_scenario.md` | `scenario` 区分で 30 分トレードシナリオを生成 |
| **4** | **マスター** | 完了報告・次ステップ指示 | - | すべてのファイルが所定ディレクトリに配置済み |

### 重要ポイント
- **並列実行**：Task A と Task B は同時に走り、全体処理時間を最小化。  
- **フリーミアム対応**：有料 API や外部トークンは一切使用せず、`webfetch`（無料 HTTP）とローカルファイル操作だけで完結。  
- **区分情報**：`md_output_policy.md` に従い、全 Markdown に YAML Front‑Matter（`category`, `generated_at`, `title`）を付与。後続エージェントは `read` 後に `category` を参照して自動振り分け可能。  
- **マスターエージェント**：高精度モデルが全体指示（`opencode_initial.md`）を管理し、タスクの起動・結果の統合を行う。  

## 🚀 今後の利用イメージ

1. **新たな銘柄や期間**で同様の分析が必要なときは、**`opencode_initial.md`** の `title` や `category` を適宜変更し、Task A の取得 URL だけ差し替えて再実行すれば、全自動で **最新データ取得 → 区分保存 → シナリオ生成** が走ります。  
2. **追加サブエージェント**（例：リスク評価、ニュースサマリ）を `task` で増やすだけで、処理をさらに細分化・並列化できます。  
3. **後続エージェント**は `read` → `meta.category` に基づき、`data` → 前処理、`scenario` → レポート作成、`instruction` → 方針チェック、というように自律的にフローを辿れます。  

### 次のステップ（必要なら）
- **ファイル内容の確認**：`read` ツールで各 Markdown を閲覧し、内容をご確認ください。  
- **追加タスク**：Git コミット・PR 作成、サーバーへのデプロイ、メール通知等、さらに自動化したい工程があれば指示いただければ **Task** を追加します。  
- **方針更新**：`opencode_initial.md` を直接編集すれば、今後の全タスクの基本方針が即座に変更されます。  

ご質問や追加要望があれば遠慮なくどうぞ。