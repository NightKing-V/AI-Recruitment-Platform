import streamlit as st


class App:
    def __init__(self):
        st.title("AI-Powered Recrutment Platform")
        
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(page_title="AI-Powered Recrutment Platform", layout="wide")
    
    def render_header(self):
        """Render the application header"""
        st.title("📚 EduAgent – Multi-Agent Educational Assistant")
        st.markdown("""
        Welcome! This tool helps you:
        - 🧠 Summarize and interact with academic research papers
        - ✍️ Extract study topics from exams and match with your study notes
        """)
        
        st.markdown(f"💬 **Session Chat ID:** `{self.session_manager.get_chat_id()}`")
    
    def render_footer(self):
        """Render the application footer"""
        st.markdown("---")
        st.caption("Created by Valenteno Lenora using LangChain + CrewAI + Mistral + ChromaDB + Streamlit 🧠")
    
    
    
    def run(self):
        """Run the Streamlit application"""
        self.setup_page_config()
        self.render_header()
        
        # Main content goes here
        st.write("This is where the main content of the app will be displayed.")
        
        self.render_footer()