import streamlit as st
import time
from datetime import datetime
from services.JobHandler import jobHandler
from data.mongodb.MongoClient import MongoDBHandler


class JobManagementPage:
    def __init__ (self):
        self.job_handler = jobHandler()
        self.mongo_handler = MongoDBHandler()
            
    def render(self):
        # JOB MANAGEMENT PAGE
        with st.container():
            st.subheader("Job Management")
            
            st.markdown('</br>', unsafe_allow_html=True)
            
            tab1, tab2, tab3 = st.tabs(["Generate Jobs", "Create Job", "View Jobs"])
            
            with tab1:
                st.write("Generate Job Descriptions")
                
                domains = st.session_state.domains
                if not domains:
                    st.session_state.domains = [
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
            jobs_per_domain = st.slider("Jobs per Domain", 1, 10, 2)

            if st.button("🚀 Generate Job Descriptions", key="generate_jobs"):
                if selected_domains:
                    with st.spinner("Generating job descriptions..."):
                        progress_bar = st.progress(0)
                        all_jobs = []
                        total_jobs_to_generate = jobs_per_domain * len(selected_domains)
                        jobs_generated = 0
                        failed_jobs = 0

                        # Max jobs per prompt
                        max_batch_size = 3
                        
                        
                        for domain in selected_domains:
                            domain_jobs_to_generate = jobs_per_domain
                            while domain_jobs_to_generate > 0:
                                batch_size = min(max_batch_size, domain_jobs_to_generate)

                                try:
                                    # Generate batch of jobs for this domain
                                    batch_jobs = self.job_handler.generate_job(
                                        job_num=batch_size,
                                        job_domains=[domain]
                                    )
                                    all_jobs.extend(batch_jobs)
                                except Exception as e:
                                    failed_jobs += batch_size
                                    continue

                                jobs_generated += batch_size
                                domain_jobs_to_generate -= batch_size

                                # Update progress bar
                                progress_bar.progress(int(jobs_generated / total_jobs_to_generate * 100))

                                # Optional: add small sleep to simulate/give UI time
                                time.sleep(0.1)

                        if all_jobs:
                            if failed_jobs > 0:
                                st.error(f"Failed to generate {failed_jobs} jobs.")
                            st.success(f"✅ Generated {jobs_generated} job positions!")
                            st.balloons()
                        else:
                            st.warning("❌ No jobs generated. Please try again.")
                else:
                    st.error("Please select at least one domain")

            
            with tab2:
                st.write("Enter a Job Description")
                
                job_text = st.text_area(
                    "Paste job description here",
                    height=200,
                    placeholder="Enter the job description text here..."
                )
                
                if st.button("📤 Process Job Description", key="process_job"):
                    if job_text.strip():
                        with st.spinner("Processing job description..."):
                            time.sleep(2)
                            
                            job = self.job_handler.create_job(job_text.strip())
                            
                            if job:
                                st.success("✅ Job description processed!")
                                st.balloons()
                            else:
                                st.error("❌ Failed to process job description. Please check the format.")
                    else:
                        st.warning("Please enter a job description")
            
            with tab3:
                st.write("View all Jobs")

                jobs_to_display = self.mongo_handler.get_all_jobs()

                if jobs_to_display:
                    # Search and filter
                    search_term = st.text_input("🔍 Search jobs...", placeholder="Enter job title, company, or skill")

                    filtered_jobs = jobs_to_display
                    if search_term:
                        filtered_jobs = self.mongo_handler.search_jobs(search_term)

                    st.write(f"Showing {len(filtered_jobs)} of {len(jobs_to_display)} jobs")

                    # Display jobs
                    for job in filtered_jobs:

                        created_at = job.get("created_at")
                        if created_at:
                            try:
                                if isinstance(created_at, str):
                                    # If stored as string, try parsing it
                                    created_at = datetime.fromisoformat(created_at)
                                time_diff = datetime.now() - created_at

                                # Format "x days/hours ago"
                                if time_diff.days > 0:
                                    created_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
                                else:
                                    hours = int(time_diff.seconds // 3600)
                                    if hours > 0:
                                        created_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
                                    else:
                                        minutes = int(time_diff.seconds // 60)
                                        created_ago = f"{minutes} min ago"
                            except Exception:
                                created_ago = "Unknown"
                        else:
                            created_ago = "Unknown"

                        with st.expander(f"📋 {job['job_title']} – {created_ago}", expanded=False):

                            col1, col2 = st.columns(2)

                            with col1:
                                st.write(f"**Location:** {job['location']}")
                                st.write(f"**Experience:** {job['experience_level']}")
                                st.write(f"**Employment Type:** {job['employment_type']}")
                                if job.get('salary_range'):
                                    st.write(f"**Salary:** {job['salary_range']}")
                                if created_at:
                                    st.write(f"**Company:** {job['company']}")

                            with col2:
                                st.write("**Required Skills:**")
                                if 'required_skills' in job:
                                    skills_html = " ".join(
                                        [f'<span style="background-color:#e1e1e1; color:#000; padding:3px 8px; border-radius:10px; margin:2px; display:inline-block;">{skill}</span>'
                                        for skill in job['required_skills']]
                                    )
                                    st.markdown(skills_html, unsafe_allow_html=True)

                            st.write("**Description:**")
                            st.write(job['summary'])
                else:
                    st.info("No jobs found. Generate or Create some jobs first!")
