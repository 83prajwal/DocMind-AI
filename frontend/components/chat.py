import streamlit as st
from utils.api_client import api_client
from components.status_display import render_agent_status, render_sources

def render_chat():
    """Render the chat interface"""
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display agent steps and sources for assistant messages
            if message["role"] == "assistant" and "metadata" in message:
                metadata = message["metadata"]
                if "agent_steps" in metadata:
                    render_agent_status(metadata["agent_steps"], metadata.get("query_type", "unknown"))
                if "sources" in metadata:
                    render_sources(metadata["sources"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from backend
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = api_client.query(prompt)
                
                if "error" in response:
                    error_msg = f"❌ Error: {response['error']}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                else:
                    answer = response.get("answer", "No answer generated")
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Display agent steps and sources
                    metadata = {
                        "agent_steps": response.get("agent_steps", []),
                        "query_type": response.get("query_type", "unknown"),
                        "sources": response.get("sources", [])
                    }
                    
                    render_agent_status(metadata["agent_steps"], metadata["query_type"])
                    render_sources(metadata["sources"])
                    
                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "metadata": metadata
                    })