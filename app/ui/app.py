import streamlit as st
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import base64

from app.ui.components.header import Header
from app.ui.components.sidebar import Sidebar
from app.ui.components.footer import Footer
from app.ui.pages.analytics import AnalyticsPage
from app.ui.pages.jobmanagement import JobManagementPage
from app.ui.pages.resumeupload import ResumeUploadPage
from app.ui.pages.recommendations import RecommendationsPage
from app.ui.pages.home import HomePage



class App:
    def __init__(self):
        self.setup_page()
        self.sidebar = Sidebar()
        self.header = Header()
        self.footer = Footer()
        self.analytics_page = AnalyticsPage()
        self.job_management_page = JobManagementPage()
        self.resume_upload_page = ResumeUploadPage()
        self.recommendations_page = RecommendationsPage()
        self.home_page = HomePage()
        
        # Initialize session state
        if 'job_descriptions' not in st.session_state:
            st.session_state.job_descriptions = []
        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = None
        if 'recommendations' not in st.session_state:
            st.session_state.recommendations = []
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None
            

    def setup_page(self):
        # Set page configuration
        st.set_page_config(
            page_title="AI-Powered Recruitment Platform",
            page_icon="🎯",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
            .main-header {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 10px;
                color: white;
                margin-bottom: 2rem;
            }
            
            .metric-card {
                background: white;
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                text-align: center;
            }
            
            .job-card {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                margin-bottom: 1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .skill-tag {
                background: #e3f2fd;
                color: #1976d2;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.8rem;
                margin: 0.1rem;
                display: inline-block;
            }
            
            .recommendation-card {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid #4caf50;
                margin-bottom: 1rem;
            }
            
            .sidebar .sidebar-content {
                background: #1e293b;
            }
            
            .stButton > button {
                width: 100%;
                background: #667eea;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-weight: 500;
            }
            
            .stButton > button:hover {
                background: #5a6fd8;
            }
            
            .upload-box {
                border: 2px dashed #ccc;
                border-radius: 8px;
                padding: 2rem;
                text-align: center;
                background: #f9f9f9;
            }
        </style>
        """, unsafe_allow_html=True)


        # Mock data for demonstration
        mock_jobs = [
            {
                "id": 1,
                "title": "Senior Frontend Developer",
                "company": "TechCorp Inc.",
                "location": "San Francisco, CA",
                "job_type": "Full-time",
                "experience_level": "Senior",
                "department": "Software Engineering",
                "salary_range": "$120,000 - $180,000",
                "required_skills": ["React", "JavaScript", "TypeScript", "CSS", "Node.js"],
                "responsibilities": ["Develop user interfaces", "Collaborate with design team", "Optimize performance"],
                "qualifications": ["5+ years experience", "Bachelor's degree", "Strong JavaScript skills"],
                "description": "We're looking for a Senior Frontend Developer to join our innovative team and build amazing user experiences.",
                "created_at": datetime.now()
            },
            {
                "id": 2,
                "title": "Data Scientist",
                "company": "DataVision Labs",
                "location": "New York, NY",
                "job_type": "Full-time",
                "experience_level": "Mid",
                "department": "Data Science",
                "salary_range": "$100,000 - $140,000",
                "required_skills": ["Python", "Machine Learning", "SQL", "TensorFlow", "Pandas"],
                "responsibilities": ["Build predictive models", "Analyze data trends", "Create visualizations"],
                "qualifications": ["3+ years experience", "Master's degree preferred", "Strong analytical skills"],
                "description": "Join our data science team to build predictive models and analytics solutions that drive business decisions.",
                "created_at": datetime.now()
            },
            {
                "id": 3,
                "title": "DevOps Engineer",
                "company": "CloudFirst Solutions",
                "location": "Austin, TX",
                "job_type": "Full-time",
                "experience_level": "Senior",
                "department": "DevOps",
                "salary_range": "$110,000 - $160,000",
                "required_skills": ["AWS", "Docker", "Kubernetes", "Jenkins", "Python"],
                "responsibilities": ["Manage CI/CD pipelines", "Monitor infrastructure", "Automate deployments"],
                "qualifications": ["4+ years experience", "AWS certification", "Strong automation skills"],
                "description": "We need a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines.",
                "created_at": datetime.now()
            }
        ]

        mock_resume = {
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1 (555) 123-4567",
            "skills": ["React", "JavaScript", "Python", "AWS", "Docker", "Node.js"],
            "experience": [
                {
                    "title": "Frontend Developer",
                    "company": "StartupXYZ",
                    "duration": "2021-2023",
                    "description": "Developed React applications with modern JavaScript"
                },
                {
                    "title": "Junior Developer",
                    "company": "WebCorp",
                    "duration": "2019-2021",
                    "description": "Built responsive web applications"
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Computer Science",
                    "institution": "University of Technology",
                    "year": "2019"
                }
            ],
            "summary": "Passionate frontend developer with 4+ years of experience in React and modern web technologies.",
            "certifications": ["AWS Certified Developer", "React Certification"]
        }



    def run(self):
        # Render header
        self.header.render()
        
        # Render sidebar
        self.sidebar.render()
        
        with st.tabs(["Home", "Job Management", "Resume Upload", "Recommendations", "Analytics"]):
            # Home Page
            with st.tab("Home"):
                self.home_page.render()
            
            # Job Management Page
            with st.tab("Job Management"):
                self.job_management_page.render()
            
            # Resume Upload Page
            with st.tab("Resume Upload"):
                self.resume_upload_page.render()
            
            # Recommendations Page
            with st.tab("Recommendations"):
                self.recommendations_page.render()
            
            # Analytics Page
            with st.tab("Analytics"):
                self.analytics_page.setup_analytics_page()
        
        # Render footer
        self.footer.render()
