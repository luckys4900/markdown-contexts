---
title: "md_output_policy"
date: "2026-04-28T08:23:18.832Z"
source: "C:\Users\ライズコーポレーション\Desktop\context\exports\md_output_policy.md"
category: "analysis"
---

# MD 出力ポリシー - 区分情報付与

## 目的
- 解析結果やシナリオ等を Markdown で保存する際に、ファイルの内容を自動的に分類できるように「区分情報」を付与する。  
- 後続の AI エージェントがファイルを読み込む際、`read` ツールで取得したテキストからカテゴリを容易に判別できる。

## 区分情報の付与ルール

### 1. YAML Front Matter (推奨)
ファイル先頭に YAML ブロックを挿入し、必須フィールドは以下:

```yaml
---
category: <区分名>   # 例: analysis, scenario, instruction, data
generated_at: "<ISO8601 timestamp>"
title: "<ファイルの概要タイトル>"
---
```

- `category` は「analysis」「scenario」「instruction」など、ファイルの主目的に応じて設定する。  
- `generated_at` はファイル生成時の日時（例: `2026-04-27T15:12:00+09:00`）。  
- `title` はユーザーが指定した場合はそのタイトル、未指定の場合はファイル名から自動生成。

### 2. プレーンテキスト形式（代替）
YAML が不要な場合は、先頭に次の行を追加:

```
# 区分: <区分名>
# 生成日時: <ISO8601 timestamp>
```

## 適用例

### 例1 – 分析フロー
```
---
category: analysis
generated_at: "2026-04-27T15:30:00+09:00"
title: "ADVANTEST（コード 6857）分析フロー"
---
# ADVANTEST（コード 6857）分析フロー
...
```

### 例2 – トレードシナリオ
```
---
category: scenario
generated_at: "2026-04-27T16:05:00+09:00"
title: "ADVANTEST 30分トレードシナリオ"
---
# ADVANTEST 30分トレードシナリオ
...
```

## 運用手順
1. **分析開始** → `webfetch` でデータ取得。  
2. **解析・シナリオ作成** → 内部で `category` を決定。  
3. **Markdown 保存** → `write` ツールで上記 YAML をヘッダーに含めた状態で保存。  
4. **後続エージェント** → `read` でファイルを取得し、`category` フィールドを基に処理を振り分ける。

このポリシーは本フォルダー内の全 Markdown 出力に自動適用されます。以後、`write` ツールで生成される Markdown は必ずこの形式で保存されます。