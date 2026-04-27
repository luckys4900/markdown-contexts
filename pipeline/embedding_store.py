import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
from typing import List, Dict, Optional
import re

class EmbeddingStore:
    def __init__(self, storage_dir: Path = Path("storage/vector_db")):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=str(storage_dir))
        self.collection = self.client.get_or_create_collection(
            name="context_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    def extract_frontmatter(self, content: str) -> Dict:
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if match:
            frontmatter = {}
            for line in match.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
            return frontmatter, content[match.end():]
        return {}, content
    
    def add_document(self, file_path: Path, doc_id: Optional[str] = None):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, body = self.extract_frontmatter(content)
            
            full_text = f"{frontmatter.get('title', '')}\n{body}"
            embedding = self.model.encode(full_text)
            
            metadata = {
                'file_path': str(file_path),
                'category': frontmatter.get('category', 'unknown'),
                'tags': frontmatter.get('tags', '[]'),
                'date': frontmatter.get('date', ''),
                'title': frontmatter.get('title', file_path.stem)
            }
            
            if doc_id is None:
                doc_id = str(file_path)
            
            self.collection.add(
                documents=[full_text],
                embeddings=[embedding.tolist()],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            return True
        except Exception as e:
            print(f"Error adding {file_path}: {e}")
            return False
    
    def add_directory(self, dir_path: Path, pattern: str = "*.md"):
        files = list(dir_path.rglob(pattern))
        count = 0
        for file_path in files:
            if self.add_document(file_path):
                count += 1
        return count
    
    def search(self, query: str, n_results: int = 5, 
               category_filter: Optional[str] = None) -> List[Dict]:
        query_embedding = self.model.encode(query)
        
        where_filter = None
        if category_filter:
            where_filter = {"category": category_filter}
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
            where=where_filter
        )
        
        documents = []
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]
            
            documents.append({
                'content': doc,
                'metadata': metadata,
                'similarity': 1 - distance,
                'file_path': metadata.get('file_path', '')
            })
        
        return documents
    
    def get_all_categories(self) -> List[str]:
        results = self.collection.get(include=['metadatas'])
        categories = set()
        for metadata in results['metadatas']:
            if 'category' in metadata:
                categories.add(metadata['category'])
        return list(categories)
    
    def delete_document(self, doc_id: str):
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            print(f"Error deleting {doc_id}: {e}")
            return False
    
    def rebuild_index(self, context_dir: Path):
        self.client.delete_collection("context_documents")
        self.collection = self.client.get_or_create_collection(
            name="context_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        count = 0
        for subdir in ['analysis', 'strategy', 'memory', 'reports']:
            dir_path = context_dir / subdir
            if dir_path.exists():
                count += self.add_directory(dir_path)
        
        return count

store = EmbeddingStore()
