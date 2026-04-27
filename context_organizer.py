import os
import re
import shutil
from datetime import datetime
from pathlib import Path

CONTEXT_DIR = Path(__file__).parent
INBOX_DIR = CONTEXT_DIR / "inbox"
CATEGORIES = {
    "strategy": ["戦略", "ストラテジー", "フレームワーク", "アプローチ", "方針", "plan", "strategy", "framework"],
    "analysis": ["分析", "調査", "研究", "データ", "検証", "テスト", "analysis", "research", "data", "test"],
    "memory": ["記憶", "学習", "ノウハウ", "知見", "メモ", "備忘", "memory", "learn", "note", "memo"],
    "reports": ["レポート", "報告", "サマリー", "結論", "まとめ", "report", "summary", "conclusion"]
}

def extract_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        frontmatter_str = match.group(1)
        frontmatter = {}
        for line in frontmatter_str.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
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
    
    tags_str = str(tags).replace("'", '"')
    
    frontmatter = f"""---
date: {date}
category: {category}
tags: {tags_str}
title: Untitled
---

"""
    
    return frontmatter + content

def categorize_file(content, filename):
    existing_frontmatter, body = extract_frontmatter(content)
    
    if existing_frontmatter and 'category' in existing_frontmatter:
        return existing_frontmatter['category']
    
    content_lower = (content + ' ' + filename).lower()
    
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                return category
    
    return 'analysis'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        category = categorize_file(content, filepath.name)
        frontmatter, body = extract_frontmatter(content)
        
        if not frontmatter:
            content = create_frontmatter(content, category)
        else:
            if 'date' not in frontmatter:
                frontmatter['date'] = datetime.now().strftime('%Y-%m-%d')
            if 'category' not in frontmatter:
                frontmatter['category'] = category
            
            frontmatter_str = '---\n'
            for key, value in frontmatter.items():
                frontmatter_str += f'{key}: {value}\n'
            frontmatter_str += '---\n'
            
            content = frontmatter_str + body
        
        target_dir = CONTEXT_DIR / category
        target_path = target_dir / filepath.name
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        os.remove(filepath)
        print(f"Moved: {filepath.name} -> {category}/")
        
    except Exception as e:
        print(f"Error processing {filepath.name}: {e}")

def main():
    print("Context Organizer started...")
    
    md_files = list(INBOX_DIR.glob('*.md'))
    
    if not md_files:
        print("No MD files found in inbox/")
        return
    
    print(f"Found {len(md_files)} MD file(s)")
    
    for filepath in md_files:
        process_file(filepath)
    
    print("Organizing completed!")

if __name__ == '__main__':
    main()
