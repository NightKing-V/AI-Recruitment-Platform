import streamlit as st
from typing import Dict, Any, Optional
from .LLMFactory import LLMFactory
from .clients.GroqClient import GroqClient
from .prompts.PromptTemplates import PromptTemplates
from services.ResponseHandler import ResponseHandler


class LLMProcessor:
    
    def __init__(self):
        # Register and initialize the Groq provider
        LLMFactory.register_provider('groq', GroqClient)
        self.prompts = PromptTemplates()
        self.response_handler = ResponseHandler()
        self.llm = None
        
    def _initialize_llm(self):
        if self.llm is None:
            try:
                self.llm = LLMFactory.get_llm('groq')
            except Exception as e:
                st.error(f"Failed to initialize Groq LLM: {str(e)}")
                return False
        return True
    
    def structure_resume_data(self, resume_text: str) -> Optional[Dict[str, Any]]:
        
        if not self._initialize_llm():
            return None
        
        # Define the structured prompt for resume data extraction
        prompt = self.prompts.resume_extraction_prompt(resume_text=resume_text)
        
        try:
            # Use the Groq client to process the resume
            response = self.llm.invoke(prompt)
            
            # Extract the JSON from the response
            parsed_data = self.response_handler._parse_llm_response(response)
            structured_data = self.response_handler._validate_and_clean_resume(parsed_data)
            
            return structured_data
            
        except Exception as e:
            st.error(f"Error processing resume with Groq LLM: {str(e)}")
            return None
        
        
    def job_description_generator(self, job_num, job_domain:str) -> Optional[Dict[str, Any]]:
        if not self._initialize_llm():
            return None
        
        prompt = self.prompts.job_generator_prompt(job_num, job_domain)
        
        try:
            response = self.llm.invoke(prompt)
            
            parsed_data = self.response_handler._parse_llm_response(response)
            structured_data = self.response_handler._validate_and_clean_jd(parsed_data)

            return structured_data

        except Exception as e:
            st.error(f"An error occurred!")
            return None
        
    def job_summary_generator(self, job_desc: str) -> Optional[Dict[str, Any]]:
        if not self._initialize_llm():
            return None
        
        prompt = self.prompts.job_extraction_prompt(job_desc)
        
        try:
            response = self.llm.invoke(prompt)
            
            parsed_data = self.response_handler._parse_llm_response(response)
            structured_data = self.response_handler._validate_and_clean_jd(parsed_data)
            
            return structured_data

        except Exception as e:
            st.error(f"An error occurred!")
            return None
            