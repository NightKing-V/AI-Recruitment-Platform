import os
import logging
from typing import List, Dict, Any, Optional, Union
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import uuid
import streamlit as st

class QdrantHandler:
    """Handle Qdrant vector database operations for job matching"""
    
    def __init__(self, collection_name: str = "jobs"):
        self.client = None
        self.collection_name = collection_name
        self.vector_size = 4096  # Groq embedding size (e.g., llama-3-8b)
        self.connect()
    
    def connect(self):
        """Connect to Qdrant"""
        try:
            # Get Qdrant configuration from environment or Streamlit secrets
            qdrant_url = os.getenv("QDRANT_URL") or st.secrets.get("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY") or st.secrets.get("QDRANT_API_KEY")
            
            if not qdrant_url:
                st.error("Qdrant URL not found. Please set QDRANT_URL in environment or secrets.")
                return False
            
            if qdrant_api_key:
                self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            else:
                self.client = QdrantClient(url=qdrant_url)
            
            # Check if collection exists, create if not
            self.ensure_collection_exists()
            
            logging.info("Successfully connected to Qdrant")
            return True
            
        except Exception as e:
            logging.error(f"Qdrant connection error: {e}")
            st.error(f"Failed to connect to Qdrant: {e}")
            return False
    
    def ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
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
                logging.info(f"Created collection: {self.collection_name}")
            else:
                logging.info(f"Collection {self.collection_name} already exists")
                
        except Exception as e:
            logging.error(f"Error ensuring collection exists: {e}")
            raise
    
    def store_job_vector(self, job_data: Union[Dict[str, Any], List[Dict[str, Any]]], 
                        embedding: Union[List[float], List[List[float]]], 
                        job_id: Union[str, List[str]]) -> bool:
        try:
            # Normalize inputs to always be lists
            if isinstance(job_data, dict):
                jobs_data = [job_data]
                embeddings = [embedding]
                job_ids = [job_id]
            else:
                jobs_data = job_data
                embeddings = embedding
                job_ids = job_id
            
            # Validate input lengths match
            if not (len(jobs_data) == len(embeddings) == len(job_ids)):
                logging.error("Mismatch in lengths of job_data, embeddings, and job_ids")
                return False
            
            points = []
            for jd, emb, jid in zip(jobs_data, embeddings, job_ids):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=emb,
                    payload={
                        "job_id": jid,
                        "title": jd.get("title", ""),
                        "company": jd.get("company", ""),
                        "location": jd.get("location", ""),
                        "department": jd.get("department", ""),
                        "experience_level": jd.get("experience_level", ""),
                        "job_type": jd.get("job_type", ""),
                        "required_skills": jd.get("required_skills", []),
                        "salary_range": jd.get("salary_range", ""),
                        "description": jd.get("description", ""),
                        "summary": jd.get("summary", ""),
                        "created_at": str(jd.get("created_at", "")),
                    }
                )
                points.append(point)
            
            # Store all points
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logging.info(f"Stored {len(points)} job vector(s)")
            return True
            
        except Exception as e:
            logging.error(f"Error storing job vectors: {e}")
            return False
    
    def search_similar_jobs(self, query_vector: List[float], limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[str]:
        """Search for similar jobs using vector similarity, returning only job IDs"""
        try:
            query_filter = None
            if filters:
                conditions = []
                if "department" in filters and filters["department"]:
                    conditions.append(FieldCondition(
                        key="department",
                        match=MatchValue(value=filters["department"])
                    ))
                if "experience_level" in filters and filters["experience_level"]:
                    conditions.append(FieldCondition(
                        key="experience_level",
                        match=MatchValue(value=filters["experience_level"])
                    ))
                if "location" in filters and filters["location"]:
                    conditions.append(FieldCondition(
                        key="location",
                        match=MatchValue(value=filters["location"])
                    ))
                if conditions:
                    query_filter = Filter(must=conditions)

            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=query_filter,
                limit=limit
            )

            job_ids = [result.payload.get("job_id") for result in search_results if result.payload.get("job_id")]
            logging.info(f"Found {len(job_ids)} similar jobs")
            return job_ids

        except Exception as e:
            logging.error(f"Error searching similar jobs: {e}")
            return []
    
    def delete_job_vector(self, job_ids: Union[str, List[str]]) -> Union[bool, List[bool]]:
        """
        Delete job vector(s) by job_id(s).
        
        Args:
            job_ids: Single job ID or list of job IDs
            
        Returns:
            bool or List[bool]: Success status for each deletion
        """
        try:
            # Normalize input to always be a list
            if isinstance(job_ids, str):
                ids_to_delete = [job_ids]
                single_job = True
            else:
                ids_to_delete = job_ids
                single_job = False
            
            results = []
            
            for job_id in ids_to_delete:
                try:
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
                        
                        logging.info(f"Deleted vector for job_id: {job_id}")
                        results.append(True)
                    else:
                        logging.warning(f"No vector found for job_id: {job_id}")
                        results.append(False)
                        
                except Exception as e:
                    logging.error(f"Error deleting vector for job_id {job_id}: {e}")
                    results.append(False)
            
            # Return single boolean for single job, list for multiple
            return results[0] if single_job else results
            
        except Exception as e:
            logging.error(f"Error in delete_job_vector: {e}")
            return False if isinstance(job_ids, str) else [False] * len(job_ids)
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": info.name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "status": info.status
            }
        except Exception as e:
            logging.error(f"Error getting collection info: {e}")
            return {}
    
    def delete_collection(self) -> bool:
        """Delete the entire collection"""
        try:
            self.client.delete_collection(self.collection_name)
            logging.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            logging.error(f"Error deleting collection: {e}")
            return False