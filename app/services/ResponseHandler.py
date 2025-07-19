import streamlit as st
import json
import logging
from typing import Dict, Any, Optional, List

class ResponseHandler:
    
    def _parse_llm_response(self, response) -> Optional[Any]:
        try:

            # Case 1: AIMessage (LangChain)
            if hasattr(response, "content"):
                response = response.content

            # Case 2: Already a Python list
            if isinstance(response, list):
                return response

            # Case 3: Already a Python dict (may have 'content')
            if isinstance(response, dict):
                content = response.get("content")
                if content is None:
                    return response  # already structured job data
                if isinstance(content, list):
                    return content
                if isinstance(content, str):
                    return json.loads(content)

            # Case 4: String → parse JSON
            if isinstance(response, str):
                parsed = json.loads(response)

                if isinstance(parsed, list):
                    return parsed

                if isinstance(parsed, dict):
                    content = parsed.get("content")
                    if isinstance(content, list):
                        return content
                    if isinstance(content, str):
                        return json.loads(content)
                    return parsed

            raise ValueError(f"Unsupported LLM response type: {type(response)}")

        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return None
        except Exception as e:
            logging.error(f"Error parsing LLM response: {e}")
            return None


    
    def _validate_and_clean_resume(self, data: Any) -> Dict[str, Any]:

        default_structure = {
            "name": "",
            "location": "",
            "summary": "",
            "skills": [],
            "experience": [],
            "education": [],
            "certifications": [],
            "languages": [],
            "projects": []
        }

        # If the data is a list, take the first item
        if isinstance(data, list):
            data = data[0] if data else {}

        # Ensure it's a dictionary
        if not isinstance(data, dict):
            data = {}

        cleaned_resume = {}
        for key, default_value in default_structure.items():
            value = data.get(key, default_value)
            if key in ["skills", "experience", "education", "certifications", "languages", "projects"] and not isinstance(value, list):
                value = []
            cleaned_resume[key] = value

        return cleaned_resume

    
    
    def _validate_and_clean_jd(self, data: Any) -> List[Dict[str, Any]]:
        default_structure = {
            "job_title": "",
            "job_domain": "",
            "summary": "",
            "responsibilities": [],
            "required_skills": [],
            "qualifications": [],
            "experience_level": "",
            "company": "",
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

    