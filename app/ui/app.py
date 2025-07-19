import streamlit as st
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime
from io import StringIO
import base64

from .components.Header import Header
from .components.Sidebar import Sidebar
from .components.Footer import Footer
from .pages.Analytics import AnalyticsPage
from .pages.JobManagement import JobManagementPage
from .pages.Recommendations import RecommendationsPage
from .pages.Home import HomePage



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
                background: #764ba2;
                color: white !important;
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
