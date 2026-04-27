#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析実行スクリプト
マルチエージェントシステムを使用して分析を実行
"""

import asyncio
import sys
from multi_agent_orchestrator import MultiAgentOrchestrator

async def run_analysis(query, task_type="research"):
    """分析を実行"""

    print(f"🔍 分析開始: {query}")
    print(f"  タスクタイプ: {task_type}")
    print("-" * 50)

    async with MultiAgentOrchestrator() as orchestrator:
        result = await orchestrator.analyze_with_agents(query, task_type)

        if result['success']:
            print("✅ 分析成功")
            print(f"📊 総トークン使用量: {result['total_tokens']}")
            print(f"📈 平均トークン/タスク: {result['avg_tokens_per_task']:.1f}")
            print("\n📋 要約:")
            print(result['summary']['content'] if result['summary'] else "要約なし")

            # 結果をファイルに保存
            with open(f"inbox/analysis_result_{task_type}.md", "w", encoding="utf-8") as f:
                f.write(f"# 分析結果: {query}\n\n")
                f.write(f"## 要約\n{result['summary']['content'] if result['summary'] else ''}\n\n")
                f.write(f"## 詳細結果\n{result['main_result']['content']}\n\n")
                f.write(f"## 統計\n- 総トークン使用量: {result['total_tokens']}\n")
                f.write(f"- 使用モデル: {result['main_result']['model']}\n")

            print(f"\n💾 結果を inbox/analysis_result_{task_type}.md に保存")

        else:
            print("❌ 分析失敗")
            print(f"エラー: {result['error']}")
            if 'details' in result:
                print(f"詳細: {result['details']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python run_analysis.py <クエリ> [タスクタイプ]")
        print("タスクタイプ: research, analysis, strategy, backtest")
        sys.exit(1)

    query = sys.argv[1]
    task_type = sys.argv[2] if len(sys.argv) > 2 else "research"

    asyncio.run(run_analysis(query, task_type))