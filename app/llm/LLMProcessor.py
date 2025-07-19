import streamlit as st
from typing import Dict, Any, Optional
from .LLMFactory import LLMFactory
from .clients.GroqClient import GroqClient
from .prompts.PromptTemplates import PromptTemplates
from services.ResponseHandler import ResponseHandler


class LLMProcessor:
    """Handles LLM communication for resume processing"""
    
    def __init__(self):
        # Register and initialize the Groq provider
        LLMFactory.register_provider('groq', GroqClient)
        self.prompts = PromptTemplates()
        self.response_handler = ResponseHandler()
        self.llm = None
        
    def _initialize_llm(self):
        """Initialize the LLM instance if not already done"""
        if self.llm is None:
            try:
                self.llm = LLMFactory.get_llm('groq')
            except Exception as e:
                st.error(f"Failed to initialize Groq LLM: {str(e)}")
                return False
        return True
    
    def structure_resume_data(self, resume_text: str) -> Optional[Dict[str, Any]]:
        """Send resume text to LLM and get structured data back"""
        
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
            st.error(f"Error generating job description: {str(e)}")
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
            st.error(f"Error creating job: {str(e)}")
            return None
            
        
        
        
    
    
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     def generate_resume_summary(self, structured_data: Dict[str, Any]) -> Optional[str]:
#         """Generate a professional summary based on structured resume data"""
        
#         if not self._initialize_llm():
#             return None
        
#         prompt = f"""
# Based on the following structured resume data, generate a professional summary (2-3 sentences) that highlights the candidate's key strengths, experience, and value proposition.

# Resume Data:
# {json.dumps(structured_data, indent=2)}

# Generate a concise, professional summary that would be suitable for the top of a resume:
# """
        
#         try:
#             response = self.llm.invoke(prompt)
#             return response.strip()
#         except Exception as e:
#             st.error(f"Error generating resume summary: {str(e)}")
#             return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     def extract_keywords(self, job_description: str, resume_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
#         """Extract relevant keywords from job description and match with resume"""
        
#         if not self._initialize_llm():
#             return None
        
#         prompt = f"""
# Analyze the following job description and resume data to identify:
# 1. Key skills and technologies mentioned in the job description
# 2. Skills from the resume that match the job requirements
# 3. Missing skills that the candidate should highlight or develop

# Job Description:
# {job_description}

# Resume Data:
# {json.dumps(resume_data, indent=2)}

# Return the analysis in JSON format:
# {{
#     "job_keywords": ["keyword1", "keyword2"],
#     "matching_skills": ["skill1", "skill2"],
#     "missing_skills": ["skill3", "skill4"],
#     "match_percentage": 85,
#     "recommendations": ["recommendation1", "recommendation2"]
# }}
# """
        
#         try:
#             response = self.llm.invoke(prompt)
#             return self._parse_llm_response(response)
#         except Exception as e:
#             st.error(f"Error extracting keywords: {str(e)}")
#             return None