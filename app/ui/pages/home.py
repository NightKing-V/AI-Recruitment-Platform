import streamlit as st


class HomePage:
    def __init__ (self):
        self.setup_home_page()
        
    def setup_home_page(self):

        with st.container():
            st.header("Welcome to AI-Powered Recruitment")
            
            # Feature highlights
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <h3>🎯 Smart Matching</h3>
                    <p>AI-powered job recommendations using RAG technology</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <h3>📄 Resume Analysis</h3>
                    <p>Automated extraction of skills and experience</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <h3>📋 Job Generation</h3>
                    <p>Create realistic job descriptions across domains</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # How it works
            st.subheader("How It Works")
            
            steps_col1, steps_col2, steps_col3, steps_col4 = st.columns(4)
            
            with steps_col1:
                st.markdown("**1. Generate Jobs**")
                st.write("Create or upload job descriptions")
            
            with steps_col2:
                st.markdown("**2. Upload Resume**")
                st.write("Upload your resume for analysis")
            
            with steps_col3:
                st.markdown("**3. AI Processing**")
                st.write("Our AI analyzes and matches")
            
            with steps_col4:
                st.markdown("**4. Get Matches**")
                st.write("Receive personalized recommendations")
            
            # Recent activity
            st.markdown("---")
            st.subheader("Recent Activity")
            
            if st.session_state.job_descriptions:
                st.write(f"✅ {len(st.session_state.job_descriptions)} jobs in database")
            else:
                st.write("📋 No jobs generated yet")
            
            if st.session_state.resume_data:
                st.write(f"✅ Resume uploaded for {st.session_state.resume_data['name']}")
            else:
                st.write("📄 No resume uploaded yet")
            
            if st.session_state.recommendations:
                st.write(f"✅ {len(st.session_state.recommendations)} job recommendations available")
            else:
                st.write("🎯 No recommendations generated yet")
