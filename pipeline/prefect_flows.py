from prefect import flow, task, get_run_logger
from prefect.context import get_run_context
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

from embedding_store import store
from rag_retriever import retriever
from mcp_connector import connector
from auto_memory import auto_memory

@task
def rebuild_vector_index(context_dir: Path) -> int:
    logger = get_run_logger()
    logger.info(f"Rebuilding vector index from {context_dir}")
    
    count = store.rebuild_index(context_dir)
    logger.info(f"Indexed {count} documents")
    
    return count

@task
def search_context(query: str, 
                   max_tokens: int = 8000,
                   category: Optional[str] = None) -> Dict:
    logger = get_run_logger()
    logger.info(f"Searching context for: {query}")
    
    retriever.max_tokens = max_tokens
    context_data = retriever.retrieve_context(query, top_k=5, category=category)
    
    logger.info(f"Found {context_data['num_documents']} documents, "
                f"using ~{context_data['token_usage']} tokens")
    
    return context_data

@task
def check_cache(query: str, context_hash: str) -> Optional[Dict]:
    logger = get_run_logger()
    
    cached = connector.get_cached_context(query, context_hash)
    if cached:
        logger.info(f"Cache hit for query: {query}")
    else:
        logger.info(f"Cache miss for query: {query}")
    
    return cached

@task
def cache_context(query: str, context_hash: str, context_data: Dict):
    logger = get_run_logger()
    connector.cache_context(query, context_hash, context_data)
    logger.info(f"Context cached: {context_hash}")

@task
def extract_insights(analysis_result: Dict) -> List[Dict]:
    logger = get_run_logger()
    
    insights = auto_memory.extract_insights(analysis_result)
    logger.info(f"Extracted {len(insights)} insights")
    
    return insights

@task
def save_to_memory(analysis_result: Dict) -> Optional[str]:
    logger = get_run_logger()
    
    filepath = auto_memory.save_memory(analysis_result)
    if filepath:
        logger.info(f"Memory saved to: {filepath}")
    else:
        logger.info("No insights to save")
    
    return filepath

@task
def log_agent_communication(from_agent: str, to_agent: str,
                           message_type: str, payload: Dict) -> bool:
    logger = get_run_logger()
    
    success = connector.send_message(from_agent, to_agent, message_type, payload)
    if success:
        logger.info(f"Communication logged: {from_agent} -> {to_agent}")
    
    return success

@task
def generate_summary_report(insights: List[Dict]) -> str:
    logger = get_run_logger()
    
    report = auto_memory.create_summary_report(insights)
    logger.info("Summary report generated")
    
    return report

@flow(name="Context Analysis Pipeline")
def context_analysis_flow(query: str,
                         category: Optional[str] = None,
                         use_cache: bool = True,
                         max_tokens: int = 8000) -> Dict:
    logger = get_run_logger()
    logger.info(f"Starting context analysis for: {query}")
    
    context_hash = hashlib.md5(query.encode()).hexdigest()
    
    cached_result = None
    if use_cache:
        cached_result = check_cache(query, context_hash)
    
    if cached_result:
        return {
            'query': query,
            'context': cached_result,
            'from_cache': True,
            'status': 'completed'
        }
    
    context_data = search_context(query, max_tokens=max_tokens, category=category)
    
    if use_cache:
        cache_context(query, context_hash, context_data)
    
    analysis_result = {
        'query': query,
        'context': context_data['context'],
        'sources': context_data['sources'],
        'token_usage': context_data['token_usage'],
        'category': category or 'analysis'
    }
    
    insights = extract_insights(analysis_result)
    
    memory_path = save_to_memory(analysis_result)
    
    if insights:
        log_agent_communication(
            from_agent='analyzer',
            to_agent='memory',
            message_type='insights_extracted',
            payload={'count': len(insights), 'query': query}
        )
    
    summary = generate_summary_report(insights)
    
    result = {
        'query': query,
        'context': context_data,
        'insights': insights,
        'memory_path': memory_path,
        'summary': summary,
        'from_cache': False,
        'status': 'completed'
    }
    
    logger.info(f"Analysis completed: {len(insights)} insights extracted")
    
    return result

@flow(name="Batch Context Analysis")
def batch_analysis_flow(queries: List[str],
                       category: Optional[str] = None,
                       max_tokens: int = 8000) -> List[Dict]:
    logger = get_run_logger()
    logger.info(f"Starting batch analysis for {len(queries)} queries")
    
    results = []
    for query in queries:
        result = context_analysis_flow(
            query=query,
            category=category,
            max_tokens=max_tokens
        )
        results.append(result)
    
    logger.info(f"Batch analysis completed: {len(results)} queries processed")
    
    return results

@flow(name="Index Rebuild Flow")
def index_rebuild_flow(context_dir: Path) -> int:
    logger = get_run_logger()
    logger.info("Starting index rebuild")
    
    count = rebuild_vector_index(context_dir)
    
    logger.info(f"Index rebuild completed: {count} documents indexed")
    
    return count

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        result = context_analysis_flow(query=query)
        print(f"Analysis completed: {len(result['insights'])} insights")
    else:
        print("Usage: python prefect_flows.py <query>")
