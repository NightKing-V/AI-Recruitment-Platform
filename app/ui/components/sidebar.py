import streamlit as st


class Sidebar:
    def __init__(self):
        self.setup_session_state()
        self.setup_sidebar()
        
    def setup_sidebar(self):
        with st.sidebar:
            st.markdown("### 🎯 AI Recruitment Platform")
            st.markdown("---")
            
            pages = {
                "🏠 Home": "home",
                "📋 Job Management": "job_management",
                "📄 Resume Upload": "resume_upload",
                "🎯 Job Recommendations": "recommendations",
                "📊 Analytics": "analytics"
            }
            
            selected_page = st.selectbox("Navigate", list(pages.keys()))
            current_page = pages[selected_page]
            
            st.markdown("---")
            st.markdown("### Quick Stats")
            st.metric("Total Jobs", len(st.session_state.job_descriptions) if st.session_state.job_descriptions else len(mock_jobs))
            st.metric("Resume Status", "✅ Uploaded" if st.session_state.resume_data else "❌ Not Uploaded")
            st.metric("Recommendations", len(st.session_state.recommendations))