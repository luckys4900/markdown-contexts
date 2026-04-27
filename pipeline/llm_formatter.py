import os
import requests
from typing import Optional, Dict, Any
import json

class LLMFormatter:
    def __init__(self):
        self.primary_api_key = os.getenv("ZAI_API_KEY", "")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        # モデル設定
        self.primary_models = [
            "zai-coding-plan/model",  # z.ai coding planのモデル
            "anthropic/claude-3-haiku",  # 低コスト
        ]
        
        self.fallback_models = [
            "google/gemini-flash-1.5",  # 高速・低コスト
            "meta-llama/llama-3.2-3b-instruct:free",  # 無料
            "meta-llama/llama-3.1-8b-instruct:free",  # 無料
        ]
    
    def format_with_llm(self, content: str, title: str = "Untitled") -> tuple[str, str]:
        """LLMを使ってTXTを構造化MDに変換"""
        
        # まずフリーミアムモデルを試す
        for model in self.primary_models:
            try:
                result = self._call_llm(content, title, model, primary=True)
                if result:
                    return result, model
            except Exception as e:
                print(f"  [WARN] Primary model {model} failed: {e}")
                continue
        
        # フォールバックモデルを試す
        for model in self.fallback_models:
            try:
                result = self._call_llm(content, title, model, primary=False)
                if result:
                    return result, model
            except Exception as e:
                print(f"  [WARN] Fallback model {model} failed: {e}")
                continue
        
        # すべて失敗した場合、ルールベースにフォールバック
        print("  [INFO] All LLM models failed, using rule-based formatting")
        return self._rule_based_fallback(content, title), "rule-based"
    
    def _call_llm(self, content: str, title: str, model: str, primary: bool) -> Optional[str]:
        """LLMを呼び出す"""
        
        # プロンプトの作成
        prompt = self._create_prompt(content, title)
        
        # API設定
        if primary:
            # z.ai coding planのAPI
            api_url = "https://api.zai.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.primary_api_key}",
                "Content-Type": "application/json"
            }
        else:
            # OpenRouterのAPI
            api_url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/luckys4900/markdown-contexts",
                "X-Title": "Context Management System"
            }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "あなたは専門的なドキュメント整形アシスタントです。LLMの会話記録を構造化されたMarkdown形式に変換してください。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 8000,
            "temperature": 0.3,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decode failed: {e}")
    
    def _create_prompt(self, content: str, title: str) -> str:
        """LLMへのプロンプトを作成"""
        
        prompt = f"""以下のLLM会話記録を、LLMが理解しやすい構造化されたMarkdown形式に変換してください。

# タイトル
{title}

# 変換ルール
1. **セクション構造**: 以下のセクションで構成すること
   - 📊 ドキュメント情報（作成日時、対話数、トピック）
   - 📋 実行要約（全体の要約、3〜5行）
   - 🔑 重要ポイント（数字、スコア、価格、日付などの重要な情報、最大15個）
   - ✅ アクションアイテム（推奨事項、アクション項目、最大10個）
   - 💡 主な洞察（発見、結論、パターン、最大10個）
   - 💬 会話内容（ユーザーとアシスタントの対話、構造化）
   - 🔗 関連情報（トピック別の関連キーワード）
   - 🔍 検索用キーワード（重要なキーワード、最大20個）

2. **フォーマット**:
   - 見出しは # ## ### を適切に使用
   - 重要なポイントは箇条書き（- または 1.）
   - アクションアイテムは ✅ マークを使用
   - 洞察は 💡 マークを使用
   - ユーザー発言は 👤 マーク
   - アシスタント発言は 🤖 マーク

3. **情報の抽出**:
   - 数値情報（スコア、価格、日時）を明確に抽出
   - 結論と推奨事項を強調
   - リスクと機会を分類
   - 時系列を維持

4. **簡潔さ**:
   - 長すぎる会話は要約
   - 重複する情報は統合
   - 本質的な情報に焦点を当てる

# 会話記録
{content}

# 出力形式
上記のルールに従って、構造化されたMarkdown形式で出力してください。YAMLフロントマターは含めないでください。"""
        
        return prompt
    
    def _rule_based_fallback(self, content: str, title: str) -> str:
        """ルールベースのフォールバック処理"""
        
        # 既存の関数を再利用
        from context_organizer import (
            parse_llm_conversation,
            extract_topics,
            generate_title_from_conversation,
            extract_insights_from_messages,
            extract_key_points,
            generate_executive_summary,
            extract_action_items
        )
        
        messages = parse_llm_conversation(content)
        topics = extract_topics(messages)
        
        md_content = f"# {title}\n\n"
        
        # ドキュメント情報
        md_content += "---\n"
        md_content += "## 📊 ドキュメント情報\n\n"
        md_content += f"**作成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"**対話数**: {len(messages)} 回\n"
        md_content += f"**トピック**: {', '.join(topics)}\n\n"
        md_content += "---\n\n"
        
        # 実行要約
        md_content += "## 📋 実行要約\n\n"
        md_content += f"{generate_executive_summary(content)}\n\n"
        md_content += "---\n\n"
        
        # 重要ポイント
        key_points = extract_key_points(content)
        if key_points:
            md_content += "## 🔑 重要ポイント\n\n"
            for i, point in enumerate(key_points, 1):
                md_content += f"{i}. {point}\n"
            md_content += "\n---\n\n"
        
        # アクションアイテム
        action_items = extract_action_items(content)
        if action_items:
            md_content += "## ✅ アクションアイテム\n\n"
            for i, action in enumerate(action_items, 1):
                md_content += f"{i}. {action}\n"
            md_content += "\n---\n\n"
        
        # 主な洞察
        insights = extract_insights_from_messages(messages)
        if insights:
            md_content += "## 💡 主な洞察\n\n"
            for insight in insights:
                md_content += f"- {insight}\n"
            md_content += "\n---\n\n"
        
        # 会話内容
        md_content += "## 💬 会話内容\n\n"
        for i, msg in enumerate(messages, 1):
            role_label = "👤 **ユーザー**" if msg['role'] == 'user' else "🤖 **アシスタント**"
            md_content += f"\n### {i}. {role_label}\n\n"
            md_content += f"{msg['content']}\n\n"
            md_content += "---\n\n"
        
        # 関連情報
        md_content += "## 🔗 関連情報\n\n"
        for topic in topics:
            md_content += f"- **{topic}**: このトピックに関する詳細情報は上記の会話を参照\n"
        md_content += "\n"
        
        return md_content

formatter = LLMFormatter()
