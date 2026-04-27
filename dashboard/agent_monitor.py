import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import threading
import queue

class AgentMonitor:
    def __init__(self, log_dir: Path = Path("logs")):
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        self.message_queue = queue.Queue()
        self.agents = {}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = self.log_dir / f"session_{self.session_id}.json"
        
        self.running = False
        self.monitor_thread = None
        
    def start(self):
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_logs, daemon=True)
        self.monitor_thread.start()
    
    def stop(self):
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
    
    def _monitor_logs(self):
        while self.running:
            try:
                for log_file in self.log_dir.glob("agent_*.json"):
                    self._parse_log_file(log_file)
                time.sleep(0.5)
            except Exception as e:
                print(f"Monitor error: {e}")
    
    def _parse_log_file(self, log_file: Path):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.message_queue.put(data)
                self._update_agent_state(data)
        except Exception as e:
            pass
    
    def _update_agent_state(self, data: dict):
        agent_id = data.get('agent_id', 'unknown')
        if agent_id not in self.agents:
            self.agents[agent_id] = {
                'id': agent_id,
                'name': data.get('agent_name', 'Unknown'),
                'status': 'idle',
                'tokens_used': 0,
                'tasks_completed': 0,
                'current_task': None,
                'logs': [],
                'start_time': datetime.now().isoformat()
            }
        
        agent = self.agents[agent_id]
        agent['status'] = data.get('status', 'idle')
        agent['tokens_used'] = data.get('tokens_used', agent['tokens_used'])
        agent['current_task'] = data.get('task', None)
        
        if data.get('status') == 'completed':
            agent['tasks_completed'] += 1
        
        if 'message' in data:
            agent['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'message': data['message']
            })
            if len(agent['logs']) > 100:
                agent['logs'] = agent['logs'][-100:]
    
    def get_agent_states(self) -> Dict:
        return self.agents
    
    def get_session_summary(self) -> Dict:
        total_tokens = sum(a['tokens_used'] for a in self.agents.values())
        total_tasks = sum(a['tasks_completed'] for a in self.agents.values())
        
        master_tokens = next((a['tokens_used'] for a in self.agents.values() 
                            if 'master' in a['id'].lower()), 0)
        slave_tokens = total_tokens - master_tokens
        
        return {
            'session_id': self.session_id,
            'start_time': self.agents.get('master', {}).get('start_time'),
            'total_tokens': total_tokens,
            'master_tokens': master_tokens,
            'slave_tokens': slave_tokens,
            'total_tasks': total_tasks,
            'active_agents': sum(1 for a in self.agents.values() if a['status'] == 'running'),
            'completed_agents': sum(1 for a in self.agents.values() if a['status'] == 'completed')
        }
    
    def save_session(self):
        summary = {
            'session': self.get_session_summary(),
            'agents': self.agents
        }
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    def log_agent_event(self, agent_id: str, agent_name: str, status: str, 
                       task: Optional[str] = None, message: Optional[str] = None, 
                       tokens_used: int = 0):
        log_data = {
            'agent_id': agent_id,
            'agent_name': agent_name,
            'status': status,
            'task': task,
            'message': message,
            'tokens_used': tokens_used,
            'timestamp': datetime.now().isoformat()
        }
        
        log_file = self.log_dir / f"agent_{agent_id}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

monitor = AgentMonitor()
