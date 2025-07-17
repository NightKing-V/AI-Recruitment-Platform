import streamlit as st




class RecommendationsPage:
    # def __init__ (self):
    #     self.setup_recommendations_page()
        
    def setup_recommendations_page(self):
        # RECOMMENDATIONS PAGE
        with st.container():
            st.header("🎯 Job Recommendations")
            
            if None is None:
                st.warning("⚠️ Please upload a resume first to get recommendations.")
                st.info("Go to the 'Resume Upload' page to upload your resume.")
            else:
                # Display resume summary
                st.subheader("📄 Your Resume Summary")
                
                # resume = st.session_state.resume_data
                
                col1, col2, col3 = st.columns(3)
                
                # with col1:
                #     st.metric("Name", resume['name'])
                
                # with col2:
                #     st.metric("Skills", len(resume['skills']))
                
                # with col3:
                #     st.metric("Experience", f"{len(resume['experience'])} positions")
                
                # Show top skills
                st.write("**Top Skills:**")
                skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in resume['skills'][:6]])
                st.markdown(skills_html, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Get recommendations
                if st.button("🎯 Get Job Recommendations", key="get_recommendations"):
                    with st.spinner("Finding the best job matches..."):
                        progress_bar = st.progress(0)
                        
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        # # Simulate recommendations with mock data
                        # recommendations = [
                        #     {"job": mock_jobs[0], "similarity": 0.89},
                        #     {"job": mock_jobs[2], "similarity": 0.76},
                        #     {"job": mock_jobs[1], "similarity": 0.65}
                        # ]
                        
                        # st.session_state.recommendations = recommendations
                        
                        # st.success(f"✅ Found {len(recommendations)} job recommendations!")
                
                # # Display recommendations
                # if st.session_state.recommendations:
                #     st.subheader(f"📋 Recommended Jobs ({len(st.session_state.recommendations)})")
                    
                #     for i, rec in enumerate(st.session_state.recommendations, 1):
                #         job = rec['job']
                #         similarity = rec['similarity']
                        
                #         # Create recommendation card
                #         st.markdown(f"""
                #         <div class="recommendation-card">
                #             <h4>{i}. {job['title']} at {job['company']}</h4>
                #             <p><strong>Match Score:</strong> {similarity:.0%}</p>
                #         </div>
                #         """, unsafe_allow_html=True)
                        
                #         with st.expander(f"View Details - {job['title']}"):
                #             col1, col2 = st.columns(2)
                            
                #             with col1:
                #                 st.write(f"**📍 Location:** {job['location']}")
                #                 st.write(f"**⏰ Experience:** {job['experience_level']}")
                #                 st.write(f"**💼 Job Type:** {job['job_type']}")
                #                 st.write(f"**🏢 Department:** {job['department']}")
                #                 if job.get('salary_range'):
                #                     st.write(f"**💰 Salary:** {job['salary_range']}")
                            
                #             with col2:
                #                 st.write("**Required Skills:**")
                #                 skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in job['required_skills']])
                #                 st.markdown(skills_html, unsafe_allow_html=True)
                            
                #             st.write("**Description:**")
                #             st.write(job['description'])
                            
                #             # Match analysis
                #             st.write("**Why this matches:**")
                #             matching_skills = set(resume['skills']) & set(job['required_skills'])
                #             if matching_skills:
                #                 st.write(f"• You have {len(matching_skills)} matching skills: {', '.join(matching_skills)}")
                            
                #             st.write(f"• Experience level alignment: {job['experience_level']}")
                    
                    # # Download recommendations
                    # st.markdown("---")
                    
                    # if st.button("📥 Download Recommendations as CSV", key="download_csv"):
                    #     # Create CSV data
                    #     csv_data = []
                    #     for rec in st.session_state.recommendations:
                    #         job = rec['job']
                    #         csv_data.append({
                    #             'Job Title': job['title'],
                    #             'Company': job['company'],
                    #             'Location': job['location'],
                    #             'Experience Level': job['experience_level'],
                    #             'Job Type': job['job_type'],
                    #             'Department': job['department'],
                    #             'Match Score': f"{rec['similarity']:.2%}",
                    #             'Required Skills': ', '.join(job['required_skills']),
                    #             'Salary Range': job.get('salary_range', 'Not specified')
                    #         })
                        
                    #     df = pd.DataFrame(csv_data)
                    #     csv = df.to_csv(index=False)
                        
                        st.download_button(
                            label="Download CSV",
                            data=None,
                            file_name=f"job_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
