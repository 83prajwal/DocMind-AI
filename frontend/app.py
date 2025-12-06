import streamlit as st
from config import config
from components.sidebar import render_sidebar
from components.chat import render_chat
from components.login import render_login

# Page config
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for main app
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Profile button styling */
    div[data-testid="column"]:last-child button {
        background: white;
        border: 1.5px solid #e0e0e0;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        padding: 0;
        font-size: 1.2rem;
    }
    
    div[data-testid="column"]:last-child button:hover {
        border-color: #667eea;
        background: #f8f9ff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def logout():
    """Handle logout"""
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.rerun()

def main():
    # Check authentication
    if not st.session_state.authenticated:
        render_login()
        return
    
    # Top bar with user profile
    user_email = st.session_state.get('user_email', 'User')
    
    # Create top bar layout
    top_col1, top_col2 = st.columns([11, 1])
    
    with top_col2:
        # Use selectbox styled as profile menu
        with st.popover("👤", use_container_width=False):
            st.markdown(f"**Signed in as**")
            st.markdown(f"`{user_email}`")
            st.divider()
            if st.button("🚪 Log out", use_container_width=True, type="primary"):
                logout()
    
    # Header
    st.markdown(f'<div class="main-header">{config.APP_ICON} {config.APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Multi-Agent Document Intelligence System</div>', unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Main chat area
    st.markdown("### 💬 Chat with Your Documents")
    st.markdown("Upload documents and ask questions to get intelligent answers powered by AI agents.")
    
    render_chat()

if __name__ == "__main__":
    main()