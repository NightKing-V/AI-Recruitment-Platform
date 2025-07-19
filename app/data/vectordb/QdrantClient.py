import os
import logging
from typing import List, Dict, Any, Optional, Union
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import uuid
import streamlit as st

class QdrantHandler:
    
    def __init__(self, collection_name: str = "jobs"):
        self.client = None
        self.collection_name = collection_name
        self.vector_size = 384  # Groq embedding size (e.g., llama-3-8b)
        self.logger = logging.getLogger(__name__)
        self.connect()
    
    def connect(self):
        # Connect to Qdrant
        try:
            # Get Qdrant configuration from environment or Streamlit secrets
            qdrant_url = os.getenv("QDRANT_URL") or st.secrets.get("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY") or st.secrets.get("QDRANT_API_KEY")
            
            if not qdrant_url:
                self.logger.error("Qdrant URL not found. Please set QDRANT_URL in environment or secrets.")
                return False
            
            if qdrant_api_key:
                self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            else:
                self.client = QdrantClient(url=qdrant_url)
            
            # Check if collection exists, create if not
            self.ensure_collection_exists()
            
            self.logger.info("Successfully connected to Qdrant")
            return True
            
        except Exception as e:
            self.logger.error(f"Qdrant connection error: {e}")
            return False
    
    def ensure_collection_exists(self):
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    ),
                )
                self.logger.info(f"Created collection: {self.collection_name}")
            else:
                self.logger.info(f"Collection {self.collection_name} already exists")
                
        except Exception as e:
            self.logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    def store_job_vector(self, job_data: Dict[str, Any], embedding: List[float], job_id: str) -> bool:
        try:
            self.logger.info(f"Storing job vector for job_id: {job_id}")
            
            # Validate embedding dimension
            if len(embedding) != self.vector_size:
                self.logger.error(f"Embedding dimension mismatch: expected {self.vector_size}, got {len(embedding)}")
                return False
            
            # Create point with proper field mapping
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "job_id": job_id,
                    "title": job_data.get("job_title", ""),  # Fixed: job_title -> title
                    "company": job_data.get("company", ""),
                    "location": job_data.get("location", ""),
                    "department": job_data.get("department", ""),
                    "job_domain": job_data.get("job_domain", ""),  # Added job_domain
                    "experience_level": job_data.get("experience_level", ""),
                    "employment_type": job_data.get("employment_type", ""),
                    "required_skills": job_data.get("required_skills", []),
                    "salary_range": job_data.get("salary_range", ""),
                    "description": job_data.get("description", ""),
                    "summary": job_data.get("summary", ""),
                    "responsibilities": job_data.get("responsibilities", []),
                    "qualifications": job_data.get("qualifications", []),
                    "created_at": str(job_data.get("created_at", "")),
                }
            )
            
            # Store the point
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            self.logger.info(f"Successfully stored job vector for job_id: {job_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing job vector for job_id {job_id}: {e}")
            return False
    
    def search_similar_jobs(self, query_vector: List[float], limit: int = 10) -> List[str]:
        try:

            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            job_ids = [result.payload.get("job_id") for result in search_results if result.payload.get("job_id")]
            scores = [result.score for result in search_results if result.payload.get("job_id")]

            self.logger.info(f"Found {len(job_ids)} similar jobs")
            return job_ids, scores


        except Exception as e:
            self.logger.error(f"Error searching similar jobs: {e}")
            return []
    
    def delete_job_vector(self, job_id: str) -> bool:
        try:
            self.logger.info(f"Deleting job vector for job_id: {job_id}")
            
            # Search for the point with the job_id
            search_results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="job_id",
                            match=MatchValue(value=job_id)
                        )
                    ]
                ),
                limit=1
            )
            
            if search_results[0]:  # If points found
                point_id = search_results[0][0].id
                
                # Delete the point
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=[point_id]
                )
                
                self.logger.info(f"Successfully deleted vector for job_id: {job_id}")
                return True
            else:
                self.logger.warning(f"No vector found for job_id: {job_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error deleting vector for job_id {job_id}: {e}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "status": info.status
            }
        except Exception as e:
            self.logger.error(f"Error getting collection info: {e}")
            return {}
    
    def delete_collection(self) -> bool:
        try:
            self.client.delete_collection(self.collection_name)
            self.logger.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting collection: {e}")
            return False