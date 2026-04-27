import os
import re
import shutil
from datetime import datetime
from pathlib import Path
import json

CONTEXT_DIR = Path(__file__).parent
INBOX_DIR = CONTEXT_DIR / "受信トレイ"
CATEGORIES = {
    "戦略": ["戦略", "ストラテジー", "フレームワーク", "アプローチ", "方針", "plan", "strategy", "framework"],
    "分析": ["分析", "調査", "研究", "データ", "検証", "テスト", "analysis", "research", "data", "test"],
    "記憶": ["記憶", "学習", "ノウハウ", "知見", "メモ", "備忘", "memory", "learn", "note", "memo", "対話", "会話", "思考"],
    "レポート": ["レポート", "報告", "サマリー", "結論", "まとめ", "report", "summary", "conclusion"]
}

def extract_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        frontmatter_str = match.group(1)
        frontmatter = {}
        
        for line in frontmatter_str.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                if key in ['作成日', 'カテゴリ', 'タイトル']:
                    frontmatter[key] = value
                elif key == 'date':
                    frontmatter['作成日'] = value
                elif key == 'category':
                    frontmatter['カテゴリ'] = value
                elif key == 'title':
                    frontmatter['タイトル'] = value
        
        return frontmatter, content[match.end():]
    return None, content

def create_frontmatter(content, category):
    date = datetime.now().strftime('%Y-%m-%d')
    
    tags = []
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw.lower() in content.lower():
                if cat not in tags:
                    tags.append(cat)
    
    if category not in tags:
        tags.insert(0, category)
    
    domain_tags = [tag for tag in tags if tag in ['投資', '株式', '仮想通貨', 'FX']]
    importance_tags = [tag for tag in tags if tag in ['高', '中', '低', '重要', '緊急']]
    topic_tags = [tag for tag in tags if tag not in domain_tags + importance_tags]
    
    domain_str = str(domain_tags) if domain_tags else '[]'
    importance_str = str(importance_tags) if importance_tags else '[]'
    topic_str = str(topic_tags) if topic_tags else '[]'
    
    frontmatter = f"""---
# メタ情報
作成日: {date}
カテゴリ: {category}
タイトル: Untitled

# タグ（ドメイン・重要度・トピック）
タグ:
  ドメイン: {domain_str}
  重要度: {importance_str}
  トピック: {topic_str}

# 自動生成情報
生成元: opencode
バージョン: 1.0
---

"""
    
    return frontmatter + content

