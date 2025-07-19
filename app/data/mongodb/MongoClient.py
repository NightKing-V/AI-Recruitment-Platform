import os
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Dict, List, Optional, Any
from datetime import datetime
import streamlit as st
from bson import ObjectId


class MongoDBHandler:
    def __init__(self):
        self.client = None
        self.db = None
        self.jobs_collection = None
        self.resumes_collection = None
        self.connect()
    
    def connect(self):
        # Connect to MongoDB
        try:
            # Get MongoDB connection string from environment or Streamlit secrets
            mongo_uri = os.getenv("MONGODB_URI") or st.secrets.get("MONGODB_URI")
            db_name = os.getenv("MONGODB_DB") or st.secrets.get("MONGODB_DB") or "recruitment_platform"
            jobs_collection_name = os.getenv("MONGODB_JOBS_COLLECTION") or st.secrets.get("MONGODB_JOBS_COLLECTION") or "jobs"
            resumes_collection_name = os.getenv("MONGODB_RESUMES_COLLECTION") or st.secrets.get("MONGODB_RESUMES_COLLECTION") or "resumes"

            if not mongo_uri:
                st.error("MongoDB URI not found. Please set MONGODB_URI in environment or secrets.")
                return False

            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
            self.jobs_collection = self.db[jobs_collection_name]
            self.resumes_collection = self.db[resumes_collection_name]
            
            # Test connection
            self.client.admin.command('ping')
            logging.info("Successfully connected to MongoDB")
            return True
            
        except PyMongoError as e:
            logging.error(f"MongoDB connection error: {e}")
            st.error(f"Failed to connect to MongoDB: {e}")
            return False
    
    def store_jobs(self, jobs_data: Any) -> Optional[List[str]]:
        try:
            if isinstance(jobs_data, dict):
                # Single job
                jobs_data["created_at"] = datetime.now()
                jobs_data["updated_at"] = datetime.now()
                result = self.jobs_collection.insert_one(jobs_data)
                logging.info(f"Job stored with ID: {result.inserted_id}")
                return [str(result.inserted_id)]
            
            elif isinstance(jobs_data, list):
                # Multiple jobs
                for job in jobs_data:
                    job["created_at"] = datetime.now()
                    job["updated_at"] = datetime.now()
                result = self.jobs_collection.insert_many(jobs_data)
                job_ids = [str(id) for id in result.inserted_ids]
                logging.info(f"Stored {len(job_ids)} jobs")
                return job_ids
            else:
                logging.error("Invalid input type for store_jobs. Must be dict or list of dicts.")
                st.error("Invalid input type for store_jobs. Must be dict or list of dicts.")
                return None
        except PyMongoError as e:
            logging.error(f"Error storing job(s): {e}")
            st.error(f"Failed to store job(s): {e}")
            return None
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        try:

            job = self.jobs_collection.find_one({"_id": ObjectId(job_id)})
            if job:
                job["_id"] = str(job["_id"])
            return job
            
        except (PyMongoError, Exception) as e:
            logging.error(f"Error retrieving job: {e}")
            return None
    
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        try:
            jobs = list(self.jobs_collection.find().sort("created_at", -1))
            
            # Convert ObjectId to string
            for job in jobs:
                job["_id"] = str(job["_id"])
            
            return jobs
            
        except PyMongoError as e:
            logging.error(f"Error retrieving jobs: {e}")
            return []

    
    def delete_job(self, job_id: str) -> bool:
        try:
            result = self.jobs_collection.delete_one({"_id": ObjectId(job_id)})
            return result.deleted_count > 0
            
        except (PyMongoError, Exception) as e:
            logging.error(f"Error deleting job: {e}")
            return False
    
    def store_resume(self, resume_data: Dict[str, Any]) -> Optional[str]:
        try:
            # Add metadata
            resume_data["created_at"] = datetime.now()
            resume_data["updated_at"] = datetime.now()
            
            # Insert resume
            result = self.resumes_collection.insert_one(resume_data)
            
            logging.info(f"Resume stored with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except PyMongoError as e:
            logging.error(f"Error storing resume: {e}")
            st.error(f"Failed to store resume: {e}")
            return None
    
    def get_jobs_count(self) -> int:
        try:
            return self.jobs_collection.count_documents({})
        except PyMongoError as e:
            logging.error(f"Error counting jobs: {e}")
            return 0

    def close_connection(self):
        # Close MongoDB connection
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed")
            
                
    def search_jobs(self, search_term: str = "") -> List[Dict[str, Any]]:
        """Search jobs by a text term using regex (no index required)"""
        try:
            if not search_term or not search_term.strip():
                # Return all jobs if no search term
                jobs = list(self.jobs_collection.find().sort("created_at", -1))
            else:
                search_term = search_term.strip()
                
                # Use regex search (case-insensitive)
                regex_pattern = {"$regex": search_term, "$options": "i"}
                query = {
                    "$or": [
                        {"job_title": regex_pattern},
                        {"company": regex_pattern},
                        {"summary": regex_pattern},
                        {"location": regex_pattern},
                        {"employment_type": regex_pattern},
                        {"experience_level": regex_pattern},
                        {"required_skills": {"$elemMatch": {"$regex": search_term, "$options": "i"}}}
                    ]
                }
                jobs = list(self.jobs_collection.find(query).limit(limit).sort("created_at", -1))

            # Convert ObjectId to string
            for job in jobs:
                job["_id"] = str(job["_id"])

            return jobs

        except PyMongoError as e:
            logging.error(f"Error searching jobs: {e}")
            return []
