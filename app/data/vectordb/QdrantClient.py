import os
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import uuid
import streamlit as st

class QdrantHandler:
    """Handle Qdrant vector database operations for job matching"""
    
    def __init__(self, collection_name: str = "jobs"):
        self.client = None
        self.collection_name = collection_name
        self.vector_size = 1536  # OpenAI embedding size
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
    
    def store_job_vector(self, job_data: Dict[str, Any], embedding: List[float], job_id: str) -> bool:
        """Store job vector in Qdrant"""
        try:
            # Create point with vector and metadata
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "job_id": job_id,
                    "title": job_data.get("title", ""),
                    "company": job_data.get("company", ""),
                    "location": job_data.get("location", ""),
                    "department": job_data.get("department", ""),
                    "experience_level": job_data.get("experience_level", ""),
                    "job_type": job_data.get("job_type", ""),
                    "required_skills": job_data.get("required_skills", []),
                    "salary_range": job_data.get("salary_range", ""),
                    "description": job_data.get("description", ""),
                    "summary": job_data.get("summary", ""),
                    "created_at": str(job_data.get("created_at", "")),
                }
            )
            
            # Upload point
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logging.info(f"Stored vector for job: {job_data.get('title', 'Unknown')}")
            return True
            
        except Exception as e:
            logging.error(f"Error storing job vector: {e}")
            return False
    
    def store_multiple_job_vectors(self, jobs_data: List[Dict[str, Any]], embeddings: List[List[float]], job_ids: List[str]) -> int:
        """Store multiple job vectors in Qdrant"""
        try:
            points = []
            
            for job_data, embedding, job_id in zip(jobs_data, embeddings, job_ids):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "job_id": job_id,
                        "title": job_data.get("title", ""),
                        "company": job_data.get("company", ""),
                        "location": job_data.get("location", ""),
                        "department": job_data.get("department", ""),
                        "experience_level": job_data.get("experience_level", ""),
                        "job_type": job_data.get("job_type", ""),
                        "required_skills": job_data.get("required_skills", []),
                        "salary_range": job_data.get("salary_range", ""),
                        "description": job_data.get("description", ""),
                        "summary": job_data.get("summary", ""),
                        "created_at": str(job_data.get("created_at", "")),
                    }
                )
                points.append(point)
            
            # Upload all points
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logging.info(f"Stored {len(points)} job vectors")
            return len(points)
            
        except Exception as e:
            logging.error(f"Error storing multiple job vectors: {e}")
            return 0
    
    def search_similar_jobs(self, query_vector: List[float], limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar jobs using vector similarity"""
        try:
            # Prepare filters if provided
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
            
            # Search for similar vectors
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=query_filter,
                limit=limit
            )
            
            # Format results
            results = []
            for result in search_results:
                job_match = {
                    "similarity_score": result.score,
                    "job_id": result.payload.get("job_id"),
                    "title": result.payload.get("title"),
                    "company": result.payload.get("company"),
                    "location": result.payload.get("location"),
                    "department": result.payload.get("department"),
                    "experience_level": result.payload.get("experience_level"),
                    "job_type": result.payload.get("job_type"),
                    "required_skills": result.payload.get("required_skills", []),
                    "salary_range": result.payload.get("salary_range"),
                    "description": result.payload.get("description"),
                    "summary": result.payload.get("summary"),
                }
                results.append(job_match)
            
            logging.info(f"Found {len(results)} similar jobs")
            return results
            
        except Exception as e:
            logging.error(f"Error searching similar jobs: {e}")
            return []
    
    def delete_job_vector(self, job_id: str) -> bool:
        """Delete job vector by job_id"""
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
                return True
            else:
                logging.warning(f"No vector found for job_id: {job_id}")
                return False
                
        except Exception as e:
            logging.error(f"Error deleting job vector: {e}")
            return False
    
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