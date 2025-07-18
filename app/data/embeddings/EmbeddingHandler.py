import requests
import json
import numpy as np
from typing import List, Union, Optional
import time
import logging
import os

class EmbeddingHandler:
    
    def __init__(self, 
                 model_name: Optional[str] = None,
                 api_token: Optional[str] = None,
                 max_retries: int = 3,
                 retry_delay: float = 1.0):

        # Get environment variables or use defaults
        hf_url = os.getenv("HF_URL")
        model_name = model_name or os.getenv("HF_MODEL")
        api_token = api_token or os.getenv("HF_API_KEY")

        self.model_name = model_name
        self.api_token = api_token
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Hugging Face Inference API endpoint
        self.api_url = f"{hf_url}/{model_name}"
        # Set up headers
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.warning(f"EmbeddingHandler initialized with model: {self.model_name}")
        self.logger.warning(f"API URL: {self.api_url}")
    
    def _make_request(self, texts: List[str]) -> List[List[float]]:
        payload = {
            "inputs": texts,
            "options": {
                "wait_for_model": True,
                "use_cache": True
            }
        }
        
        self.logger.info(f"Making embedding request for {len(texts)} texts")
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    embeddings = response.json()
                    self.logger.info(f"Successfully got embeddings: {len(embeddings)} embeddings, each with {len(embeddings[0])} dimensions")
                    return embeddings
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    self.logger.warning(f"Model is loading, waiting {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.logger.error(f"API request failed with status {response.status_code}: {response.text}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        raise Exception(f"API request failed: {response.status_code} - {response.text}")
                        
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request exception: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
        
        raise Exception(f"Failed to get embeddings after {self.max_retries} attempts")
    
    def get_embeddings(self, texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Get embeddings for text(s). Can handle single string or list of strings."""
        try:
            # Handle single string input
            if isinstance(texts, str):
                texts = [texts]
                return_single = True
            else:
                return_single = False
            
            # Validate input
            if not texts or len(texts) == 0:
                raise ValueError("Input texts cannot be empty")
            
            # Make API request
            embeddings = self._make_request(texts)
            
            # Return single embedding if single input was provided
            if return_single:
                return embeddings[0]
            
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Error getting embeddings: {e}")
            raise e
    
    def get_job_embeddings(self, jobs: List[dict]) -> List[List[float]]:
        """
        Get embeddings for job descriptions.
        Creates one embedding per job using title, description, and required skills.
        """
        try:
            self.logger.info(f"Getting embeddings for {len(jobs)} jobs")
            
            embeddings = []
            for i, job in enumerate(jobs):
                self.logger.info(f"Processing job {i+1}/{len(jobs)}: {job.get('job_title', 'No title')}")
                
                text_parts = []
                if job.get("job_title"):
                    text_parts.append(f"Title: {job['job_title']}")
                    
                if job.get("job_domain"):
                    text_parts.append(f"Domain: {job['job_domain']}")
                    
                if job.get("summary"):
                    text_parts.append(f"Summary: {job['summary']}")
                    
                if job.get("responsibilities"):
                    if isinstance(job["responsibilities"], list):
                        resp_text = "; ".join(job["responsibilities"])
                    else:
                        resp_text = str(job["responsibilities"])
                    text_parts.append(f"Responsibilities: {resp_text}")
                    
                if job.get("required_skills"):
                    if isinstance(job["required_skills"], list):
                        skills_text = ", ".join(job["required_skills"])
                    else:
                        skills_text = str(job["required_skills"])
                    text_parts.append(f"Required Skills: {skills_text}")
                    
                if job.get("qualifications"):
                    if isinstance(job["qualifications"], list):
                        qual_text = "; ".join(job["qualifications"])
                    else:
                        qual_text = str(job["qualifications"])
                    text_parts.append(f"Qualifications: {qual_text}")
                    
                if job.get("experience_level"):
                    text_parts.append(f"Experience Level: {job['experience_level']}")
                
                if job.get("company"):
                    text_parts.append(f"Company: {job['company']}")
                    
                if job.get("location"):
                    text_parts.append(f"Location: {job['location']}")
                    
                if job.get("employment_type"):
                    text_parts.append(f"Employment Type: {job['employment_type']}")
                    
                full_text = "\n".join(text_parts)
                
                self.logger.info(f"Job {i+1} text length: {len(full_text)} characters")
                self.logger.info(f"Job {i+1} text preview: {full_text[:200]}...")
                
                # Get embedding for this job
                embedding = self.get_embeddings(full_text)
                embeddings.append(embedding)
                
                self.logger.info(f"Generated embedding for job {i+1}: {len(embedding)} dimensions")
                
            self.logger.info(f"Generated embeddings for {len(jobs)} jobs")
            return embeddings
        except Exception as e:
            self.logger.error(f"Error getting job embeddings: {e}")
            raise e
    
    def get_resume_embedding(self, resume: Union[str, dict]) -> List[float]:
        """
        Get embedding for resume - can handle both string and dict input.
        """
        try:
            self.logger.info(f"Getting resume embedding for: {type(resume)}")
            
            # Handle string input (plain text resume)
            if isinstance(resume, str):
                self.logger.info(f"Processing resume as string, length: {len(resume)} characters")
                embedding = self.get_embeddings(resume)
                self.logger.info(f"Generated embedding for resume string: {len(embedding)} dimensions")
                return embedding
            
            # Handle dict input (structured resume)
            elif isinstance(resume, dict):
                self.logger.info(f"Processing resume as dict with keys: {list(resume.keys())}")
                
                text_parts = []
                if resume.get("name"):
                    text_parts.append(f"Name: {resume['name']}")
                if resume.get("email"):
                    text_parts.append(f"Email: {resume['email']}")
                if resume.get("phone"):
                    text_parts.append(f"Phone: {resume['phone']}")
                if resume.get("location"):
                    text_parts.append(f"Location: {resume['location']}")
                if resume.get("summary"):
                    text_parts.append(f"Summary: {resume['summary']}")
                if resume.get("skills"):
                    skills_text = ", ".join(resume["skills"]) if isinstance(resume["skills"], list) else str(resume["skills"])
                    text_parts.append(f"Skills: {skills_text}")
                if resume.get("experience"):
                    if isinstance(resume["experience"], list):
                        exp_text = "; ".join([str(e) for e in resume["experience"]])
                    else:
                        exp_text = str(resume["experience"])
                    text_parts.append(f"Experience: {exp_text}")
                if resume.get("education"):
                    if isinstance(resume["education"], list):
                        edu_text = "; ".join([str(e) for e in resume["education"]])
                    else:
                        edu_text = str(resume["education"])
                    text_parts.append(f"Education: {edu_text}")
                if resume.get("certifications"):
                    cert_text = ", ".join(resume["certifications"]) if isinstance(resume["certifications"], list) else str(resume["certifications"])
                    text_parts.append(f"Certifications: {cert_text}")
                if resume.get("languages"):
                    lang_text = ", ".join(resume["languages"]) if isinstance(resume["languages"], list) else str(resume["languages"])
                    text_parts.append(f"Languages: {lang_text}")
                if resume.get("projects"):
                    if isinstance(resume["projects"], list):
                        proj_text = "; ".join([str(p) for p in resume["projects"]])
                    else:
                        proj_text = str(resume["projects"])
                    text_parts.append(f"Projects: {proj_text}")

                full_text = "\n".join(text_parts)
                
                self.logger.info(f"Resume text length: {len(full_text)} characters")
                self.logger.info(f"Resume text preview: {full_text[:200]}...")
                
                embedding = self.get_embeddings(full_text)
                self.logger.info(f"Generated embedding for resume dict: {len(embedding)} dimensions")
                return embedding
            
            else:
                raise ValueError(f"Resume must be string or dict, got {type(resume)}")

        except Exception as e:
            self.logger.error(f"Error getting resume embedding: {e}")
            raise e