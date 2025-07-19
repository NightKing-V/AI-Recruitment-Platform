import streamlit as st
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime
from io import StringIO
import base64

from ui.components.Header import Header
from ui.components.Sidebar import Sidebar
from ui.components.Footer import Footer
from ui.pages.Analytics import AnalyticsPage
from ui.pages.JobManagement import JobManagementPage
from ui.pages.Recommendations import RecommendationsPage
from ui.pages.Home import HomePage



class App:
    def __init__(self):
        self.setup_page()
        self.sidebar = Sidebar()
        self.header = Header()
        self.footer = Footer()
        self.analytics_page = AnalyticsPage()
        self.job_management_page = JobManagementPage()
        self.recommendations_page = RecommendationsPage()
        self.home_page = HomePage()
        
        # # Initialize session state
        # if 'job_descriptions' not in st.session_state:
        #     st.session_state.job_descriptions = []
        # if 'resume_data' not in st.session_state:
        #     st.session_state.resume_data = None
        # if 'recommendations' not in st.session_state:
        #     st.session_state.recommendations = []
        # if 'uploaded_file' not in st.session_state:
        #     st.session_state.uploaded_file = None
            

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
            /* Reduce default Streamlit top padding */
            .block-container {
                padding-top: 0.5rem !important;
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
            
            /* Tab container spacing */
            .stTabs [data-baseweb="tab-list"] {
                gap: 4px;
                margin-bottom: 10px;
            }

            /* Individual tab styling */
            .stTabs [data-baseweb="tab"] {
                background-color: transparent;
                border-radius: 6px 6px 6px 6px;
                padding: 8px 16px;
                font-size: 14px;
                color: #ffff;
                transition: background-color 0.2s ease;
            }

            /* Active tab */
            .stTabs [aria-selected="true"] {
                background-color: #667eea;
                font-weight: 600;
                color: #fff;
            }

            /* Hover effect */
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #764ba2;
                color: #fff;
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
        
        home_tab, job_tab, rec_tab, ana_tab = st.tabs(["Home", "Job Management", "Recommendations", "Analytics"])
        # Home Page
        with home_tab:
            self.home_page.render()
        
        # Job Management Page
        with job_tab:
            self.job_management_page.render()
        
        # Recommendations Page
        with rec_tab:
            self.recommendations_page.render()
        
        # Analytics Page
        with ana_tab:
            self.analytics_page.render()
        
        # Render footer
        self.footer.render()
