import os
import numpy as np
from huggingface_hub import InferenceClient
from typing import List, Union, Optional
import time
import logging

class EmbeddingHandler:
    
    def __init__(self, 
                 model_name: Optional[str] = None,
                 api_token: Optional[str] = None,
                 max_retries: int = 3,
                 retry_delay: float = 1.0):

        # Get environment variables or use defaults
        model_name = model_name or os.getenv("HF_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        api_token = api_token or os.getenv("HF_API_KEY")

        self.model_name = model_name
        self.api_token = api_token
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize HuggingFace Hub client
        self.client = InferenceClient(api_key=self.api_token)
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.warning(f"EmbeddingHandler initialized with model: {self.model_name}")
    
    def _get_sentence_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get sentence embeddings by mean pooling token embeddings."""
        self.logger.info(f"Getting embeddings for {len(texts)} texts")
        
        for attempt in range(self.max_retries):
            try:
                # Get token-level embeddings
                outputs = self.client.feature_extraction(texts, model=self.model_name)
                arr = np.array(outputs)  # shape: (batch, tokens, dim) or (tokens, dim) for single
                
                # Ensure batch dimension
                if arr.ndim == 2:  # single text: (tokens, dim)
                    arr = arr[np.newaxis, ...]  # -> (1, tokens, dim)
                
                # Mean pool over tokens axis
                sentence_embeddings = arr.mean(axis=1)  # -> (batch, dim)
                
                # Convert to list of lists
                embeddings = sentence_embeddings.tolist()
                
                self.logger.info(f"Successfully got embeddings: {len(embeddings)} embeddings, each with {len(embeddings[0])} dimensions")
                return embeddings
                
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    self.logger.warning(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise Exception(f"Failed to get embeddings after {self.max_retries} attempts: {e}")
    
    def get_embeddings(self, texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        #Get embeddings for text(s). Can handle single string or list of strings.
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
            
            # Filter out empty strings
            texts = [text for text in texts if text and text.strip()]
            if not texts:
                raise ValueError("No valid non-empty texts provided")
            
            # Make API request
            embeddings = self._get_sentence_embeddings(texts)
            
            # Return single embedding if single input was provided
            if return_single:
                return embeddings[0]
            
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Error getting embeddings: {e}")
            raise e
    
    def get_job_embeddings(self, jobs: List[dict]) -> List[List[float]]:
        
        # Get embeddings for job descriptions.
        # Creates one embedding per job using title, description, and required skills.
        
        try:
            self.logger.info(f"Getting embeddings for {len(jobs)} jobs")
            
            job_texts = []
            valid_jobs = []
            
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
                
                # Skip if no meaningful text was generated
                if not full_text.strip():
                    self.logger.warning(f"Job {i+1} has no meaningful text content, skipping")
                    continue
                
                self.logger.info(f"Job {i+1} text length: {len(full_text)} characters")
                self.logger.debug(f"Job {i+1} text preview: {full_text[:200]}...")
                
                job_texts.append(full_text)
                valid_jobs.append(i+1)
                
            if not job_texts:
                raise Exception("No valid jobs with meaningful text content found")
            
            # Get embeddings for all jobs at once
            embeddings = self._get_sentence_embeddings(job_texts)
            
            self.logger.info(f"Generated embeddings for {len(embeddings)} jobs")
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Error getting job embeddings: {e}")
            raise e
    
    def get_resume_embedding(self, resume: Union[str, dict]) -> List[float]:

        # Get embedding for resume - can handle both string and dict input.

        try:
            self.logger.info(f"Getting resume embedding for: {type(resume)}")
            
            # Handle string input (plain text resume)
            if isinstance(resume, str):
                if not resume.strip():
                    raise ValueError("Resume string cannot be empty")
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
                
                if not full_text.strip():
                    raise ValueError("Resume dict contains no meaningful text content")
                
                self.logger.info(f"Resume text length: {len(full_text)} characters")
                self.logger.debug(f"Resume text preview: {full_text[:200]}...")
                
                embedding = self.get_embeddings(full_text)
                self.logger.info(f"Generated embedding for resume dict: {len(embedding)} dimensions")
                return embedding
            
            else:
                raise ValueError(f"Resume must be string or dict, got {type(resume)}")

        except Exception as e:
            self.logger.error(f"Error getting resume embedding: {e}")
            raise e