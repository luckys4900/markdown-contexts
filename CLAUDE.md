# Context Management System - CLAUDE Rules

## 基本原則
- **作業開始時は必ずコンテキスト参照プロセスを実行すること**
- **既存の分析・調査を重複させないこと**
- **OpenCodeの自動化ワークフローを尊重すること**

## コンテキスト参照フロー

### Step 1: 調査前のコンテキスト確認（トークン最適化版）
```bash
# 1. 既存コンテキストの検索（トークン最適化RAGを使用）
python -c "from pipeline.rag_retriever import retriever; print(retriever.retrieve_optimized('調査テーマ', max_tokens=1500, similarity_threshold=0.7))"

# 2. 関連ファイルのメタデータ確認（低トークン）
python -c "from pipeline.rag_retriever import retriever; print(retriever.search_metadata('調査テーマ', max_results=8))"

# 3. キーワード検索（ファイルパスのみ）
rg "キーワード" context/ --type=md -l | head -5
```

### Step 2: プロセス内容の記録（トークン最適化版）
すべての調査・分析プロセスは `inbox/` にMDファイルとして保存（トークン効率的な形式）：
```markdown
---
date: YYYY-MM-DD
category: analysis|strategy|memory|reports
tags: [keyword1, keyword2, topic, token-optimized]
title: 調査プロセス - [テーマ名] [トークン: XXXX]
process_type: context_review_optimized|analysis|strategy_development
reviewed_files: [file1.md, file2.md]
token_usage: XXXX
---

## 調査プロセス記録

### 調査開始前のコンテキスト確認
- 検索クエリ: "調査テーマ"
- 検索結果: X件の関連ファイルを発見
- 主要な既存コンテキスト:
  - `strategy/rsi_analysis.md`: RSI戦略の基本分析
  - `analysis/market_trend_2026.md`: 市場トレンド分析

### 調査目的
[調査の目的と期待される成果を記載]

### 参照した既存コンテキスト
1. **ファイル**: `strategy/rsi_analysis.md`
   - 内容: RSIの基本戦略とバックテスト結果
   - 関連性: 高
   - 活用方法: 基本戦略をベースに拡張

2. **ファイル**: `analysis/market_trend_2026.md`
   - 内容: 2026年の市場環境分析
   - 関連性: 中
   - 活用方法: マクロ環境の考慮

### 新規分析の追加価値
[既存コンテキストに対する新規分析の追加価値を明確化]

### 次回調査時の参照ポイント
[この調査が将来の調査で参照すべきポイント]
```

### Step 3: 自動処理の実行
```bash
# inbox/に保存後、自動処理を実行
run.bat

# または個別実行
python context_organizer.py
```

## 禁止事項

### コンテキスト無視の禁止
- ❌ 既存の分析を無視して新規分析を開始しない
- ❌ 重複する調査を実施しない
- ❌ 参照プロセスをスキップしない

### ファイル出力の禁止
- ❌ `inbox/` 以外のディレクトリに直接ファイルを保存しない
- ❌ 手動でYAMLフロントマターを編集しない
- ❌ 手動でファイルを移動しない

## 推奨ワークフロー

### トークン最適化調査フロー
```python
# トークン効率的な調査開始スクリプト例
from pipeline.rag_retriever import retriever
from pathlib import Path
import datetime

def start_optimized_investigation(topic, max_tokens=1500):
    # 1. 既存コンテキスト検索（トークン最適化版）
    context = retriever.retrieve_optimized(topic, 
        max_tokens=max_tokens, 
        similarity_threshold=0.7,
        max_documents=3
    )
    
    # 2. トークン効率的なプロセス記録作成
    process_content = f'''---
date: {datetime.date.today()}
category: analysis
tags: [process, investigation, {topic.lower()}, token-optimized]
title: 調査プロセス - {topic} [トークン: {context['token_usage']}]
process_type: context_review_optimized
reviewed_files: {[doc['file'] for doc in context['documents']]}
token_usage: {context['token_usage']}
---

## 🔍 コンテキスト概要

### 検索結果
- クエリ: "{topic}"
- 関連ファイル: {context['num_documents']}件（類似度 > 0.7）
- トークン使用量: {context['token_usage']}/{max_tokens}

### 主要インサイト
'''
    
    for i, doc in enumerate(context['documents'], 1):
        process_content += f"{i}. **{doc['key_insight']}** ({doc['file']})\n"
    
    process_content += f'''
### 重複回避
✅ 新規分析: {topic}の新規側面
❌ 既存: 既存分析でカバー済みの内容

## 🎯 調査焦点
既存分析を拡張する新規アプローチ

## 📋 参照詳細（トークン節約のため折り畳み）

<details>
<summary>ファイル詳細（クリックで展開）</summary>
'''
    
    for doc in context['documents']:
        process_content += f"### {doc['file']}\n- 内容: {doc['summary'][:80]}...\n- トークン: {doc['token_count']}\n\n"
    
    process_content += "</details>\n"
    
    # 3. inbox/に保存
    filename = f"inbox/investigation_process_optimized_{topic.lower()}_{datetime.date.today()}.md"
    Path(filename).write_text(process_content, encoding='utf-8')
    
    return context
```

