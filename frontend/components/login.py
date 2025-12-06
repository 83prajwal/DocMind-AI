import streamlit as st

def check_login(username, password):
    """Check if credentials are valid"""
    VALID_USERNAME = "admin@documind.ai"
    VALID_PASSWORD = "admin@123"
    
    return username == VALID_USERNAME and password == VALID_PASSWORD

def render_login():
    """Render the login page with split layout"""
    
    # Custom CSS for split login page
    st.markdown("""
    <style>
        /* Hide sidebar on login page */
        [data-testid="stSidebar"] {
            display: none;
        }
        
        /* Main container styling */
        .main .block-container {
            padding-top: 3rem;
            max-width: 100%;
        }
        
        /* Header styling */
        .login-main-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .login-title {
            font-size: 3.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .login-subtitle {
            color: #555;
            font-size: 1.3rem;
            font-weight: 500;
            margin-bottom: 0.3rem;
        }
        
        .login-description {
            color: #888;
            font-size: 1rem;
        }
        
        /* Left side - Features */
        .features-container {
            padding: 2rem;
        }
        
        .feature-box {
            background: linear-gradient(135deg, #667eea08 0%, #764ba208 100%);
            border-radius: 12px;
            padding: 2rem;
            border-left: 4px solid #667eea;
        }
        
        .feature-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 1.5rem;
            font-size: 1.3rem;
        }
        
        .feature-item {
            color: #555;
            margin: 1rem 0;
            padding-left: 0.5rem;
            font-size: 1.05rem;
            line-height: 1.6;
        }
        
        /* Right side - Sign In */
        .signin-container {
            padding: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .signin-box {
            width: 100%;
            max-width: 450px;
        }
        
        .signin-header {
            font-size: 1.8rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 1.5rem;
        }
        
        /* Form styling */
        .stTextInput > label {
            font-weight: 500;
            color: #555;
            font-size: 0.95rem;
        }
        
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1.5px solid #e0e0e0;
            padding: 0.75rem;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.15);
        }
        
        .stButton > button {
            border-radius: 8px;
            height: 3.2rem;
            font-size: 1.1rem;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            width: 100%;
            margin-top: 1rem;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #5568d3 0%, #653a8b 100%);
            border: none;
        }
        
        /* Footer styling */
        .login-footer {
            text-align: center;
            color: #999;
            font-size: 0.9rem;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e0e0e0;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-size: 0.95rem;
            color: #667eea;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="login-main-header">
        <div class="login-title">💬 DocuMind AI</div>
        <div class="login-subtitle">Multi-Agent Document Intelligence</div>
        <div class="login-description">Transform your documents into intelligent conversations with AI-powered agents</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Split layout - Left and Right columns
    left_col, right_col = st.columns([1, 1], gap="large")
    
    # LEFT SIDE - Features
    with left_col:
        st.markdown("""
        <div class="features-container">
            <div class="feature-box">
                <div class="feature-title">✨ What You Can Do</div>
                <div class="feature-item">📄 Upload PDF, TXT, and DOCX documents</div>
                <div class="feature-item">💬 Ask intelligent questions about your content</div>
                <div class="feature-item">🎯 Get AI-powered answers with sources</div>
                <div class="feature-item">🔍 Smart document analysis and insights</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # RIGHT SIDE - Sign In Form
    with right_col:
        st.markdown('<div class="signin-container">', unsafe_allow_html=True)
        st.markdown('<div class="signin-box">', unsafe_allow_html=True)
        
        st.markdown('<div class="signin-header">🔐 Sign In</div>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "Email Address",
                placeholder="admin@documind.ai",
                key="username_input"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="password_input"
            )
            
            submit = st.form_submit_button("Sign In")
            
            if submit:
                if check_login(username, password):
                    st.session_state.authenticated = True
                    st.session_state.user_email = username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        # Demo credentials hint
        with st.expander("💡 Demo Credentials"):
            st.code("Email: admin@documind.ai\nPassword: admin@123", language=None)
        
        # Footer
        st.markdown("""
        <div class="login-footer">
            🔒 Secure • 🚀 Fast • 🧠 Intelligent
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)