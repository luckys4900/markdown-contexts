import os
from openai import OpenAI
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

class LLMFormatter:
    def __init__(self):
        load_dotenv()
        
        self.primary_api_key = os.getenv("ZAI_API_KEY", "")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        # モデル設定
        self.primary_models = [
            "glm-4-flash",     # GLM-4 Flash（高速・低コスト）
            "glm-4",           # GLM-4
        ]
        
        self.fallback_models = [
            "google/gemini-flash-1.5",
            "meta-llama/llama-3.2-3b-instruct:free",
            "meta-llama/llama-3.1-8b-instruct:free",
        ]
        
        # デバッグ用: APIキーを表示（セキュリティ上、最初の数文字のみ）
        if self.primary_api_key:
            print(f"  [DEBUG] ZAI_API_KEY: {self.primary_api_key[:8]}...")
        else:
            print(f"  [WARN] ZAI_API_KEY not set in environment variables")
        
        if self.openrouter_api_key:
            print(f"  [DEBUG] OPENROUTER_API_KEY: {self.openrouter_api_key[:8]}...")
        else:
            print(f"  [WARN] OPENROUTER_API_KEY not set in environment variables")
    
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
        
        # プロンプトを非常にシンプルに
        prompt = f"""Convert this conversation to structured Markdown with these sections:

1. Document Info (creation time, count, topics)
2. Executive Summary (3-5 lines)
3. Key Points (max 15)
4. Action Items (max 10)
5. Key Insights (max 10)
6. Conversation Content
7. Related Info
8. Search Keywords (max 20)

Title: {title}

Conversation:
{content}

Return only Markdown content. No YAML frontmatter.
"""
        
        try:
            if primary:
                # z.ai API（OpenAI互換）
                print(f"  [DEBUG] Calling z.ai API with model: {model}")
                client = OpenAI(
                    base_url="https://open.bigmodel.cn/api/paas/v4",
                    api_key=self.primary_api_key,
                    timeout=60.0,
                    max_retries=2
                )
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                return response.choices[0].message.content
            else:
                # OpenRouter API
                print(f"  [DEBUG] Calling OpenRouter API with model: {model}")
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=self.openrouter_api_key,
                    default_headers={
                        "HTTP-Referer": "https://github.com/luckys4900/markdown-contexts",
                        "X-Title": "Context Management System"
                    },
                    timeout=60.0,
                    max_retries=2
                )
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
        except Exception as e:
            raise Exception(f"API call failed: {e}")
    
    def _create_prompt(self, content: str, title: str) -> str:
        """LLMへのプロンプトを作成（英語版）"""
        
        prompt = f"""Convert the following LLM conversation to a structured Markdown format.

# Title
{title}

# Conversion Rules
1. **Section Structure**: Create the following sections:
   - 📊 Document Information (creation time, conversation count, topics)
   - 📋 Executive Summary (overall summary, 3-5 lines)
   - 🔑 Key Points (numbers, scores, prices, dates, max 15 items)
   - ✅ Action Items (recommendations, action items, max 10 items)
   - 💡 Key Insights (findings, conclusions, patterns, max 10 items)
   - 💬 Conversation Content (structured user and assistant messages)
   - 🔗 Related Information (topic-related keywords)
   - 🔍 Search Keywords (important keywords, max 20 items)

2. **Formatting**:
   - Use # ## ### for headings appropriately
   - Use bullet points (- or 1.) for important points
   - Use ✅ mark for action items
   - Use 💡 mark for insights
   - Use 👤 mark for user speech
   - Use 🤖 mark for assistant speech

3. **Information Extraction**:
   - Clearly extract numeric information (scores, prices, dates)
   - Emphasize conclusions and recommendations
   - Categorize risks and opportunities
   - Maintain chronological order

4. **Conciseness**:
   - Summarize long conversations
   - Consolidate duplicate information
   - Focus on essential information

# Conversation Record
{content}

# Output Format
Convert to structured Markdown format following the rules above. Do not include YAML frontmatter.
"""
        
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
