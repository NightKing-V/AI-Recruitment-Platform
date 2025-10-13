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
                
                resume = st.session_state.resume_data
                
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

                           
                success_flag = recommendations.get("success", False)
                error_message = recommendations.get("error") # Defaults to None if not found
                jobs = recommendations.get("jobs", [])
                scores = recommendations.get("scores", [])

                # Now, we use these safe variables in our logic
                if error_message:
                    # If there's an explicit error message, always show it first.
                    st.error(f"❌ {error_message}")

                elif success_flag:
                    # If the call was a success, we then check if we actually got any jobs.
                    if jobs:
                        # SUCCESS and JOBS FOUND
                        self.display_job_recommendations(jobs=jobs, scores=scores)
                        st.success(f"✅ Found {len(jobs)} job recommendations!")
                        st.session_state.recommendations = jobs
                        st.session_state.scores = scores
                    else:
                        # SUCCESS but NO JOBS FOUND
                        st.warning("No job recommendations found. Please try again with a different resume or criteria.")
                        
                else:
                    # CATCH-ALL: If not an error and not a success, something unexpected happened.
                    st.error("An unknown error occurred. Please try again later.")

            

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




