import streamlit as st
import json
from typing import Dict, Any, Optional

class ResponseHandler:
    
    def _parse_llm_response(self, response: str) -> Optional[Any]:
        """Parse the LLM response and extract JSON data (object or list)"""
        try:
            cleaned_response = response.strip()

            # Remove markdown code blocks if present
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            elif cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]

            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]

            # Extract JSON substring: look for either {..} or [..]
            start_idx = cleaned_response.find('{')
            start_idx_list = cleaned_response.find('[')

            if start_idx_list != -1 and (start_idx_list < start_idx or start_idx == -1):
                # It's a list
                start_idx = start_idx_list
                end_idx = cleaned_response.rfind(']')
            else:
                # It's a single object
                end_idx = cleaned_response.rfind('}')

            if start_idx != -1 and end_idx != -1:
                json_str = cleaned_response[start_idx:end_idx + 1]
                parsed_data = json.loads(json_str)
                return parsed_data  # could be dict or list
            else:
                raise ValueError("No valid JSON found in response")

        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON from LLM response: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error parsing LLM response: {str(e)}")
            return None

    
    def _validate_and_clean_resume(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the extracted data"""
        
        # Define the expected structure with defaults
        default_structure = {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "summary": "",
            "skills": [],
            "experience": [],
            "education": [],
            "certifications": [],
            "languages": [],
            "projects": []
        }
        
        # Merge with defaults to ensure all required fields exist
        for key, default_value in default_structure.items():
            if key not in data:
                data[key] = default_value
            elif data[key] is None:
                data[key] = default_value
        
        # Clean and validate specific fields
        if not isinstance(data["skills"], list):
            data["skills"] = []
        
        if not isinstance(data["experience"], list):
            data["experience"] = []
        
        if not isinstance(data["education"], list):
            data["education"] = []
        
        if not isinstance(data["certifications"], list):
            data["certifications"] = []
        
        if not isinstance(data["languages"], list):
            data["languages"] = []
        
        if not isinstance(data["projects"], list):
            data["projects"] = []
        
        return data
    
    
    def _validate_and_clean_data(self, data: Any) -> List[Dict[str, Any]]:
        """Validate and clean a list of job descriptions"""
        default_structure = {
            "job_title": "",
            "job_domain": "",
            "summary": "",
            "responsibilities": [],
            "required_skills": [],
            "qualifications": [],
            "experience_level": "",
            "location": "",
            "employment_type": ""
        }

        if not isinstance(data, list):
            data = [data]  # wrap single dict into a list

        cleaned_jobs = []
        for jd in data:
            cleaned_jd = {}
            for key, default_value in default_structure.items():
                value = jd.get(key, default_value)
                if key in ["responsibilities", "required_skills", "qualifications"] and not isinstance(value, list):
                    value = []
                cleaned_jd[key] = value
            cleaned_jobs.append(cleaned_jd)

        return cleaned_jobs

    