import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from mcp_connector import connector
from rag_retriever import retriever

class AutoMemory:
    def __init__(self, memory_dir: Path = Path("memory")):
        self.memory_dir = memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_insights(self, analysis_result: Dict) -> List[Dict]:
        insights = []
        
        content = analysis_result.get('content', '')
        query = analysis_result.get('query', '')
        
        insight_patterns = {
            'finding': r'(発見|発見された|判明した|明らかになった)[:：]\s*(.+?)(?:\n|$)',
            'conclusion': r'(結論|まとめ|結論として)[:：]\s*(.+?)(?:\n|$)',
            'recommendation': r'(推奨|推奨事項|提案)[:：]\s*(.+?)(?:\n|$)',
            'pattern': r'(パターン|傾向|パターン認識)[:：]\s*(.+?)(?:\n|$)',
            'risk': r'(リスク|懸念|注意点)[:：]\s*(.+?)(?:\n|$)',
            'opportunity': r'(機会|可能性|チャンス)[:：]\s*(.+?)(?:\n|$)'
        }
        
        for insight_type, pattern in insight_patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                insights.append({
                    'type': insight_type,
                    'content': match.group(2).strip(),
                    'context': query,
                    'timestamp': datetime.now().isoformat()
                })
        
        return insights
    
    def generate_frontmatter(self, insights: List[Dict], 
                            query: str, 
                            category: str = 'memory') -> str:
        tags = set()
        tags.add(category)
        
        for insight in insights:
            tags.add(insight['type'])
        
        date = datetime.now().strftime('%Y-%m-%d')
        title = f"Memory: {query[:50]}..."
        
        frontmatter = f"""---
date: {date}
category: {category}
tags: {list(tags)}
title: {title}
generated_by: auto_memory
---

"""
        return frontmatter
    
    def generate_memory_content(self, insights: List[Dict], 
                               query: str, 
                               context: str) -> str:
        content = f"# Memory: {query}\n\n"
        content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += "---\n\n"
        
        content += "## Insights\n\n"
        for insight in insights:
            content += f"### {insight['type'].capitalize()}\n"
            content += f"{insight['content']}\n\n"
        
        content += "## Original Query\n\n"
        content += f"{query}\n\n"
        
        content += "## Context Summary\n\n"
        content += f"{context[:500]}...\n\n"
        
        return content
    
    def save_memory(self, analysis_result: Dict) -> Optional[str]:
        insights = self.extract_insights(analysis_result)
        
        if not insights:
            return None
        
        query = analysis_result.get('query', 'unknown')
        context = analysis_result.get('context', '')
        category = analysis_result.get('category', 'memory')
        
        frontmatter = self.generate_frontmatter(insights, query, category)
        content = self.generate_memory_content(insights, query, context)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"memory_{timestamp}.md"
        filepath = self.memory_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)
        
        for insight in insights:
            connector.store_insight(
                insight_type=insight['type'],
                content=insight['content'],
                source_file=str(filepath),
                tags=[insight['type'], category]
            )
        
        return str(filepath)
    
    def auto_tag_document(self, content: str) -> List[str]:
        tags = []
        
        keywords = {
            'strategy': ['戦略', 'ストラテジー', 'アプローチ', 'フレームワーク'],
            'analysis': ['分析', '調査', 'データ', '検証'],
            'risk': ['リスク', '懸念', '注意', '警告'],
            'opportunity': ['機会', 'チャンス', '可能性', '見込み'],
            'pattern': ['パターン', '傾向', 'トレンド'],
            'insight': ['洞察', '発見', '知見']
        }
        
        content_lower = content.lower()
        for tag, kw_list in keywords.items():
            if any(kw in content_lower for kw in kw_list):
                tags.append(tag)
        
        return tags
    
    def create_summary_report(self, insights: List[Dict]) -> str:
        summary = f"# Memory Summary Report\n\n"
        summary += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        summary += f"Total Insights: {len(insights)}\n\n"
        summary += "---\n\n"
        
        by_type = {}
        for insight in insights:
            itype = insight['type']
            if itype not in by_type:
                by_type[itype] = []
            by_type[itype].append(insight)
        
        for itype, items in by_type.items():
            summary += f"## {itype.capitalize()} ({len(items)})\n\n"
            for item in items[:5]:
                summary += f"- {item['content']}\n"
            summary += "\n"
        
        return summary

auto_memory = AutoMemory()
