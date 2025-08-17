import streamlit as st
import logging
import time
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

    @staticmethod
    def retry(func, max_attempts=3, delay=3, *args, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Retry wrapper for any function.
        :param func: Function to call
        :param max_attempts: Number of attempts
        :param delay: Delay in seconds between retries
        :return: Function result or None if all retries fail
        """
        for attempt in range(1, max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"Attempt {attempt}/{max_attempts} failed: {str(e)}")
                if attempt == max_attempts:
                    logging.error("All retry attempts failed.")
                    raise
                time.sleep(delay)


    def structure_resume_data_retry(self, resume_text: dict) -> Dict[str, Any]:
        
        if not self._initialize_llm():
            raise RuntimeError("LLM initialization failed")

        current_response = ""  # empty on first page

        for page_num, page_content in resume_text.items():
            logging.info(f"Processing page {page_num}...")

            prompt = self.prompts.resume_extraction_prompt(
                resume_text=page_content,
                existing_json=current_response
            )

            response = self.llm.invoke(prompt)

            if hasattr(response, "content"):
                response_text = response.content
            elif hasattr(response, "text"):
                response_text = response.text
            else:
                raise RuntimeError(f"Unexpected LLM response type: {type(response)}")

            if not response_text.strip():
                raise RuntimeError(f"LLM returned empty response on page {page_num}")

            current_response = response_text.strip()

        if not current_response:
            raise RuntimeError("LLM returned no valid JSON for any page.")

        # Final post-processing
        try:
            structured_data = self.response_handler._parse_llm_response(current_response)
        except Exception as parse_err:
            raise RuntimeError(f"Error parsing JSON from LLM: {parse_err}")

        try:
            structured_data = self.response_handler._validate_and_clean_resume(structured_data)
        except Exception as validate_err:
            raise RuntimeError(f"Error validating/cleaning structured data: {validate_err}")

        return structured_data


    def structure_resume_data(self, resume_text: dict) -> Optional[Dict[str, Any]]:
        """
        Wrapper around structure_resume_data with retries for the whole function.
        """
        return self.retry(self.structure_resume_data_retry, max_attempts=3, delay=3, resume_text=resume_text)




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
            