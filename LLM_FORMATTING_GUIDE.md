# LLMフォーマット機能のセットアップ

## 概要
TXTファイルの内容をLLMを使って整形し、構造化されたMarkdownファイルとして保存する機能です。

## セットアップ手順

### 1. 依存パッケージのインストール
```bash
pip install python-dotenv requests
```

### 2. APIキーの設定

`.env.example` を `.env` にコピーし、APIキーを設定します：

```bash
copy .env.example .env
```

`.env` ファイルを編集：
```env
# z.ai coding planのAPIキー（優先）
ZAI_API_KEY=your_zai_api_key_here

# OpenRouterのAPIキー（フォールバック）
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. 使用方法

#### 方法1: LLMフォーマットを使用
```bash
run_llm_format.bat
```

この方法では：
- 最初にz.ai coding planのモデルを試す
- 失敗した場合、OpenRouterのフリーミアムモデルを試す
- それも失敗した場合、ルールベースのフォーマットにフォールバック

#### 方法2: 完全自動（既存のrun.bat）
`run.bat` は現在ルールベースのみを使用しています。

LLMフォーマットを使用するには、`run_llm_format.bat` を使用してください。

### モデルの優先順位

#### プライマリモデル（z.ai coding plan）
1. zai-coding-plan/model
2. anthropic/claude-3-haiku

#### フォールバックモデル（OpenRouter）
1. google/gemini-flash-1.5
2. meta-llama/llama-3.2-3b-instruct:free
3. meta-llama/llama-3.1-8b-instruct:free

## 使用されるモデルの確認

実行時のログでどのモデルが使用されたか確認できます：

```
[INFO] Attempting LLM formatting...
[OK] Formatted using: google/gemini-flash-1.5
```

または

```
[WARN] LLM formatting failed: ...
[INFO] Using rule-based formatting...
```

## フォーマット形式

LLMが生成するMarkdown形式：

```markdown
# タイトル

## 📊 ドキュメント情報

**作成日時**: 2026-04-28 01:00:00
**対話数**: 8 回
**トピック**: 投資戦略, 技術分析, データ分析

## 📋 実行要約

この対話では...（3〜5行の要約）

## 🔑 重要ポイント

1. スコア: 9/90 = 10%
2. RVOL≥1.2
3. ATR×0.4
...

## ✅ アクションアイテム

1. 🛑 このレポートの数値をそのまま使わない
2. ✅ 4/20 08:30時点で再生成
...

## 💡 主な洞察

- 良いデータがなければ良いモデルは作れない
- データの品質が分析結果の80%を決定する
...

## 💬 会話内容

### 1. 👤 **ユーザー**

投資戦略について教えてください

---

### 2. 🤖 **アシスタント**

投資戦略にはいくつかのアプローチがあります...

---

## 🔗 関連情報

- **投資戦略**: このトピックに関する詳細情報は上記の会話を参照
...

## 🔍 検索用キーワード

投資, 戦略, RSI, トレード, ...
```

## トラブルシューティング

### LLMフォーマットが動作しない場合

1. APIキーが正しく設定されているか確認
2. インターネット接続を確認
3. `.env` ファイルが存在するか確認

### トークン切れの場合

自動的にOpenRouterのフリーミアムモデルにフォールバックします。

### すべてのLLMモデルが失敗した場合

ルールベースのフォーマットに自動的にフォールバックします。

## コスト

- **z.ai coding plan**: 無料枠内で使用
- **OpenRouter フリーミアムモデル**: 無料
- **ルールベース**: 完全に無料

## 次のステップ

1. `.env` ファイルにAPIキーを設定
2. `受信トレイ/` にTXTファイルを保存
3. `run_llm_format.bat` を実行
4. 構造化されたMDファイルを確認
