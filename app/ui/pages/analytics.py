import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class AnalyticsPage:
    # def __init__(self):
    #     self.setup_analytics_page()
        
    def render(self):
        # ANALYTICS PAGE
        with st.container():
            st.header("📊 Analytics Dashboard")
            
            # Use mock data for demonstration
            jobs_data = st.session_state.job_descriptions
            
            if not jobs_data:
                st.info("No data available for analytics. Please generate some job descriptions first.")
            else:
                # Convert to DataFrame
                df = pd.DataFrame(jobs_data)
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Jobs", len(df))
                
                with col2:
                    st.metric("Companies", df['company'].nunique())
                
                with col3:
                    st.metric("Locations", df['location'].nunique())
                
                with col4:
                    st.metric("Departments", df['department'].nunique())
                
                st.markdown("---")
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Jobs by Department")
                    dept_counts = df['department'].value_counts()
                    fig_dept = px.pie(
                        values=dept_counts.values,
                        names=dept_counts.index,
                        title="Distribution of Jobs by Department"
                    )
                    st.plotly_chart(fig_dept, use_container_width=True)
                
                with col2:
                    st.subheader("Jobs by Experience Level")
                    exp_counts = df['experience_level'].value_counts()
                    fig_exp = px.bar(
                        x=exp_counts.index,
                        y=exp_counts.values,
                        title="Jobs by Experience Level"
                    )
                    st.plotly_chart(fig_exp, use_container_width=True)
                
                # Location analysis
                st.subheader("Top Locations")
                location_counts = df['location'].value_counts().head(10)
                fig_loc = px.bar(
                    x=location_counts.values,
                    y=location_counts.index,
                    orientation='h',
                    title="Top 10 Job Locations"
                )
                st.plotly_chart(fig_loc, use_container_width=True)
                
                # Skills analysis
                st.subheader("Most In-Demand Skills")
                all_skills = []
                for job in jobs_data:
                    all_skills.extend(job['required_skills'])
                
                skills_df = pd.DataFrame(all_skills, columns=['skill'])
                skill_counts = skills_df['skill'].value_counts().head(10)
                
                fig_skills = px.bar(
                    x=skill_counts.values,
                    y=skill_counts.index,
                    orientation='h',
                    title="Top 10 Most Required Skills"
                )
                st.plotly_chart(fig_skills, use_container_width=True)
                
                # Recent jobs table
                st.subheader("Recent Jobs")
                recent_jobs = df.head(5)[['title', 'company', 'location', 'department', 'experience_level']]
                st.dataframe(recent_jobs, use_container_width=True)
