from data.mongodb.MongoClient import MongoDBHandler
from data.embeddings.EmbeddingHandler import EmbeddingHandler
from data.vectordb.QdrantClient import QdrantHandler
from typing import Dict, Any
import logging

class RecommendationsPipeline:
    def __init__(self):
        self.mongo_handler = MongoDBHandler()
        self.embedding_handler = EmbeddingHandler()
        self.vector_handler = QdrantHandler()
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def search_jobs_pipeline(self, resume_text: str, limit: int = 10) -> Dict[str, Any]:
        """
        Pipeline for job search:
        1. Generate resume embedding
        2. Search similar jobs in Qdrant
        3. Retrieve job details from MongoDB
        """
        try:
            self.logger.info("Starting job search pipeline")
            
            # Step 1: Generate resume embedding
            resume_embedding = self.embedding_handler.get_resume_embedding(resume_text)
            
            if not resume_embedding:
                self.logger.error("Failed to generate resume embedding")
                return {"success": False, "error": "Failed to generate resume embedding"}
            
            self.logger.info(f"Generated resume embedding with dimension: {len(resume_embedding)}")
            
            # Step 2: Search similar jobs
            search_results, score = self.vector_handler.search_similar_jobs(
                query_vector=resume_embedding,
                limit=limit,
            )
            
            if not search_results:
                self.logger.info("No similar jobs found")
                return {"success": True, "jobs": [], "count": 0}
            
            # Extract job IDs from search results (assuming search returns list of IDs or objects with IDs)
            if isinstance(search_results[0], dict) and 'id' in search_results[0]:
                job_ids = [result['id'] for result in search_results]
            else:
                job_ids = search_results
            
            self.logger.info(f"Found {len(job_ids)} similar jobs")
            
            # Step 3: Retrieve job details from MongoDB
            jobs = []
            for job_id in job_ids:
                job = self.mongo_handler.get_job_by_id(job_id)
                if job:
                    jobs.append(job)
                else:
                    self.logger.warning(f"Job with ID {job_id} not found in MongoDB")
            
            self.logger.info(f"Retrieved {len(jobs)} job details from MongoDB")
            
            return {
                "success": True,
                "jobs": jobs,
                "scores": score,
                "count": len(jobs)
            }
            
        except Exception as e:
            self.logger.error(f"Error in search jobs pipeline: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return {"success": False, "error": str(e)}
    