#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
マルチエージェントオーケストレーター
トークン効率化と最適モデル割り当てを実現
"""

import asyncio
import aiohttp
import yaml
import json
from typing import Dict, List, Any
from pathlib import Path

class MultiAgentOrchestrator:
    def __init__(self, config_path: str = "multi_agent_config.yaml"):
        self.config = self.load_config(config_path)
        self.session = None
        self.token_usage = 0
        self.total_tasks = 0

    def load_config(self, config_path: str) -> Dict:
        """設定ファイルを読み込み"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def assign_agent(self, task_type: str, complexity: str = "medium") -> Dict:
        """タスクに最適なエージェントを割り当て"""
        agent_config = self.config['agents'].get(task_type)
        if not agent_config:
            raise ValueError(f"未知のタスクタイプ: {task_type}")

        # トークン予算の計算
        base_budget = self.config['token_budget']['default_allocations'].get(task_type, 1000)
        complexity_factor = self.config['token_budget']['importance_weights'].get(complexity, 1.0)
        allocated_tokens = int(base_budget * complexity_factor)

        return {
            'agent_type': task_type,
            'model': agent_config['provider'],
            'max_tokens': allocated_tokens,
            'timeout': agent_config['timeout'],
            'temperature': agent_config['temperature']
        }

    async def execute_agent(self, agent_config: Dict, prompt: str) -> Dict:
        """エージェントを実行"""
        provider = agent_config['model']

        if provider.startswith('ollama/'):
            return await self.call_ollama(agent_config, prompt)
        elif provider.startswith('openrouter/'):
            return await self.call_openrouter(agent_config, prompt)
        elif provider == 'z_ai':
            return await self.call_z_ai(agent_config, prompt)
        else:
            # デフォルトはOpenRouter
            return await self.call_openrouter(agent_config, prompt)

    async def call_ollama(self, agent_config: Dict, prompt: str) -> Dict:
        """Ollama APIを呼び出し"""
        model_name = agent_config['model'].replace('ollama/', '')
        url = f"{self.config['providers']['ollama']['base_url']}/api/generate"

        payload = {
            "model": model_name,
            "prompt": prompt,
            "options": {
                "temperature": agent_config['temperature'],
                "num_predict": agent_config['max_tokens']
            }
        }

        try:
            async with self.session.post(url, json=payload, timeout=agent_config['timeout']) as response:
                # OllamaはNDJSON（改行区切りJSON）を返す
                content = ""
                total_tokens = 0

                async for line in response.content:
                    if line:
                        try:
                            json_line = json.loads(line.decode('utf-8'))
                            if 'response' in json_line:
                                content += json_line['response']
                            if 'eval_count' in json_line:
                                total_tokens = json_line['eval_count']
                        except json.JSONDecodeError:
                            continue

                # トークン使用量を記録
                self.token_usage += total_tokens
                self.total_tasks += 1

                return {
                    'success': True,
                    'content': content,
                    'tokens_used': total_tokens,
                    'model': agent_config['model']
                }

        except asyncio.TimeoutError:
            return {
                'success': False,
                'error': 'timeout',
                'model': agent_config['model']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': agent_config['model']
            }

    async def call_openrouter(self, agent_config: Dict, prompt: str) -> Dict:
        """OpenRouter APIを呼び出し"""
        model_name = agent_config['model'].replace('openrouter/', '')
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.config['providers']['openrouter']['api_key']}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": agent_config['max_tokens'],
            "temperature": agent_config['temperature']
        }

        try:
            async with self.session.post(url, json=payload, headers=headers,
                                       timeout=agent_config['timeout']) as response:
                result = await response.json()

                if 'error' in result:
                    return {
                        'success': False,
                        'error': result['error'],
                        'model': agent_config['model']
                    }

                # トークン使用量を記録
                tokens_used = result['usage']['total_tokens']
                self.token_usage += tokens_used
                self.total_tasks += 1

                content = result['choices'][0]['message']['content']

                return {
                    'success': True,
                    'content': content,
                    'tokens_used': tokens_used,
                    'model': agent_config['model']
                }

        except asyncio.TimeoutError:
            return {
                'success': False,
                'error': 'timeout',
                'model': agent_config['model']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': agent_config['model']
            }

    async def call_z_ai(self, agent_config: Dict, prompt: str) -> Dict:
        """Z.ai APIを呼び出し（OpenRouter経由）"""
        # Z.aiはOpenRouter経由でアクセス
        agent_config['model'] = 'openrouter/google/gemini-flash'  # フォールバック
        return await self.call_openrouter(agent_config, prompt)

    async def analyze_with_agents(self, query: str, task_type: str = "research") -> Dict:
        """マルチエージェントで分析を実行"""

        # 1. メタデータ検索（軽量）
        metadata_agent = self.assign_agent('preprocess_agent', 'low')
        metadata_result = await self.execute_agent(metadata_agent,
            f"以下のクエリに関連するメタデータを抽出: {query}")

        if not metadata_result['success']:
            return {'error': 'メタデータ検索失敗', 'details': metadata_result}

        # 2. メイン分析（タスクに応じた専門エージェント）
        main_agent = self.assign_agent(task_type, 'high')

        # メタデータをコンテキストとして追加
        context_prompt = f"""メタデータ検索結果:
{metadata_result['content']}

メインクエリ:
{query}

上記のコンテキストに基づいて分析してください。"""

        main_result = await self.execute_agent(main_agent, context_prompt)

        if not main_result['success']:
            return {'error': 'メイン分析失敗', 'details': main_result}

        # 3. 検証（品質保証）
        validation_agent = self.assign_agent('validation_agent', 'medium')
        validation_result = await self.execute_agent(validation_agent,
            f"以下の分析結果を検証してください:\n\n{main_result['content']}")

        # 4. 要約
        summary_agent = self.assign_agent('summary_agent', 'low')
        summary_result = await self.execute_agent(summary_agent,
            f"以下の内容を要約してください:\n\n{main_result['content']}")

        return {
            'success': True,
            'main_result': main_result,
            'validation': validation_result if validation_result['success'] else None,
            'summary': summary_result if summary_result['success'] else None,
            'total_tokens': self.token_usage,
            'avg_tokens_per_task': self.token_usage / self.total_tasks if self.total_tasks > 0 else 0
        }

async def main():
    """メイン実行関数"""

    print("マルチエージェントオーケストレーター起動")
    print("========================================")

    async with MultiAgentOrchestrator() as orchestrator:

        # サンプルクエリでテスト
        sample_queries = [
            ("RSI戦略の最適化パラメータを分析", "analysis"),
            ("2026年の日本株市場トレンドを調査", "research"),
            ("ボリンジャーバンドとMACDの組み合わせ戦略", "strategy"),
            ("過去5年の日経平均のボラティリティ分析", "backtest")
        ]

        for query, task_type in sample_queries:
            print(f"\n処理中: {query}")
            print(f"  タスクタイプ: {task_type}")

            result = await orchestrator.analyze_with_agents(query, task_type)

            if result['success']:
                print(f"   成功")
                print(f"   トークン使用量: {result['total_tokens']}")
                print(f"   平均トークン/タスク: {result['avg_tokens_per_task']:.1f}")

                if result['summary'] and result['summary']['success']:
                    print(f"   要約: {result['summary']['content'][:100]}...")
            else:
                print(f"   失敗: {result['error']}")

    print("\n========================================")
    print("すべての処理が完了しました")

if __name__ == "__main__":
    asyncio.run(main())