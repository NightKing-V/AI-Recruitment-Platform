import streamlit as st
import time

from pipelines.JobPipeline import JobPipeline


class JobManagementPage:
    def __init__ (self):
        self.pipeline = JobPipeline()
        
    def render(self):
        # JOB MANAGEMENT PAGE
        with st.container():
            st.subheader("Job Management")
            
            st.markdown('</br>', unsafe_allow_html=True)
            
            tab1, tab2, tab3 = st.tabs(["Generate Jobs", "Create Job", "View Jobs"])
            
            with tab1:
                st.write("Generate Job Descriptions")
                
                domains = [
                    "Software Engineering", "Data Science", "DevOps",
                    "Machine Learning", "Quality Assurance", "Project Management",
                    "Business Analytics"
                ]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_domains = st.multiselect(
                        "Select Domains",
                        domains,
                        default=["Software Engineering", "Data Science", "DevOps"]
                    )
                
                with col2:
                    jobs_per_domain = st.slider("Jobs per Domain", 1, 50, 10)
                
                if st.button("🚀 Generate Job Descriptions", key="generate_jobs"):
                    if selected_domains:
                        with st.spinner("Generating job descriptions..."):
                            progress_bar = st.progress(0)
                            
                            # Simulate job generation
                            for i in range(100):
                                time.sleep(0.01)
                                progress_bar.progress(i + 1)
                            
                            jobs = self.pipeline.generation_pipeline(
                                job_num=jobs_per_domain,
                                job_domain=selected_domains
                            )

                            st.success(f"✅ Generated {len(jobs)} job positions!")
                            st.balloons()
                    else:
                        st.error("Please select at least one domain")
            
            with tab2:
                st.subheader("Upload Job Description")
                
                job_text = st.text_area(
                    "Paste job description here",
                    height=200,
                    placeholder="Enter the job description text here..."
                )
                
                if st.button("📤 Process Job Description", key="process_job"):
                    if job_text.strip():
                        with st.spinner("Processing job description..."):
                            time.sleep(2)
                            
                            self.pipeline.creation_pipeline(
                                job_description=job_text.strip()
                            )
                            
                            st.success("✅ Job description processed!")
                            st.balloons()
                    else:
                        st.warning("Please enter a job description")
            
            with tab3:
                st.subheader("View Stored Jobs")
                
                jobs_to_display = self.mongo_handler.get_all_jobs()
                
                if jobs_to_display:
                    # Search and filter
                    search_term = st.text_input("🔍 Search jobs...", placeholder="Enter job title, company, or skill")
                    
                    # Apply filters
                    filtered_jobs = jobs_to_display
                    if search_term:
                        filtered_jobs = self.mongo_handler.search_jobs(search_term)
                    
                    
                    st.write(f"Showing {len(filtered_jobs)} of {len(jobs_to_display)} jobs")
                    
                    # Display jobs
                    for job in filtered_jobs:
                        with st.expander(f"📋 {job['title']} at {job['company']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Location:** {job['location']}")
                                st.write(f"**Experience:** {job['experience_level']}")
                                st.write(f"**Job Type:** {job['job_type']}")
                                st.write(f"**Department:** {job['department']}")
                                if job.get('salary_range'):
                                    st.write(f"**Salary:** {job['salary_range']}")
                            
                            with col2:
                                st.write("**Required Skills:**")
                                skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in job['required_skills']])
                                st.markdown(skills_html, unsafe_allow_html=True)
                            
                            st.write("**Description:**")
                            st.write(job['description'])
                else:
                    st.info("No jobs found. Generate or Create some jobs first!")
