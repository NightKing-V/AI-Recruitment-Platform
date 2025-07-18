import os
import logging
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI
import streamlit as st
import time

class EmbeddingsHandler:
    """Handle text embeddings using OpenAI API"""
    
    def __init__(self):
        self.client = None
        self.model = "text-embedding-3-small"  # You can also use text-embedding-3-large
        self.max_tokens = 8192
        self.setup_client()
    
    def setup_client(self):
        """Setup OpenAI client"""
        try:
            api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
            
            if not api_key:
                st.error("OpenAI API key not found. Please set OPENAI_API_KEY in environment or secrets.")
                return False
            
            self.client = OpenAI(api_key=api_key)
            logging.info("OpenAI client setup successful")
            return True
            
        except Exception as e:
            logging.error(f"Error setting up OpenAI client: {e}")
            st.error(f"Failed to setup OpenAI client: {e}")
            return False
    
    def create_embedding(self, text: str) -> Optional[List[float]]:
        """Create embedding for a single text"""
        try:
            if not self.client:
                logging.error("OpenAI client not initialized")
                return None
            
            # Truncate text if too long
            if len(text) > self.max_tokens:
                text = text[:self.max_tokens]
            
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            
            embedding = response.data[0].embedding
            logging.info(f"Created embedding for text of length {len(text)}")
            return embedding
            
        except Exception as e:
            logging.error(f"Error creating embedding: {e}")
            return None
    
    def create_batch_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Create embeddings for multiple texts in batches"""
        try:
            if not self.client:
                logging.error("OpenAI client not initialized")
                return []
            
            embeddings = []
            
            # Process in batches
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                # Truncate texts if too long
                batch = [text[:self.max_tokens] if len(text) > self.max_tokens else text for text in batch]
                
                try:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=batch
                    )
                    
                    batch_embeddings = [data.embedding for data in response.data]
                    embeddings.extend(batch_embeddings)
                    
                    logging.info(f"Created {len(batch_embeddings)} embeddings in batch {i//batch_size + 1}")
                    
                    # Rate limiting - wait a bit between batches
                    if i + batch_size < len(texts):
                        time.sleep(0.1)
                        
                except Exception as e:
                    logging.error(f"Error in batch {i//batch_size + 1}: {e}")
                    # Add None for failed embeddings
                    embeddings.extend([None] * len(batch))
            
            return embeddings
            
        except Exception as e:
            logging.error(f"Error creating batch embeddings: {e}")
            return []
    
    def create_job_embedding(self, job_data: Dict[str, Any]) -> Optional[List[float]]:
        """Create embedding for job description"""
        try:
            # Combine relevant job fields for embedding
            text_parts = []
            
            # Title and company
            if job_data.get("title"):
                text_parts.append(f"Job Title: {job_data['title']}")
            if job_data.get("company"):
                text_parts.append(f"Company: {job_data['company']}")
            
            # Location and department
            if job_data.get("location"):
                text_parts.append(f"Location: {job_data['location']}")
            if job_data.get("department"):
                text_parts.append(f"Department: {job_data['department']}")
            
            # Experience level
            if job_data.get("experience_level"):
                text_parts.append(f"Experience Level: {job_data['experience_level']}")
            
            # Job type
            if job_data.get("job_type"):
                text_parts.append(f"Job Type: {job_data['job_type']}")
            
            # Required skills
            if job_data.get("required_skills"):
                skills = ", ".join(job_data["required_skills"])
                text_parts.append(f"Required Skills: {skills}")
            
            # Description
            if job_data.get("description"):
                text_parts.append(f"Description: {job_data['description']}")
            
            # Summary
            if job_data.get("summary"):
                text_parts.append(f"Summary: {job_data['summary']}")
            
            # Responsibilities
            if job_data.get("responsibilities"):
                if isinstance(job_data["responsibilities"], list):
                    responsibilities = ". ".join(job_data["responsibilities"])
                else:
                    responsibilities = job_data["responsibilities"]
                text_parts.append(f"Responsibilities: {responsibilities}")
            
            # Qualifications
            if job_data.get("qualifications"):
                if isinstance(job_data["qualifications"], list):
                    qualifications = ". ".join(job_data["qualifications"])
                else:
                    qualifications = job_data["qualifications"]
                text_parts.append(f"Qualifications: {qualifications}")
            
            # Combine all parts
            combined_text = " | ".join(text_parts)
            
            # Create embedding
            return self.create_embedding(combined_text)
            
        except Exception as e:
            logging.error(f"Error creating job embedding: {e}")
            return None
    
    def create_resume_embedding(self, resume_data: Dict[str, Any]) -> Optional[List[float]]:
        """Create embedding for resume"""
        try:
            # Combine relevant resume fields for embedding
            text_parts = []
            
            # Name and contact
            if resume_data.get("name"):
                text_parts.append(f"Name: {resume_data['name']}")
            
            # Summary
            if resume_data.get("summary"):
                text_parts.append(f"Summary: {resume_data['summary']}")
            
            # Skills
            if resume_data.get("skills"):
                skills = ", ".join(resume_data["skills"])
                text_parts.append(f"Skills: {skills}")
            
            # Experience
            if resume_data.get("experience"):
                for exp in resume_data["experience"]:
                    exp_text = f"Experience: {exp.get('title', '')} at {exp.get('company', '')} - {exp.get('description', '')}"
                    text_parts.append(exp_text)
            
            # Education
            if resume_data.get("education"):
                for edu in resume_data["education"]:
                    edu_text = f"Education: {edu.get('degree', '')} from {edu.get('institution', '')}"
                    text_parts.append(edu_text)
            
            # Certifications
            if resume_data.get("certifications"):
                certifications = ", ".join(resume_data["certifications"])
                text_parts.append(f"Certifications: {certifications}")
            
            # Projects
            if resume_data.get("projects"):
                for project in resume_data["projects"]:
                    if isinstance(project, dict):
                        project_text = f"Project: {project.get('name', '')} - {project.get('description', '')}"
                    else:
                        project_text = f"Project: {project}"
                    text_parts.append(project_text)
            
            # Combine all parts
            combined_text = " | ".join(text_parts)
            
            # Create embedding
            return self.create_embedding(combined_text)
            
        except Exception as e:
            logging.error(f"Error creating resume embedding: {e}")
            return None
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            import numpy as np
            
            # Convert to numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            logging.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def get_embedding_dimensions(self) -> int:
        """Get the dimensions of the embedding model"""
        if self.model == "text-embedding-3-small":
            return 1536
        elif self.model == "text-embedding-3-large":
            return 3072
        else:
            return 1536  # Default