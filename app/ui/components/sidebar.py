import streamlit as st


class Sidebar:
    # def __init__(self):
    #     self.setup_sidebar()
            
    def setup_sidebar(self):
        st.sidebar.markdown("""
        <style>
                
            /* 🎯 Bounce Animation */
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }

            .animated-icon {
                font-size: 6rem;
                text-align: center;
                animation: bounce 1s infinite;
            }

            /* Fade-in Quick Stats */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>

        <div class="animated-icon">🎯</div>
        """, unsafe_allow_html=True)

        st.sidebar.markdown("---")
        st.sidebar.subheader("Upload Your Resume")

            # st.metric("Total Jobs", len(st.session_state.job_descriptions) if st.session_state.job_descriptions else len(mock_jobs))
            # st.metric("Resume Status", "✅ Uploaded" if st.session_state.resume_data else "❌ Not Uploaded")