import streamlit as st


class Header:
    def __init__(self):
        self.setup_header()
        
    def setup_header(self):
        # Main Header
        st.markdown("""
        <div class="main-header">
            <h1>🎯 AI-Powered Recruitment Platform</h1>
            <p>Find the perfect job match using advanced AI and RAG technology</p>
        </div>
        """, unsafe_allow_html=True)
