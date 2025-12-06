import streamlit as st

def render_agent_status(agent_steps, query_type):
    """Display agent execution steps"""
    
    with st.expander("🤖 Agent Execution Steps", expanded=False):
        st.markdown(f"**Query Type:** `{query_type}`")
        
        for i, step in enumerate(agent_steps, 1):
            if "analyzed" in step.lower():
                icon = "🔍"
                color = "blue"
            elif "retrieved" in step.lower():
                icon = "📚"
                color = "green"
            elif "generated" in step.lower():
                icon = "✍️"
                color = "orange"
            else:
                icon = "✅"
                color = "gray"
            
            st.markdown(f":{color}[{icon} **Step {i}:** {step}]")

def render_sources(sources):
    """Display source documents"""
    
    if sources:
        with st.expander("📄 Sources", expanded=False):
            for i, source in enumerate(sources, 1):
                st.markdown(f"**{i}.** {source}")