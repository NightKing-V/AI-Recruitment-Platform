import streamlit as st
from pipelines.RecPipeline import RecommendationsPipeline
from services.FileProcessor import FileProcessor
import time



class RecommendationsPage:
    def __init__ (self):
        self.pipeline = RecommendationsPipeline()
        self.file_processor = FileProcessor()
        st.session_state.recommendations = []
        st.session_state.scores = []
        
        st.markdown("""
        <style> 
            .recommendation-card {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid #764ba2;
                margin-bottom: 1rem;
                color: #000;
            }
        </style>
        """, unsafe_allow_html=True)
            
    def render(self):
        # RECOMMENDATIONS PAGE
        with st.container():
            st.subheader("Job Recommendations")
            
            if st.session_state.resume_data is None:
                st.warning("⚠️ Please upload a resume first to get recommendations.")
                st.info("Go to the 'Resume Upload' page to upload your resume.")
            else:
                # # Display resume summary
                # st.subheader("📄 Your Resume Summary")
                
                resume = st.session_state.resume_data
                
                # col1, col2, col3 = st.columns(3)
                
                # with col1:
                #     st.metric("Name", resume['name'])
                
                # with col2:
                #     st.metric("Skills", len(resume['skills']))
                
                # with col3:
                #     st.metric("Experience", f"{len(resume['experience'])} positions")
                
                # # Show top skills
                # st.write("**Top Skills:**")
                # skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in resume['skills'][:6]])
                # st.markdown(skills_html, unsafe_allow_html=True)

                # st.markdown("---")

                # Slider and download button in one row
                col1, col2 = st.columns([3, 1])
                recommendations = {"success": False, "jobs": [], "scores": [], "error": False}

                with col1:
                    limit = st.slider("Number of job recommendations", min_value=1, max_value=20, value=5, step=1)

                with col2:
                    
                    # --- GET RECOMMENDATIONS BUTTON ---
                    if st.button("🎯 Get Job Recommendations", key="get_recommendations"):
                        with st.spinner("Finding the best job matches..."):
                            progress_bar = st.progress(0)
                            
                            for i in range(100):
                                time.sleep(0.01)
                                progress_bar.progress(i + 1)
                            
                            recommendations = self.pipeline.search_jobs_pipeline(
                                resume_text=resume,
                                limit=limit
                            )
                        
                st.markdown("---")

                           
                if recommendations["success"]:
                    self.display_job_recommendations(jobs=recommendations["jobs"], scores=recommendations["scores"])
                    st.success(f"✅ Found {len(recommendations['jobs'])} job recommendations!")
                    st.session_state.recommendations = recommendations["jobs"]
                    st.session_state.scores = recommendations["scores"]
                    
                elif recommendations["error"]:
                    st.error(f"❌ {recommendations['error']}")
                elif recommendations["success"] is False and not recommendations['error'] is False:
                    st.error("An error occurred while processing your request. Please try again later.")
                elif recommendations['success'] and not recommendations["jobs"]:
                    st.warning("No job recommendations found. Please try again with a different resume.")
                else:
                    None
            

    def display_job_recommendations(self, jobs: list, scores: list):
        """
        Display a list of job recommendations in Streamlit with details and match scores.
        """
        if not jobs:
            st.info("No job recommendations to display.")
            return

        st.subheader(f"📋 Recommended Jobs ({len(jobs)})")

        for i, (job, score) in enumerate(zip(jobs, scores), 1):
            # Convert score to percentage if it's cosine similarity (0–1)
            similarity_pct = score * 100  

            # Recommendation card
            st.markdown(f"""
            <div class="recommendation-card">
                <h4>{i}. {job['job_title']} at {job['company']}</h4>
                <p><strong>Match Score:</strong> {similarity_pct:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View Details - {job['job_title']}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**📍 Location:** {job['location']}")
                    st.write(f"**⏰ Experience:** {job['experience_level']}")
                    st.write(f"**💼 Job Type:** {job['employment_type']}")
                    if job.get('salary_range'):
                        st.write(f"**💰 Salary:** {job['salary_range']}")

                with col2:
                    st.write("**Required Skills:**")
                    skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in job['required_skills']])
                    st.markdown(skills_html, unsafe_allow_html=True)

                st.write("**Description:**")
                st.write(job['summary'])
                
        if jobs and scores:
            pdf_buffer = self.file_processor.download_jobs_as_pdf(
                jobs=jobs,
                scores=scores
            )
            if pdf_buffer:
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_buffer,
                    file_name="job_recommendations.pdf",
                    mime="application/pdf"
                )




