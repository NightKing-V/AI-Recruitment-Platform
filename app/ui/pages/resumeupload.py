import streamlit as st 



class ResumeUploadPage:
    def __init__(self):
        self.setup_resume_upload_page()
        
    def setup_resume_upload_page(self):
        # RESUME UPLOAD PAGE
        with st.container():
            st.header("📄 Resume Upload & Analysis")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Upload Resume")
                
                uploaded_file = st.file_uploader(
                    "Choose a resume file",
                    type=['pdf', 'docx', 'txt'],
                    help="Supported formats: PDF, DOCX, TXT"
                )
                
                if uploaded_file is not None:
                    st.success(f"✅ File uploaded: {uploaded_file.name}")
                    
                    if st.button("🔍 Analyze Resume", key="analyze_resume"):
                        with st.spinner("Analyzing resume..."):
                            progress_bar = st.progress(0)
                            
                            for i in range(100):
                                time.sleep(0.02)
                                progress_bar.progress(i + 1)
                            
                            # Use mock data for demonstration
                            st.session_state.resume_data = mock_resume
                            
                            st.success("✅ Resume analyzed successfully!")
                            st.balloons()
            
            with col2:
                if st.session_state.resume_data:
                    st.subheader("Analysis Results")
                    
                    resume = st.session_state.resume_data
                    
                    # Personal Info
                    st.markdown("**Personal Information**")
                    st.write(f"Name: {resume['name']}")
                    st.write(f"Email: {resume['email']}")
                    st.write(f"Phone: {resume['phone']}")
                    
                    # Skills
                    st.markdown("**Skills**")
                    skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in resume['skills']])
                    st.markdown(skills_html, unsafe_allow_html=True)
                    
                    # Experience
                    st.markdown("**Experience**")
                    for exp in resume['experience']:
                        st.write(f"• **{exp['title']}** at {exp['company']} ({exp['duration']})")
                    
                    # Education
                    st.markdown("**Education**")
                    for edu in resume['education']:
                        st.write(f"• {edu['degree']} from {edu['institution']} ({edu['year']})")
                    
                    # Summary
                    st.markdown("**Summary**")
                    st.write(resume['summary'])
                else:
                    st.info("Upload a resume to see analysis results")
import streamlit as st