from typing import List, Dict, Optional
from pathlib import Path
from embedding_store import store

class RAGRetriever:
    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.store = store
    
    def retrieve_context(self, query: str, 
                        top_k: int = 5,
                        category: Optional[str] = None,
                        min_similarity: float = 0.3) -> Dict:
        results = self.store.search(query, n_results=top_k, category_filter=category)
        
        filtered_results = [
            r for r in results 
            if r['similarity'] >= min_similarity
        ]
        
        context_parts = []
        metadata_list = []
        total_tokens = 0
        
        for result in filtered_results:
            content = result['content']
            metadata = result['metadata']
            similarity = result['similarity']
            
            estimated_tokens = len(content.split()) * 1.3
            
            if total_tokens + estimated_tokens > self.max_tokens:
                remaining_tokens = self.max_tokens - total_tokens
                if remaining_tokens > 100:
                    words = content.split()
                    words = words[:int(remaining_tokens / 1.3)]
                    truncated_content = ' '.join(words)
                    context_parts.append(f"[{metadata['title']}]\n{truncated_content}...")
                    metadata_list.append(metadata)
                    total_tokens += len(truncated_content.split()) * 1.3
                break
            
            context_parts.append(f"[{metadata['title']}]\n{content}")
            metadata_list.append(metadata)
            total_tokens += estimated_tokens
        
        context = '\n\n---\n\n'.join(context_parts)
        
        return {
            'context': context,
            'sources': metadata_list,
            'token_usage': int(total_tokens),
            'num_documents': len(context_parts),
            'query': query
        }
    
    def retrieve_with_summary(self, query: str,
                             top_k: int = 5,
                             category: Optional[str] = None) -> Dict:
        results = self.store.search(query, n_results=top_k, category_filter=category)
        
        summaries = []
        for result in results:
            metadata = result['metadata']
            similarity = result['similarity']
            
            summaries.append({
                'title': metadata.get('title', ''),
                'category': metadata.get('category', ''),
                'date': metadata.get('date', ''),
                'similarity': similarity,
                'file_path': metadata.get('file_path', '')
            })
        
        return {
            'summaries': summaries,
            'query': query
        }
    
    def get_relevant_categories(self, query: str, top_n: int = 3) -> List[str]:
        categories = self.store.get_all_categories()
        
        category_scores = []
        for category in categories:
            results = self.store.search(query, n_results=1, category_filter=category)
            if results and results[0]['similarity'] > 0.2:
                category_scores.append((category, results[0]['similarity']))
        
        category_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [cat[0] for cat in category_scores[:top_n]]
    
    def build_context_prompt(self, query: str, 
                             max_context_docs: int = 3,
                             category: Optional[str] = None) -> str:
        context_data = self.retrieve_context(
            query, 
            top_k=max_context_docs, 
            category=category
        )
        
        prompt = f"""Query: {query}

Relevant Context (from {context_data['num_documents']} documents, ~{context_data['token_usage']} tokens):

{context_data['context']}

---
Sources:
"""
        for i, source in enumerate(context_data['sources'], 1):
            prompt += f"\n{i}. {source['title']} ({source['category']}, {source['date']})"
        
        return prompt

retriever = RAGRetriever()