### 自動化推奨設定
```bash
# .claude/settings.json に追加（オプション）
{
  "before": {
    "task": [
      {
        "command": "python -c \"from pipeline.rag_retriever import retriever; retriever.retrieve_context('{user_input}', top_k=3)\"",
        "description": "Search existing context before starting task"
      }
    ]
  }
}
```

## 違反時の影響

### コンテキスト無視の影響
- ❌ 分析の重複発生
- ❌ 時間とリソースの浪費
- ❌ 一貫性のない結論

### ワークフロー違反の影響
- ❌ YAMLフロントマター欠如
- ❌ Vector DB未更新
- ❌ 検索不可能
- ❌ 自動記憶パイプライン機能不全

## 例外処理

### 緊急調査の場合
緊急で即時の分析が必要な場合：
1. 最小限のコンテキスト確認のみ実施
2. 分析完了後、必ずプロセス記録を `inbox/` に保存
3. `run.bat` を実行して正式な処理を完了

### 技術的問題の場合
RAGシステムが利用できない場合：
1. 手動でキーワード検索を実施
2. 検索結果をプロセス記録に明記
3. 通常通り `inbox/` に保存

## 品質基準

### 優れたプロセス記録
- ✅ 検索クエリが明確
- ✅ 参照ファイルが具体的に記載
- ✅ 既存コンテキストとの関係性が説明されている
- ✅ 新規分析の追加価値が明確
- ✅ 将来の参照ポイントが記載されている

### 不十分なプロセス記録
- ❌ 検索クエリが不明確
- ❌ 参照ファイルの記載なし
- ❌ 既存コンテキストとの関係性不明
- ❌ 追加価値の説明なし
- ❌ 将来の参照ポイントなし

## 監査と改善

### 定期的な監査
```bash
# プロセス記録の品質チェック
rg "process_type:" context/ --type=md | grep -v "reviewed_files" | wc -l

# コンテキスト参照の効果測定
python -c "
from pipeline.rag_retriever import retriever
result = retriever.retrieve_context('investment strategy', top_k=10)
print(f'重複回避率: {result['duplication_prevention_rate']}%')
"
```

### 継続的改善
1. 每月、プロセス記録をレビュー
2. 効果的な検索クエリを共有
3. 参照パターンを分析し最適化
4. RAGシステムの精度向上

---

## トークン最適化に関する追加ガイドライン

### トークン削減の原則
1. **メタデータ優先**: 全文検索の前にメタデータ検索を実施
2. **類似度フィルタリング**: 類似度0.7未満の文書は除外
3. **文書数制限**: 最大3文書までに制限
4. **動的要約**: トークン制限内で智能的要約
5. **キャッシュ活用**: 同一クエリの重複検索を防止

### 期待される効果
- 🔽 トークン使用量: 8000 → 2000（75%削減）
- 🔼 検索精度: 類似度閾値でフィルタリングにより向上
- ⏱️ 処理時間: キャッシュにより50%短縮

### 詳細な最適化手法
詳細は `記憶/token_optimization_context_review.md` を参照してください。

**重要**: このルールはすべての調査・分析作業で適用されます。コンテキスト参照プロセスを省略すると、重複作業や矛盾した結論が発生するリスクがあります。

**トークン最適化の重要性**: コンテキスト参照は必須ですが、適切な最適化によりトークン使用量を大幅に削減しながら、検索品質を維持できます。