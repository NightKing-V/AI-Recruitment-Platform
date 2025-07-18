import streamlit as st

from services.FileProcessor import FileProcessor
from llm.LLMProcessor import LLMProcessor
from data.mongodb.MongoClient import MongoDBHandler



class Sidebar:
    def __init__(self):
        self.llm_processor = LLMProcessor()
        self.mongo_handler = MongoDBHandler()
        self.file_processor = FileProcessor()
        
        # Initialize session state for resume data
        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = None
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None
        if 'processing' not in st.session_state:
            st.session_state.processing = False
        
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
            
            /* Processing animation */
            .processing {
                color: #ff6b6b;
                animation: pulse 1s infinite;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
        </style>
        """, unsafe_allow_html=True)
    
    def process_uploaded_file(self, uploaded_file):
        """Process the uploaded file and extract structured data"""
        if uploaded_file is None:
            return
        
        # Check if this is a new file
        if (st.session_state.uploaded_file is None or 
            st.session_state.uploaded_file.name != uploaded_file.name):
            
            st.session_state.processing = True
            st.sidebar.info("🔄 Processing your resume...")
            
            # Extract text from the file
            with st.spinner("Extracting text from file..."):
                resume_text = self.file_processor.process_file(uploaded_file)
            
            if resume_text:
                # Send to LLM for structuring
                with st.spinner("Analyzing resume with AI..."):
                    structured_data = LLMProcessor.structure_resume_data(resume_text)
                
                if structured_data:
                    st.session_state.resume_data = structured_data
                    st.session_state.uploaded_file = uploaded_file
                    st.sidebar.success("✅ Resume processed successfully!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Failed to process resume")
            else:
                st.sidebar.error("❌ Failed to extract text from file")
            
            st.session_state.processing = False
            
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
            
            # Process the file if uploaded
            if uploaded_file is not None:
                self.process_uploaded_file(uploaded_file)
        
        # Show processing status
        if st.session_state.processing:
            st.sidebar.markdown('<div class="processing">🔄 Processing...</div>', unsafe_allow_html=True)
        
        st.sidebar.markdown('<hr style="margin: 0.5rem 0;">', unsafe_allow_html=True)
        
        # Resume Status Section
        st.sidebar.subheader("📊 Resume Status")
        
        if st.session_state.resume_data:
            resume = st.session_state.resume_data
            
            # Quick info display
            st.sidebar.markdown(f"""
            <div class="resume-info">
                <strong>👤 {resume.get('name', 'Unknown')}</strong><br>
                <small>📧 {resume.get('email', 'No email')}</small><br>
                <small>📞 {resume.get('phone', 'No phone')}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Skills preview
            if resume.get('skills'):
                st.sidebar.write("**🔧 Top Skills:**")
                top_skills = resume['skills'][:4]  # Show first 4 skills
                skills_html = " ".join([f'<span class="skill-tag-sidebar">{skill}</span>' for skill in top_skills])
                if len(resume['skills']) > 4:
                    skills_html += f'<span class="skill-tag-sidebar">+{len(resume["skills"]) - 4} more</span>'
                st.sidebar.markdown(skills_html, unsafe_allow_html=True)
            
            # Experience count
            experience_count = len(resume.get('experience', []))
            st.sidebar.metric("💼 Experience", f"{experience_count} positions")
            
            # Education count
            education_count = len(resume.get('education', []))
            st.sidebar.metric("🎓 Education", f"{education_count} degrees")
            
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
        
        job_count = self.mongo_handler.get_jobs_count()
        if job_count is None:
            job_count = 0
        # You can add more metrics here based on your session state
        st.sidebar.metric("Total Jobs", job_count)  # Replace with actual count
        
        if st.session_state.resume_data:
            skills_count = len(st.session_state.resume_data.get('skills', []))
            st.sidebar.metric("Skills Count", skills_count)