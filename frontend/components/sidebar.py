import streamlit as st
from utils.api_client import api_client

def render_sidebar():
    """Render the sidebar with upload options"""
    
    with st.sidebar:
        st.title("📁 Document Manager")
        
        # File upload only
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=["pdf", "txt", "docx"],
            help="Upload PDF, TXT, or DOCX files"
        )
        
        if uploaded_file is not None:
            if st.button("📤 Upload", use_container_width=True):
                with st.spinner("Uploading..."):
                    result = api_client.upload_file(uploaded_file)
                    
                    if "error" in result:
                        st.error(f"Error: {result['error']}")
                    else:
                        st.success(f"✅ Uploaded: {result['filename']}")
                        st.info(f"📊 Chunks: {result['chunks']}")
                        st.rerun()
        
        st.divider()
        
        # Document list
        st.subheader("📚 Uploaded Documents")
        
        docs_info = api_client.get_documents()
        
        if "error" in docs_info:
            st.error("Could not fetch documents")
        else:
            st.metric("Total Documents", docs_info.get("total_documents", 0))
            st.metric("Total Chunks", docs_info.get("total_chunks", 0))
            
            documents = docs_info.get("documents", [])
            if documents:
                for doc in documents:
                    st.text(f"📄 {doc}")
            else:
                st.info("No documents uploaded yet")
        
        st.divider()
        
        # Reset button
        if st.button("🗑️ Reset Database", use_container_width=True, type="secondary"):
            if st.session_state.get("confirm_reset", False):
                with st.spinner("Resetting..."):
                    result = api_client.reset_database()
                    if "error" in result:
                        st.error(f"Error: {result['error']}")
                    else:
                        st.success("Database reset successfully!")
                        st.session_state.confirm_reset = False
                        st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("Click again to confirm reset")