import streamlit as st
import time


class Sidebar:
    def __init__(self):
        # Initialize session state for resume data
        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = None
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None
        
        st.sidebar.markdown("""
        <style>
            /* Reduce sidebar top padding */
            .css-1d391kg {
                padding-top: 0.5rem !important;
            }
            
            /* 🎯 Bounce Animation */
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }

            .animated-icon {
                font-size: 5rem;
                text-align: center;
                animation: bounce 1s infinite;
                margin: 0.5rem 0;
            }

            /* Fade-in Quick Stats */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .upload-section {
                background: #f8f9fa;
                padding: 0.8rem;
                border-radius: 8px;
                margin: 0.5rem 0;
                border: 1px solid #e9ecef;
            }
            
            .resume-info {
                background: #e8f5e8;
                padding: 0.5rem;
                border-radius: 6px;
                margin: 0.3rem 0;
                border-left: 4px solid #28a745;
            }
            
            .skill-tag-sidebar {
                background: #e3f2fd;
                color: #1976d2;
                padding: 0.2rem 0.4rem;
                border-radius: 4px;
                font-size: 0.7rem;
                margin: 0.1rem;
                display: inline-block;
            }
            
            /* Reduce spacing between sections */
            .css-1lcbmhc {
                margin-bottom: 0.5rem !important;
            }
        </style>
        """, unsafe_allow_html=True)
            
    def render(self):
        
        st.sidebar.markdown("""<div class="animated-icon">🎯</div>
        """, unsafe_allow_html=True)
        st.sidebar.markdown('<hr style="margin: 0.5rem 0;">', unsafe_allow_html=True)
        
        # Resume Upload Section
        st.sidebar.subheader("📄 Upload Your Resume")
        
        with st.sidebar.container():
            uploaded_file = st.file_uploader(
                "Choose a resume file",
                type=['pdf', 'docx', 'txt'],
                help="Supported formats: PDF, DOCX, TXT",
                key="sidebar_file_upload"
            )
        
        
        st.sidebar.markdown('<hr style="margin: 0.5rem 0;">', unsafe_allow_html=True)
        
        # Resume Status Section
        st.sidebar.subheader("📊 Resume Status")
        
        if st.session_state.resume_data:
            resume = st.session_state.resume_data
            
            # Quick info display
            st.sidebar.markdown(f"""
            <div class="resume-info">
                <strong>👤 {resume['name']}</strong><br>
                <small>📧 {resume['email']}</small><br>
                <small>📞 {resume['phone']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Skills preview
            st.sidebar.write("**🔧 Top Skills:**")
            top_skills = resume['skills'][:4]  # Show first 4 skills
            skills_html = " ".join([f'<span class="skill-tag-sidebar">{skill}</span>' for skill in top_skills])
            if len(resume['skills']) > 4:
                skills_html += f'<span class="skill-tag-sidebar">+{len(resume["skills"]) - 4} more</span>'
            st.sidebar.markdown(skills_html, unsafe_allow_html=True)
            
            # Experience count
            st.sidebar.metric("💼 Experience", f"{len(resume['experience'])} positions")
            
            # Education count
            st.sidebar.metric("🎓 Education", f"{len(resume['education'])} degrees")
            
            # Clear resume button
            if st.sidebar.button("🗑️ Clear Resume", key="clear_resume"):
                st.session_state.resume_data = None
                st.session_state.uploaded_file = None
                st.sidebar.success("Resume cleared!")
                st.rerun()
                
        else:
            st.sidebar.info("No resume uploaded yet")
            st.sidebar.write("Upload a resume to see analysis and get job recommendations.")
        
        
        st.sidebar.markdown('<hr style="margin: 0.5rem 0;">', unsafe_allow_html=True)
        
        # Quick Stats Section
        st.sidebar.subheader("📈 Quick Stats")
        
        # You can add more metrics here based on your session state
        st.sidebar.metric("Total Jobs", "3")  # Replace with actual count
        
        if st.session_state.resume_data:
            st.sidebar.metric("Skills Count", len(st.session_state.resume_data['skills']))