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
            /* Improve overall sidebar spacing */
            .css-1d391kg {
                padding-top: 1rem !important;
                padding-bottom: 2rem !important;
            }
            
            /* 🎯 Bounce Animation with better spacing */
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-8px); }
            }

            .animated-icon {
                font-size: 4rem;
                text-align: center;
                animation: bounce 2s ease-in-out infinite;
                margin: 1.5rem 0 2rem 0;
                padding: 0.5rem;
            }

            /* Fade-in animation */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(15px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Section headers with better spacing */
            .sidebar-section {
                margin: 1rem 0 1.5rem 0;
                animation: fadeIn 0.6s ease-out;
            }
            
            .sidebar-section h3 {
                margin-bottom: 1rem !important;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #f0f2f6;
            }
            
            /* Upload section with enhanced spacing */
            .upload-section {
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 12px;
                margin: 1rem 0 2rem 0;
                border: 1px solid #e9ecef;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            /* Resume info with better padding */
            .resume-info {
                background: #e8f5e8;
                padding: 1rem 1.2rem;
                border-radius: 10px;
                margin: 1rem 0 1.5rem 0;
                border-left: 5px solid #764ba2;
                color: #000;
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            }
            
            /* Skills section spacing */
            .skills-section {
                margin: 0.5rem 0;
                padding: 0.3rem 0;
            }
            
            .skill-tag-sidebar {
                background: #e3f2fd;
                color: #1976d2;
                padding: 0.4rem 0.8rem;
                border-radius: 6px;
                font-size: 0.75rem;
                margin: 0.3rem 0.2rem;
                display: inline-block;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                transition: transform 0.2s ease;
            }
            
            .skill-tag-sidebar:hover {
                transform: translateY(-1px);
            }
            
            /* Metrics section spacing */
            .metrics-section {
                background: #f8f9fa;
                padding: 0.8rem;
                border-radius: 10px;
                margin: 1.5rem 0;
                border: 1px solid #e9ecef;
            }
            
            /* Button spacing and styling */
            .sidebar-button {
                margin: 1.5rem 0 !important;
                width: 100% !important;
            }
            
            /* Divider spacing */
            .sidebar-divider {
                margin: 1.5rem 0 !important;
                border: none !important;
                height: 2px !important;
                background: linear-gradient(90deg, #764ba2, #667eea) !important;
                border-radius: 2px !important;
            }
            
            /* Processing animation with spacing */
            .processing {
                color: #ff6b6b;
                animation: pulse 1.5s ease-in-out infinite;
                padding: 1rem;
                text-align: center;
                margin: 1rem 0;
                background: #fff5f5;
                border-radius: 8px;
                border: 1px solid #fed7d7;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.6; }
                100% { opacity: 1; }
            }
            
            /* Info box spacing */
            .info-box {
                background: #f0f8ff;
                padding: 1.2rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 4px solid #4a90e2;
                color: #000;
                line-height: 1.6;
            }
            
            /* File uploader spacing */
            .stFileUploader {
                margin: 1rem 0 !important;
            }
            
            /* Streamlit metric styling */
            div[data-testid="metric-container"] {
                background: white;
                border: 1px solid #e1e5e9;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.8rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
                # st.write(resume_text)
            
            if resume_text:
                # Send to LLM for structuring
                with st.spinner("Analyzing resume with AI..."):
                    structured_data = self.llm_processor.structure_resume_data(resume_text=resume_text)
                
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
        
        # Animated header icon
        st.sidebar.markdown("""<div class="animated-icon">🎯</div>""", unsafe_allow_html=True)
        
        # Stylish divider
        st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Resume Upload Section
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.subheader("📄 Upload Your Resume")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
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
            st.sidebar.markdown('<div class="processing">🔄 Processing your resume...</div>', unsafe_allow_html=True)
        
        # Stylish divider
        st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Resume Status Section
        st.sidebar.subheader("📊 Resume Status")
        
        if st.session_state.resume_data:
            resume = st.session_state.resume_data
            
            # Quick info display with better spacing
            st.sidebar.markdown(f"""
            <div class="resume-info">
                <strong>👤 {resume.get('name', 'Unknown')}</strong><br>
                <small style="opacity: 0.8;">Resume successfully processed</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Skills preview with enhanced layout
            if resume.get('skills'):
                st.sidebar.markdown('<div class="skills-section">', unsafe_allow_html=True)
                st.sidebar.write("**🔧 Top Skills:**")
                top_skills = resume['skills'][:4]  # Show first 4 skills
                skills_html = " ".join([f'<span class="skill-tag-sidebar">{skill}</span>' for skill in top_skills])
                if len(resume['skills']) > 4:
                    skills_html += f'<span class="skill-tag-sidebar" style="background: #fff3cd; color: #856404;">+{len(resume["skills"]) - 4} more</span>'
                st.sidebar.markdown(skills_html, unsafe_allow_html=True)
                st.sidebar.markdown('</div>', unsafe_allow_html=True)
            
            # Add some spacing before the button
            st.sidebar.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
            
            # Clear resume button with better styling
            if st.sidebar.button("🗑️ Clear Resume", key="clear_resume", type="secondary"):
                st.session_state.resume_data = None
                st.session_state.uploaded_file = None
                st.sidebar.success("Resume cleared!")
                self.__init__()
                
        else:
            st.sidebar.markdown("""
            <div class="info-box">
                <strong>📋 No resume uploaded yet</strong><br>
                Upload a resume to see detailed analysis and get personalized job recommendations.
            </div>
            """, unsafe_allow_html=True)
        
        # Another stylish divider
        st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Quick Stats Section with enhanced styling
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.subheader("📈 Quick Stats")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        
        job_count = self.mongo_handler.get_jobs_count()
        if job_count is None:
            job_count = 0
        
        st.sidebar.metric("Total Jobs", job_count, help="Total number of jobs in the database")
        
        if st.session_state.resume_data:
            skills_count = len(st.session_state.resume_data.get('skills', []))
            st.sidebar.metric("Skills Count", skills_count, help="Number of skills detected in your resume")
            
            # Add experience info if available
            experience = st.session_state.resume_data.get('experience', [])
            if experience:
                st.sidebar.metric("Work Experience", f"{len(experience)} jobs", help="Number of work experiences in your resume")
        
        # Add some bottom spacing
        st.sidebar.markdown('<div style="margin-bottom: 3rem;"></div>', unsafe_allow_html=True)