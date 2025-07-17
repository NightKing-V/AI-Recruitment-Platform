import streamlit as st


class Header:
    # def __init__(self):
    #     self.setup_header()
        
    def render(self):
        # Main Header
        st.markdown("""
        <style>
        .main-header {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 10px;
                color: white;
                margin-bottom: 1.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="main-header">
            <h2>🎯 AI-Powered Recruitment Platform</h2>
        </div>
        """, unsafe_allow_html=True)
