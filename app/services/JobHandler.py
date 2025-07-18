from typing import List, Dict, Any, Optional
import json
import streamlit as st

from llm.LLMProcessor import LLMProcessor
from pipelines.JobPipeline import JobPipeline


class jobHandler:
    """Generate realistic job descriptions using LLM"""
    
    def __init__(self):
        self.llm_processor = LLMProcessor()
        self.pipeline = JobPipeline()
        
    def generate_job(self, job_num: int, job_domains:List[str])-> List[Dict[str, Any]]:
        
        # Generate job descriptions for given domains using LLM.
        
        if not self.llm_processor._initialize_llm():
            return []
        
        try:
            jobs = self.llm_processor.job_description_generator(job_num, job_domains)
            if not jobs:
                st.error("No job descriptions generated")
                return []
            result = self.pipeline.job_pipeline(jobs)
            
            return result
        except Exception as e:
            st.error(f"Error generating job descriptions: {str(e)}")
            return []
        
        
        
    def create_job(self, job_desc: str) -> Optional[str]:
        
        if not job_desc:
            st.error("Job description cannot be empty")
            return None
        
        try:
            jobs = self.llm_processor.job_summary_generator(job_desc)
            
            if not jobs:
                st.error("No job descriptions generated")
                return []
            result = self.pipeline.job_pipeline(jobs)
            
            return result
            
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error creating job summary: {str(e)}")
            return None