def categorize_file(content, filename):
    existing_frontmatter, body = extract_frontmatter(content)
    
    if existing_frontmatter and 'カテゴリ' in existing_frontmatter:
        return existing_frontmatter['カテゴリ']
    
    if existing_frontmatter and 'category' in existing_frontmatter:
        return existing_frontmatter['category']
    
    content_lower = (content + ' ' + filename).lower()
    
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                return category
    
    return '分析'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        category = categorize_file(content, filepath.name)
        frontmatter, body = extract_frontmatter(content)
        
        # 既存のYAMLフロントマターがある場合、そのまま使用
        if frontmatter:
            # 必要な情報が不足している場合のみ補完
            if '作成日' not in frontmatter and 'date' not in frontmatter:
                frontmatter['作成日'] = datetime.now().strftime('%Y-%m-%d')
            if 'カテゴリ' not in frontmatter and 'category' not in frontmatter:
                frontmatter['カテゴリ'] = category
            
            # YAMLフロントマターを再構築
            frontmatter_str = '---\n'
            frontmatter_str += '# メタ情報\n'
            if '作成日' in frontmatter:
                frontmatter_str += f'作成日: {frontmatter["作成日"]}\n'
            elif 'date' in frontmatter:
                frontmatter_str += f'作成日: {frontmatter["date"]}\n'
            
            if 'カテゴリ' in frontmatter:
                frontmatter_str += f'カテゴリ: {frontmatter["カテゴリ"]}\n'
            elif 'category' in frontmatter:
                frontmatter_str += f'カテゴリ: {frontmatter["category"]}\n'
            
            if 'タイトル' in frontmatter:
                frontmatter_str += f'タイトル: {frontmatter["タイトル"]}\n'
            elif 'title' in frontmatter:
                frontmatter_str += f'タイトル: {frontmatter["title"]}\n'
            else:
                frontmatter_str += 'タイトル: Untitled\n'
            
            # タグが存在しない場合のみ自動生成
            if 'タグ' not in frontmatter:
                frontmatter_str += '\n# タグ（ドメイン・重要度・トピック）\n'
                frontmatter_str += 'タグ:\n'
                frontmatter_str += '  ドメイン: []\n'
                frontmatter_str += '  重要度: []\n'
                frontmatter_str += '  トピック: []\n'
            else:
                frontmatter_str += '\n# タグ（ドメイン・重要度・トピック）\n'
                tags = frontmatter.get('タグ', {})
                if isinstance(tags, dict):
                    for key, value in tags.items():
                        frontmatter_str += f'タグ:\n  {key}: {value}\n'
                else:
                    frontmatter_str += f'タグ: {tags}\n'
            
            frontmatter_str += '\n# 自動生成情報\n'
            frontmatter_str += '生成元: opencode\n'
            frontmatter_str += 'バージョン: 1.0\n'
            frontmatter_str += '---\n\n'
            
            content = frontmatter_str + body
        else:
            # YAMLフロントマターがない場合、新規生成
            content = create_frontmatter(content, category)
        
        target_dir = CONTEXT_DIR / category
        target_path = target_dir / filepath.name
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        file_size = os.path.getsize(target_path)
        os.remove(filepath)
        
        return {
            'filename': filepath.name,
            'category': category,
            'size': file_size
        }
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def parse_llm_conversation(content):
    """LLMのやり取りを解析して構造化する"""
    
    messages = []
    current_role = None
    current_content = []
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # ユーザーメッセージの検出
        user_patterns = [
            r'^User:',
            r'^ユーザー:',
            r'^Q:',
            r'^質問:',
            r'^>>'
        ]
        
        # アシスタントメッセージの検出
        assistant_patterns = [
            r'^Assistant:',
            r'^アシスタント:',
            r'^A:',
            r'^回答:',
            r'^>>',
            r'^\[\s*Answer\s*\]'
        ]
        
        is_user = any(re.match(pattern, line, re.IGNORECASE) for pattern in user_patterns)
        is_assistant = any(re.match(pattern, line, re.IGNORECASE) for pattern in assistant_patterns)
        
        if is_user or is_assistant:
            if current_content:
                messages.append({
                    'role': current_role,
                    'content': '\n'.join(current_content).strip()
                })
            
            current_role = 'user' if is_user else 'assistant'
            current_content = []
            
            # パターン部分を削除
            for pattern in user_patterns + assistant_patterns:
                line = re.sub(pattern, '', line, flags=re.IGNORECASE)
            
            if line.strip():
                current_content.append(line.strip())
        elif current_role:
            current_content.append(line)
    
    if current_content:
        messages.append({
            'role': current_role,
            'content': '\n'.join(current_content).strip()
        })
    
    return messages

def extract_topics(messages):
    """メッセージからトピックを抽出"""
    all_text = ' '.join([msg['content'] for msg in messages])
    
    topics = []
    
    topic_keywords = {
        '投資戦略': ['戦略', 'ストラテジー', '投資', 'トレード'],
        '技術分析': ['RSI', 'MACD', 'ボリンジャー', '移動平均', 'テクニカル'],
        'システム設計': ['アーキテクチャ', '設計', 'システム', '実装'],
        'データ分析': ['データ', '分析', '統計', 'パターン'],
        'AI/ML': ['AI', '機械学習', 'モデル', 'トークン', 'LLM'],
        'プロセス': ['フロー', 'プロセス', 'ワークフロー', '手順']
    }
    
    for topic, keywords in topic_keywords.items():
        if any(kw in all_text for kw in keywords):
            topics.append(topic)
    
    return topics if topics else ['一般']

def generate_title_from_conversation(messages):
    """会話からタイトルを生成"""
    if not messages:
        return "Untitled Conversation"
    
    # 最初のユーザーメッセージからタイトルを生成
    first_user_msg = next((msg for msg in messages if msg['role'] == 'user'), None)
    if first_user_msg:
        title = first_user_msg['content'][:50]
        if len(first_user_msg['content']) > 50:
            title += "..."
        return title
    
    return "Untitled Conversation"

def txt_to_markdown(content, filename):
    """TXTをMarkdown形式に変換"""
    
    messages = parse_llm_conversation(content)
    topics = extract_topics(messages)
    title = generate_title_from_conversation(messages)
    
    # Markdown形式に変換
    md_content = f"# {title}\n\n"
    md_content += f"## 概要\n\n"
    md_content += f"このドキュメントはLLMとの対話を記録したものです。\n\n"
    
    if topics:
        md_content += f"**トピック**: {', '.join(topics)}\n\n"
    
    md_content += f"## 対話履歴\n\n"
    md_content += f"**対話数**: {len(messages)}\n"
    md_content += f"**作成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    md_content += "---\n\n"
    md_content += "## 会話内容\n\n"
    
    for i, msg in enumerate(messages, 1):
        role_label = "👤 ユーザー" if msg['role'] == 'user' else "🤖 アシスタント"
        md_content += f"### {role_label}\n\n"
        md_content += f"{msg['content']}\n\n"
        md_content += "---\n\n"
    
    # 洞察の抽出（パターンマッチング）
    insights = extract_insights_from_messages(messages)
    if insights:
        md_content += "## 主な洞察\n\n"
        for insight in insights:
            md_content += f"- {insight}\n"
        md_content += "\n"
    
    return md_content, title, topics

