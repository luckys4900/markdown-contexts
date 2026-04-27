import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
import grpc
from concurrent import futures
import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPConnector:
    def __init__(self, db_path: Path = Path("storage/mcp.db")):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        
        self.agent_registry = {}
        self.storage_backends = {}
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_communications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_agent TEXT,
                to_agent TEXT,
                message_type TEXT,
                payload TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS context_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                context_hash TEXT,
                context_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_type TEXT,
                content TEXT,
                source_file TEXT,
                tags TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_agent(self, agent_id: str, agent_name: str, 
                      capabilities: List[str]):
        self.agent_registry[agent_id] = {
            'name': agent_name,
            'capabilities': capabilities,
            'status': 'active'
        }
        logger.info(f"Agent registered: {agent_id} ({agent_name})")
    
    def send_message(self, from_agent: str, to_agent: str, 
                    message_type: str, payload: Dict) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO agent_communications 
                (from_agent, to_agent, message_type, payload)
                VALUES (?, ?, ?, ?)
            ''', (from_agent, to_agent, message_type, json.dumps(payload)))
            
            conn.commit()
            logger.info(f"Message: {from_agent} -> {to_agent} ({message_type})")
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
        finally:
            conn.close()
    
    def get_agent_messages(self, agent_id: str, limit: int = 10) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT from_agent, to_agent, message_type, payload, timestamp
            FROM agent_communications
            WHERE to_agent = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (agent_id, limit))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'from_agent': row[0],
                'to_agent': row[1],
                'message_type': row[2],
                'payload': json.loads(row[3]),
                'timestamp': row[4]
            })
        
        conn.close()
        return messages
    
    def cache_context(self, query: str, context_hash: str, context_data: Dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO context_cache 
                (query, context_hash, context_data)
                VALUES (?, ?, ?)
            ''', (query, context_hash, json.dumps(context_data)))
            
            conn.commit()
        except Exception as e:
            logger.error(f"Error caching context: {e}")
        finally:
            conn.close()
    
    def get_cached_context(self, query: str, context_hash: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT context_data, timestamp
            FROM context_cache
            WHERE query = ? AND context_hash = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (query, context_hash))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None
    
    def store_insight(self, insight_type: str, content: str, 
                     source_file: str, tags: List[str]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO memory_insights 
                (insight_type, content, source_file, tags)
                VALUES (?, ?, ?, ?)
            ''', (insight_type, content, source_file, json.dumps(tags)))
            
            conn.commit()
            logger.info(f"Insight stored: {insight_type}")
        except Exception as e:
            logger.error(f"Error storing insight: {e}")
        finally:
            conn.close()
    
    def get_insights(self, insight_type: Optional[str] = None, 
                    limit: int = 10) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if insight_type:
            cursor.execute('''
                SELECT insight_type, content, source_file, tags, timestamp
                FROM memory_insights
                WHERE insight_type = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (insight_type, limit))
        else:
            cursor.execute('''
                SELECT insight_type, content, source_file, tags, timestamp
                FROM memory_insights
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        insights = []
        for row in cursor.fetchall():
            insights.append({
                'insight_type': row[0],
                'content': row[1],
                'source_file': row[2],
                'tags': json.loads(row[3]),
                'timestamp': row[4]
            })
        
        conn.close()
        return insights
    
    def connect_storage(self, backend: str, config: Dict):
        if backend == 's3':
            try:
                import boto3
                self.storage_backends['s3'] = boto3.client('s3', **config)
                logger.info("S3 storage connected")
            except Exception as e:
                logger.error(f"Error connecting S3: {e}")
        elif backend == 'minio':
            try:
                from minio import Minio
                self.storage_backends['minio'] = Minio(**config)
                logger.info("MinIO storage connected")
            except Exception as e:
                logger.error(f"Error connecting MinIO: {e}")
    
    def store_to_backend(self, backend: str, key: str, data: bytes) -> bool:
        if backend not in self.storage_backends:
            logger.error(f"Backend {backend} not connected")
            return False
        
        try:
            if backend == 's3':
                self.storage_backends[backend].put_object(
                    Bucket='context-storage',
                    Key=key,
                    Body=data
                )
            elif backend == 'minio':
                self.storage_backends[backend].put_object(
                    'context-storage',
                    key,
                    data,
                    length=len(data)
                )
            return True
        except Exception as e:
            logger.error(f"Error storing to {backend}: {e}")
            return False

connector = MCPConnector()
