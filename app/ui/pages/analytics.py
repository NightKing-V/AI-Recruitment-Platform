import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data.mongodb.MongoClient import MongoDBHandler
import logging

class AnalyticsPage:
    def __init__(self):
        self.mongo_handler = MongoDBHandler()
        
    def render(self):
        """Render the analytics dashboard using MongoDB data"""
        with st.container():
            st.subheader("Analytics Dashboard")
            
            # Get data from MongoDB
            try:
                jobs_data = self.mongo_handler.get_all_jobs()
                
                if not jobs_data:
                    st.info("No job data available for analytics. Please add some job descriptions first.")
                    return
                
                # Convert to DataFrame
                df = pd.DataFrame(jobs_data)
                
                # Display key metrics
                self._display_key_metrics(df)
                
                st.markdown("---")
                
                # Display charts
                self._display_charts(df, jobs_data)
                
                # Display recent jobs table
                self._display_recent_jobs(df)
                
            except Exception as e:
                st.error(f"Error loading analytics data: {e}")
                logging.error(f"Analytics page error: {e}")
    
    def _display_key_metrics(self, df):
        """Display key metrics in columns"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", len(df))
        
        with col2:
            companies_count = df['company'].nunique() if 'company' in df.columns else 0
            st.metric("Companies", companies_count)
        
        with col3:
            locations_count = df['location'].nunique() if 'location' in df.columns else 0
            st.metric("Locations", locations_count)
        
        with col4:
            # Use job_domain instead of department
            domains_count = df['job_domain'].nunique() if 'job_domain' in df.columns else 0
            st.metric("Job Domains", domains_count)
    
    def _display_charts(self, df, jobs_data):
        """Display various analytics charts"""
        col1, col2 = st.columns(2)
        
        with col1:
            self._display_domain_chart(df)
        
        with col2:
            self._display_experience_chart(df)
        
        # Location analysis
        self._display_location_chart(df)
        
        # Skills analysis
        self._display_skills_chart(jobs_data)
    
    def _display_domain_chart(self, df):
        """Display jobs by domain pie chart"""
        st.subheader("Jobs by Domain")
        
        if 'job_domain' in df.columns and not df['job_domain'].isna().all():
            domain_counts = df['job_domain'].value_counts()
            if not domain_counts.empty:
                fig_domain = px.pie(
                    values=domain_counts.values,
                    names=domain_counts.index,
                    title="Distribution of Jobs by Domain"
                )
                st.plotly_chart(fig_domain, use_container_width=True)
            else:
                st.info("No domain data available")
        else:
            st.info("No domain data available")
    
    def _display_experience_chart(self, df):
        """Display jobs by experience level bar chart"""
        st.subheader("Jobs by Experience Level")
        
        if 'experience_level' in df.columns and not df['experience_level'].isna().all():
            exp_counts = df['experience_level'].value_counts()
            if not exp_counts.empty:
                fig_exp = px.bar(
                    x=exp_counts.index,
                    y=exp_counts.values,
                    title="Jobs by Experience Level",
                    labels={'x': 'Experience Level', 'y': 'Number of Jobs'}
                )
                st.plotly_chart(fig_exp, use_container_width=True)
            else:
                st.info("No experience level data available")
        else:
            st.info("No experience level data available")
    
    def _display_location_chart(self, df):
        """Display top locations horizontal bar chart"""
        st.subheader("Top Locations")
        
        if 'location' in df.columns and not df['location'].isna().all():
            location_counts = df['location'].value_counts().head(10)
            if not location_counts.empty:
                fig_loc = px.bar(
                    x=location_counts.values,
                    y=location_counts.index,
                    orientation='h',
                    title="Top 10 Job Locations",
                    labels={'x': 'Number of Jobs', 'y': 'Location'}
                )
                st.plotly_chart(fig_loc, use_container_width=True)
            else:
                st.info("No location data available")
        else:
            st.info("No location data available")
    
    def _display_skills_chart(self, jobs_data):
        """Display most in-demand skills chart"""
        st.subheader("Most In-Demand Skills")
        
        try:
            all_skills = []
            
            # Extract skills from all jobs using the correct field name
            for job in jobs_data:
                if 'required_skills' in job and job['required_skills']:
                    if isinstance(job['required_skills'], list):
                        all_skills.extend(job['required_skills'])
                    elif isinstance(job['required_skills'], str):
                        # Split string by common separators
                        skills = job['required_skills'].replace(',', '\n').replace(';', '\n').split('\n')
                        all_skills.extend([skill.strip() for skill in skills if skill.strip()])
            
            if all_skills:
                skills_df = pd.DataFrame(all_skills, columns=['skill'])
                skill_counts = skills_df['skill'].value_counts().head(10)
                
                fig_skills = px.bar(
                    x=skill_counts.values,
                    y=skill_counts.index,
                    orientation='h',
                    title="Top 10 Most Required Skills",
                    labels={'x': 'Frequency', 'y': 'Skill'}
                )
                st.plotly_chart(fig_skills, use_container_width=True)
            else:
                st.info("No skills data available")
                
        except Exception as e:
            st.info("No skills data available")
            logging.error(f"Error processing skills data: {e}")
    
    def _display_recent_jobs(self, df):
        """Display recent jobs table"""
        st.subheader("Recent Jobs")
        
        try:
            # Define columns to display based on your job structure
            display_columns = []
            possible_columns = ['job_title', 'company', 'location', 'job_domain', 'experience_level', 'employment_type', 'created_at']
            
            for col in possible_columns:
                if col in df.columns:
                    display_columns.append(col)
            
            if display_columns:
                # Sort by created_at if available, otherwise by index
                if 'created_at' in df.columns:
                    df_sorted = df.sort_values('created_at', ascending=False)
                else:
                    df_sorted = df
                
                recent_jobs = df_sorted.head(5)[display_columns]
                
                # Format datetime if present
                if 'created_at' in recent_jobs.columns:
                    recent_jobs['created_at'] = pd.to_datetime(recent_jobs['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                # Rename columns for better display
                column_rename = {
                    'job_title': 'Job Title',
                    'job_domain': 'Domain',
                    'experience_level': 'Experience',
                    'employment_type': 'Type',
                    'created_at': 'Created'
                }
                
                display_df = recent_jobs.rename(columns=column_rename)
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info("No job data available to display")
                
        except Exception as e:
            st.error(f"Error displaying recent jobs: {e}")
            logging.error(f"Error displaying recent jobs: {e}")
    
    def __del__(self):
        """Cleanup MongoDB connection when object is destroyed"""
        if hasattr(self, 'mongo_handler') and self.mongo_handler:
            self.mongo_handler.close_connection()