def extract_insights_from_messages(messages):
    """メッセージから洞察を抽出"""
    insights = []
    
    insight_patterns = [
        r'(発見|見つかった|判明した)[:：]\s*(.+?)(?:\n|$)',
        r'(結論|まとめ)[:：]\s*(.+?)(?:\n|$)',
        r'(推奨|提案)[:：]\s*(.+?)(?:\n|$)',
        r'(重要|ポイント)[:：]\s*(.+?)(?:\n|$)'
    ]
    
    all_text = ' '.join([msg['content'] for msg in messages])
    
    for pattern in insight_patterns:
        matches = re.finditer(pattern, all_text, re.IGNORECASE)
        for match in matches:
            insight = match.group(2).strip()
            if insight and len(insight) > 10:
                insights.append(insight)
    
    return insights[:5]  # 最大5つの洞察

def process_txt_file(filepath):
    """TXTファイルを処理してMDに変換"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        md_content, title, topics = txt_to_markdown(content, filepath.name)
        
        # MDファイルとして保存
        md_filename = filepath.stem + '.md'
        md_filepath = filepath.parent / md_filename
        
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # TXTファイルを削除
        os.remove(filepath)
        
        return {
            'original_filename': filepath.name,
            'new_filename': md_filename,
            'title': title,
            'topics': topics,
            'is_converted': True
        }
        
    except Exception as e:
        print(f"  ✗ Error processing TXT: {e}")
        return None

def main():
    print("=" * 70)
    print("                    Context Management System")
    print("=" * 70)
    print()
    
    # すべてのファイルを取得
    all_files = list(INBOX_DIR.glob('*.*'))
    
    if not all_files:
        print("No files found in 受信トレイ/")
        print("=" * 70)
        return
    
    # TXTファイルとMDファイルに分類
    txt_files = [f for f in all_files if f.suffix.lower() == '.txt']
    md_files = [f for f in all_files if f.suffix.lower() == '.md']
    
    print(f"[受信トレイ] 内のファイル:")
    print(f"  - TXTファイル: {len(txt_files)} 件")
    print(f"  - MDファイル: {len(md_files)} 件")
    print()
    
    results = []
    category_counts = {cat: 0 for cat in CATEGORIES.keys()}
    
    # TXTファイルをMDに変換
    if txt_files:
        print("Step 1: TXTファイルをMDに変換中...")
        print("-" * 70)
        
        for filepath in txt_files:
            print(f"\n[Converting] {filepath.name}")
            result = process_txt_file(filepath)
            if result:
                print(f"  [OK] 変換完了: {result['original_filename']} -> {result['new_filename']}")
                print(f"  [INFO] タイトル: {result['title']}")
                print(f"  [INFO] トピック: {', '.join(result['topics'])}")
        
        # 変換後にMDファイルを再取得
        md_files = list(INBOX_DIR.glob('*.md'))
        print()
    
    # MDファイルを処理
    if md_files:
        print("Step 2: MDファイルを整理中...")
        print("-" * 70)
        
        for filepath in md_files:
            print(f"\n[Processing] {filepath.name}")
            result = process_file(filepath)
            if result:
                results.append(result)
                category_counts[result['category']] += 1
                print(f"  [OK] 移動先: {result['category']}/")
                print(f"  [INFO] ファイルサイズ: {result['size']} bytes")
    
    # サマリー表示
    print()
    print("=" * 70)
    print("                         整理サマリー")
    print("=" * 70)
    print()
    print(f"[統計] 処理統計:")
    print(f"  - TXT -> MD変換: {len(txt_files)} 件")
    print(f"  - MDファイル整理: {len(results)} 件")
    print(f"  - 合計処理: {len(txt_files) + len(results)} 件")
    print()
    
    print(f"[カテゴリ] カテゴリ別:")
    for category, count in category_counts.items():
        if count > 0:
            print(f"  - {category}/: {count} 件")
    print()
    
    if results:
        print(f"[詳細] 詳細:")
        for result in results:
            print(f"  - {result['filename']} -> {result['category']}/ ({result['size']} bytes)")
    print()
    
    print("=" * 70)
    print("                        全処理完了!")
    print("=" * 70)
    print()

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
