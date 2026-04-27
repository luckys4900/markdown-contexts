import streamlit as st
import time
from pathlib import Path
from agent_monitor import monitor
from visualizer import (
    create_flow_tree,
    create_token_usage_graph,
    create_status_timeline,
    create_token_pie_chart,
    create_performance_metrics
)

st.set_page_config(
    page_title="Multi-Agent Visualization",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Multi-Agent Processing Visualization")
st.markdown("---")

monitor.start()

sidebar = st.sidebar
sidebar.header("Controls")

if sidebar.button("Start New Session"):
    monitor.stop()
    monitor.session_id = time.strftime("%Y%m%d_%H%M%S")
    monitor.session_file = monitor.log_dir / f"session_{monitor.session_id}.json"
    monitor.agents = {}
    monitor.start()
    st.rerun()

if sidebar.button("Stop Monitoring"):
    monitor.stop()
    st.rerun()

sidebar.markdown("---")
sidebar.header("Session Info")
session_summary = monitor.get_session_summary()
sidebar.text(f"Session ID: {session_summary['session_id']}")
sidebar.text(f"Active Agents: {session_summary['active_agents']}")
sidebar.text(f"Completed: {session_summary['completed_agents']}")

tab1, tab2, tab3, tab4 = st.tabs(["Flow Visualization", "Token Usage", "Status Timeline", "Logs"])

with tab1:
    st.header("Agent Flow Tree")
    agents = monitor.get_agent_states()
    
    if agents:
        fig = create_flow_tree(agents)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No agents currently running. Start a multi-agent session to see the visualization.")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Token Usage by Agent")
        agents = monitor.get_agent_states()
        if agents:
            fig = create_token_usage_graph(agents)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No token usage data available.")
    
    with col2:
        st.header("Token Distribution")
        summary = monitor.get_session_summary()
        if summary['total_tokens'] > 0:
            fig = create_token_pie_chart(summary)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No token distribution data available.")
    
    st.markdown("---")
    st.header("Performance Metrics")
    if summary['total_tokens'] > 0:
        fig = create_performance_metrics(summary)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Agent Status Timeline")
    agents = monitor.get_agent_states()
    if agents:
        fig = create_status_timeline(agents)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No status data available.")

with tab4:
    st.header("Agent Logs")
    agents = monitor.get_agent_states()
    
    if agents:
        selected_agent = st.selectbox(
            "Select Agent",
            options=list(agents.keys()),
            format_func=lambda x: agents[x]['name']
        )
        
        if selected_agent:
            agent = agents[selected_agent]
            st.subheader(f"{agent['name']} Logs")
            
            for log in agent['logs'][-20:]:
                with st.expander(f"{log['timestamp']}"):
                    st.text(log['message'])
    else:
        st.info("No logs available.")

st.markdown("---")
st.subheader("Session Summary")
summary = monitor.get_session_summary()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tokens", summary['total_tokens'])
col2.metric("Master Tokens", summary['master_tokens'])
col3.metric("Slave Tokens", summary['slave_tokens'])
col4.metric("Total Tasks", summary['total_tasks'])

if st.button("Save Session"):
    monitor.save_session()
    st.success("Session saved successfully!")

monitor.stop()
