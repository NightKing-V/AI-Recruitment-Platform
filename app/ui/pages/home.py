import streamlit as st


class HomePage:
    def __init__ (self):
        st.session_state.domains = [
                    "Software Engineering", "Data Science", "DevOps",
                    "Machine Learning", "Quality Assurance", "Project Management",
                    "Business Analytics"
                ]
        st.markdown("""
        <style>
            .metric-card {
                background: #fff;
                margin-top: 1rem;
                padding: 1rem 1.25rem;
                border-radius: 10px;
                text-align: center;
                color: #000;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.5s ease;
            }

            .metric-card:hover {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                transform: translateY(-2px);
                color: #fff;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }

        </style>
        """, unsafe_allow_html=True)
        
    def render(self):
        

        with st.container():
            st.subheader("Welcome to AI-Powered Recruitment!")
            
            st.write("An intelligent recruitment platform that helps recruiters efficiently shortlist candidates by matching uploaded resumes against a database of job descriptions using Retrieval-Augmented Generation (RAG). The system utilizes semantic search with Qdrant, and LLMs (via Groq/Mistral) to extract and analyze key resume details, enabling accurate, fast, and scalable candidate-job matching. Deployed on Streamlit Cloud with a clean, recruiter-friendly interface.")
            
            # Feature highlights
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <h3>🎯 Smart Matching</h3>
                    <p>AI-powered job recommendations</p>
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
            
            # if st.session_state.job_descriptions:
            #     st.write(f"✅ {len(st.session_state.job_descriptions)} jobs in database")
            # else:
            #     st.write("📋 No jobs generated yet")
            
            # if st.session_state.resume_data:
            #     st.write(f"✅ Resume uploaded for {st.session_state.resume_data['name']}")
            # else:
            #     st.write("📄 No resume uploaded yet")
            
            # if st.session_state.recommendations:
            #     st.write(f"✅ {len(st.session_state.recommendations)} job recommendations available")
            # else:
            #     st.write("🎯 No recommendations generated yet")
