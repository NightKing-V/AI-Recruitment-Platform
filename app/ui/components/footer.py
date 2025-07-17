import streamlit as st


class Footer:
    # def __init__(self):
    #     self.setup_footer()
        
    def render(self):
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>🎯 <strong>AI-Powered Recruitment Platform</strong></p>
            <p>Built with Streamlit • Powered by OpenAI & RAG Technology</p>
            <p>© 2025 - Valenteno Lenora</p>
        </div>
        """, unsafe_allow_html=True)