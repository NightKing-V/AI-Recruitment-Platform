from typing import List, Dict, Any, Optional
import json
import streamlit as st
import time

from llm.LLMProcessor import LLMProcessor
from pipelines.JobPipeline import JobPipeline


class jobHandler:

    def __init__(self):
        self.llm_processor = LLMProcessor()
        self.pipeline = JobPipeline()
            
            
    def generate_job(self, job_num: int, job_domains: List[str]) -> List[Dict[str, Any]]:
        if not self.llm_processor._initialize_llm():
            return []

        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Generate fresh jobs each attempt
                jobs = self.llm_processor.job_description_generator(job_num, job_domains)
                if not jobs:
                    raise ValueError("No job descriptions generated")

                # Pass through pipeline
                result = self.pipeline.job_pipeline(jobs)
                return result  # Success, return immediately

            except Exception as e:
                st.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait a bit before retry
                    continue
                else:
                    st.error(f"{job_num} Job generations failed for {job_domains} after multiple retries.")
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
