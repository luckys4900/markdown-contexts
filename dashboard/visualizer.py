import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import Dict, List
import pandas as pd

def create_flow_tree(agents: Dict) -> go.Figure:
    fig = go.Figure()
    
    nodes = []
    edges = []
    y_positions = {}
    
    master_agent = next((a for a in agents.values() if 'master' in a['id'].lower()), None)
    
    if master_agent:
        y_positions['master'] = 0.5
        nodes.append((0, 0.5, 'Master', master_agent['status']))
    
    slave_agents = [a for a in agents.values() if 'slave' in a['id'].lower() or 'master' not in a['id'].lower()]
    
    for i, agent in enumerate(slave_agents):
        x = (i + 1) * 0.2
        y = 0.3 + (i % 3) * 0.2
        y_positions[agent['id']] = y
        nodes.append((x, y, agent['name'], agent['status']))
        edges.append(((0, 0.5), (x, y)))
    
    x_coords = [n[0] for n in nodes]
    y_coords = [n[1] for n in nodes]
    labels = [f"{n[2]}\n({n[3]})" for n in nodes]
    colors = ['green' if n[3] == 'completed' else 'blue' if n[3] == 'running' else 'gray' for n in nodes]
    
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers+text',
        text=labels,
        textposition='top center',
        marker=dict(size=50, color=colors, line=dict(width=2, color='black')),
        name='Agents'
    ))
    
    for edge in edges:
        fig.add_trace(go.Scatter(
            x=[edge[0][0], edge[1][0]],
            y=[edge[0][1], edge[1][1]],
            mode='lines',
            line=dict(width=2, color='gray', dash='dot'),
            showlegend=False
        ))
    
    fig.update_layout(
        title='Multi-Agent Flow Visualization',
        xaxis=dict(showgrid=False, showticklabels=False, range=[-0.1, 1.1]),
        yaxis=dict(showgrid=False, showticklabels=False, range=[0, 1]),
        height=500,
        showlegend=False
    )
    
    return fig

def create_token_usage_graph(agents: Dict) -> go.Figure:
    agent_names = [a['name'] for a in agents.values()]
    token_usage = [a['tokens_used'] for a in agents.values()]
    colors = ['red' if 'master' in a['id'].lower() else 'blue' for a in agents.values()]
    
    fig = go.Figure(data=[
        go.Bar(
            x=agent_names,
            y=token_usage,
            marker_color=colors,
            text=token_usage,
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title='Token Usage by Agent',
        xaxis_title='Agent',
        yaxis_title='Tokens Used',
        height=400
    )
    
    return fig

def create_status_timeline(agents: Dict) -> go.Figure:
    fig = go.Figure()
    
    for agent in agents.values():
        fig.add_trace(go.Scatter(
            x=[datetime.now()],
            y=[agent['name']],
            mode='markers',
            marker=dict(
                size=20,
                color='green' if agent['status'] == 'completed' else 'blue' if agent['status'] == 'running' else 'gray'
            ),
            name=agent['name'],
            text=f"Status: {agent['status']}<br>Tokens: {agent['tokens_used']}<br>Tasks: {agent['tasks_completed']}",
            hoverinfo='text'
        ))
    
    fig.update_layout(
        title='Agent Status Timeline',
        xaxis_title='Time',
        yaxis_title='Agent',
        height=400,
        showlegend=False
    )
    
    return fig

def create_token_pie_chart(summary: Dict) -> go.Figure:
    fig = go.Figure(data=[
        go.Pie(
            labels=['Master Agent', 'Slave Agents'],
            values=[summary['master_tokens'], summary['slave_tokens']],
            hole=0.3,
            marker=dict(colors=['red', 'blue'])
        )
    ])
    
    fig.update_layout(
        title='Token Usage Distribution',
        height=400
    )
    
    return fig

def create_performance_metrics(summary: Dict) -> go.Figure:
    metrics = ['Total Tokens', 'Total Tasks', 'Active Agents', 'Completed Agents']
    values = [
        summary['total_tokens'],
        summary['total_tasks'],
        summary['active_agents'],
        summary['completed_agents']
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=metrics,
            y=values,
            marker_color='purple',
            text=values,
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title='Session Performance Metrics',
        yaxis_title='Count',
        height=400
    )
    
    return fig
