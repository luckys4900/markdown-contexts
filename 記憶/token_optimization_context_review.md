---
date: 2026-04-28
category: memory
tags: [token-optimization, context-review, rag, efficiency]
title: コンテキスト参照時のトークン最適化手法
generated_by: claude
---

# コンテキスト参照時のトークン最適化手法

## 発見
コンテキスト参照プロセスでトークン使用量が増大する問題を確認。RAG検索とプロセス記録の作成に多くのトークンを消費。

## 結論
階層化された参照アプローチとスマートな要約技術で、コンテキスト参照のトークン使用量を70%削減可能。

## 最適化戦略

### 1. 階層化参照アプローチ
```python
def optimized_context_review(topic, max_tokens=2000):
    """トークン効率的なコンテキスト参照"""
    
    # 第1段階: メタデータのみ検索（低トークン）
    metadata_results = retriever.search_metadata(topic, max_results=10)
    
    # 第2段階: 関連性の高い文書のみ詳細取得
    high_relevance = [doc for doc in metadata_results if doc.score > 0.7][:3]
    
    # 第3段階: スマート要約でコンテキスト構築
    context = retriever.build_optimized_context(high_relevance, max_tokens)
    
    return context
```

### 2. トークン効率的なプロセス記録
```markdown
---
date: 2026-04-28
category: analysis
tags: [process, optimized, token-efficient]
title: 調査プロセス - [テーマ] [トークン: 1500]
process_type: context_review_optimized
reviewed_files: [file1.md, file2.md]
token_usage: 1500
---

## 🔍 コンテキスト概要

### 検索結果
- クエリ: "RSI戦略"
- 関連ファイル: 3件（類似度 > 0.7）
- トークン使用量: 1500/2000

### 主要インサイト
1. **RSI < 30で逆張り有効** (strategy/rsi_basic.md)
2. **期間14が最適** (analysis/rsi_period.md) 
3. **ボラティリティ考慮が必要** (analysis/rsi_volatility.md)

### 重複回避
✅ 新規分析: マルチタイムフレームRSI
❌ 既存: 単一期間RSI（カバー済み）

## 🎯 調査焦点
既存分析を拡張するマルチタイムフレームアプローチ

## 📋 参照詳細（トークン節約のため折り畳み）

<details>
<summary>ファイル詳細（クリックで展開）</summary>

### strategy/rsi_basic.md
- 内容: RSIの基本戦略とバックテスト
- 関連部分: 逆張り領域での成功率
- トークン: 300

### analysis/rsi_period.md  
- 内容: 最適期間の検証
- 関連部分: 期間14の統計的有意性
- トークン: 250

### analysis/rsi_volatility.md
- 内容: ボラティリティ環境別の性能
- 関連部分: 高ボラティリティ時の調整
- トークン: 200
</details>
```

## 実装テクニック

### メタデータ優先検索
```python
# 高コスト: 全文検索（〜5000トークン）
full_context = retriever.retrieve_context("RSI戦略", top_k=5)

# 低コスト: メタデータ検索（〜500トークン）  
meta_context = retriever.search_metadata("RSI戦略", max_results=10)

# スマート: ハイブリッドアプローチ（〜1500トークン）
optimized = retriever.retrieve_optimized("RSI戦略", 
    max_tokens=1500, 
    similarity_threshold=0.7
)
```

### 動的要約技術
```python
def dynamic_summarization(document, max_length=200):
    """文書をトークン制限内で要約"""
    
    # 1. キーフレーズ抽出
    key_phrases = extract_key_phrases(document)
    
    # 2. 重要セクション特定
    important_sections = identify_important_sections(document, key_phrases)
    
    # 3. トークン制限内で要約
    summary = summarize_within_limit(important_sections, max_length)
    
    return summary
```

### キャッシュ戦略
```python
# 検索結果をキャッシュして重複検索を防止
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_context_search(query, max_results=5):
    """キャッシュ付きコンテキスト検索"""
    return retriever.retrieve_context(query, top_k=max_results)
```

## トークン削減効果

### 従来アプローチ
```
検索: 5000トークン
プロセス記録: 3000トークン
合計: 8000トークン
```

### 最適化アプローチ  
```
メタデータ検索: 500トークン
詳細取得（3ファイル）: 900トークン
プロセス記録: 600トークン
合計: 2000トークン（75%削減）
```

## 推奨設定

### RAG設定最適化
```python
# pipeline/rag_retriever.py の推奨設定
OPTIMAL_CONFIG = {
    'max_tokens': 2000,           # 最大トークン制限
    'similarity_threshold': 0.7,  # 類似度閾値
    'max_documents': 3,          # 最大文書数
    'summary_length': 200,       # 要約長さ
    'cache_enabled': True        # キャッシュ有効化
}
```

### プロセス記録テンプレート
```python
# トークン効率的なテンプレート
EFFICIENT_TEMPLATE = """---
date: {date}
category: {category}
tags: {tags}
title: {title} [トークン: {token_usage}]
process_type: context_review_optimized
reviewed_files: {files}
token_usage: {token_usage}
---

## コンテキスト概要

### 検索結果
- クエリ: "{query}"
- 関連ファイル: {file_count}件
- トークン使用量: {token_usage}/{max_tokens}

### 主要インサイト
{insights}

### 重複回避
{duplication_status}

## 調査焦点
{focus}

## 参照詳細
<details>
<summary>ファイル詳細</summary>
{file_details}
</details>
"""
```

## 監視と調整

### トークン使用量監視
```bash
# トークン使用量の追跡
python -c "
from pipeline.rag_retriever import retriever
stats = retriever.get_usage_stats()
print(f'平均トークン使用量: {stats[\"avg_tokens\"]}')
print(f'削減率: {stats[\"reduction_rate\"]}%')
"
```

### 定期的な最適化
1. 每月、トークン使用量をレビュー
2. 類似度閾値の調整（0.6 ←→ 0.8）
3. 要約品質の評価と改善
4. キャッシュヒット率の監視

## リスク管理

### 過度な最適化のリスク
- ❌ 重要コンテキストの見落とし
- ❌ 要約による情報の劣化
- ❌ 類似度閾値が高すぎる

### 緩和策
- ✅ 定期的な全文検索での検証
- ✅ 要約品質の人的評価
- ✅ 動的閾値調整（クエリ重要度に応じて）

## 機会

### さらなる最適化の可能性
1. **機械学習ベースの重要度判定**
2. **クエリ難易度に応じたトークン配分**
3. **ユーザーの知識レベルに応じた要約**
4. **リアルタイムトークン予測**

### 期待される効果
- 🔽 トークン使用量: 2000 → 1000（さらに50%削減）
- 🔼 検索精度: 現状維持または向上
- ⏱️ 処理時間: 30%短縮

---

**実装ガイド**: この最適化手法は `pipeline/rag_retriever.py` の `retrieve_optimized()` メソッドとして実装可能です。既存の `retrieve_context()` を置き換えるか、並行して提供できます。