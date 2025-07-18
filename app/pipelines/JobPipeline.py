from data.mongodb.MongoClient import MongoDBHandler
from data.embeddings.EmbeddingHandler import EmbeddingHandler
from data.vectordb.QdrantClient import QdrantHandler
import logging
from typing import List, Dict, Any, Optional, Union


class JobPipeline:
    def __init__(self):
        self.mongo_handler = MongoDBHandler()
        self.embedding_handler = EmbeddingHandler()
        self.vector_handler = QdrantHandler()
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def job_pipeline(self, jobs_data) -> Dict[str, Any]:
        try:
            # Normalize input to always be a list
            if isinstance(jobs_data, dict):
                jobs = [jobs_data]
                single_job = True
            else:
                jobs = jobs_data
                single_job = False

            job_count = len(jobs)
            self.logger.info(f"Starting job pipeline for {job_count} job(s)")

            # Validate jobs data
            if not jobs or job_count == 0:
                self.logger.error("No jobs provided")
                return {"success": False, "error": "No jobs provided"}

            # Step 1: Store jobs in MongoDB
            self.logger.info("Storing jobs in MongoDB...")
            job_ids = self.mongo_handler.store_jobs(jobs)

            if not job_ids:
                self.logger.error("Failed to store jobs in MongoDB")
                return {"success": False, "error": "Failed to store jobs in MongoDB"}

            if len(job_ids) != job_count:
                self.logger.warning(f"Expected {job_count} job IDs, got {len(job_ids)}")

            self.logger.info(f"Stored {len(job_ids)} jobs in MongoDB with IDs: {job_ids}")

            # Step 2: Generate embeddings per job to maintain alignment
            self.logger.info("Generating embeddings for each job...")
            embeddings = []
            
            for i, job in enumerate(jobs):
                try:
                    self.logger.info(f"Processing job {i+1}/{job_count}: {job.get('job_title', 'No title')}")
                    
                    # Pass single job as a list (since get_job_embeddings expects List[dict])
                    # and get back a list with one embedding
                    job_embeddings = self.embedding_handler.get_job_embeddings([job])
                    
                    if job_embeddings and len(job_embeddings) > 0:
                        # Extract the single embedding from the list
                        embedding = job_embeddings[0]
                        embeddings.append(embedding)
                        self.logger.info(f"✓ Generated embedding for job {i+1}/{job_count} - dimension: {len(embedding)}")
                    else:
                        self.logger.error(f"✗ Failed to generate embedding for job {i+1}/{job_count}")
                        # Add None to maintain alignment
                        embeddings.append(None)
                        
                except Exception as e:
                    self.logger.error(f"✗ Error generating embedding for job {i+1}: {e}")
                    # Add None to maintain alignment
                    embeddings.append(None)

            # Filter out None embeddings and corresponding jobs/job_ids
            valid_data = []
            for i, (job, embedding, job_id) in enumerate(zip(jobs, embeddings, job_ids)):
                if embedding is not None:
                    valid_data.append((job, embedding, job_id))
                else:
                    self.logger.warning(f"Skipping job {i+1} due to embedding failure")
            
            if not valid_data:
                self.logger.error("No valid embeddings generated")
                return {"success": False, "error": "No valid embeddings generated"}

            self.logger.info(f"Generated {len(valid_data)} valid embeddings out of {job_count} jobs")

            if not embeddings:
                self.logger.error("Failed to generate any embeddings")
                return {"success": False, "error": "Failed to generate embeddings"}

            if len(embeddings) != len(job_ids):
                self.logger.warning(f"Mismatch: {len(embeddings)} embeddings vs {len(job_ids)} job IDs")

            # Step 3: Store vectors in Qdrant
            self.logger.info("Storing vectors in Qdrant...")
            vector_results = []
            successful_jobs = []

            # Process each valid job, embedding, job_id tuple
            for i, (job, embedding, job_id) in enumerate(valid_data):
                try:
                    self.logger.info(f"Storing vector for job {i+1}/{len(valid_data)}: {job.get('job_title', 'No title')} (ID: {job_id})")
                    
                    success = self.vector_handler.store_job_vector(
                        job_data=job,
                        embedding=embedding,
                        job_id=job_id
                    )
                    
                    vector_results.append(success)
                    
                    if success:
                        successful_jobs.append(job_id)
                        self.logger.info(f"✓ Stored vector for job {i+1}/{len(valid_data)}")
                    else:
                        self.logger.error(f"✗ Failed to store vector for job {i+1}/{len(valid_data)}")

                except Exception as e:
                    self.logger.error(f"✗ Error storing vector for job {i+1}: {e}")
                    vector_results.append(False)

            successful_vectors = sum(vector_results)
            self.logger.info(f"Successfully stored {successful_vectors}/{len(valid_data)} vectors")

            # Final validation - check if any jobs were actually stored
            if successful_vectors == 0:
                self.logger.error("No vectors were successfully stored in Qdrant")
                return {
                    "success": False, 
                    "error": "No vectors were successfully stored in Qdrant",
                    "jobs_processed": job_count,
                    "jobs_stored": len(job_ids),
                    "embeddings_generated": len(valid_data),
                    "vectors_stored": successful_vectors
                }

            result = {
                "success": True,
                "jobs_processed": job_count,
                "jobs_stored": len(job_ids),
                "embeddings_generated": len(valid_data),
                "vectors_stored": successful_vectors,
                "job_ids": job_ids,
                "successful_job_ids": successful_jobs
            }

            self.logger.info(f"Pipeline completed successfully: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Error in job pipeline: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return {"success": False, "error": str(e)}

    def search_jobs_pipeline(self, resume_text: str, filters: Optional[Dict[str, Any]] = None, limit: int = 10) -> Dict[str, Any]:
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
            search_results = self.vector_handler.search_similar_jobs(
                query_vector=resume_embedding,
                limit=limit,
                filters=filters
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
                "count": len(jobs)
            }
            
        except Exception as e:
            self.logger.error(f"Error in search jobs pipeline: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return {"success": False, "error": str(e)}
    
    def delete_job_pipeline(self, job_id: str) -> Dict[str, Any]:
        """
        Pipeline for deleting a single job:
        1. Delete from MongoDB
        2. Delete vector from Qdrant

        Args:
            job_id: Single job ID string
        """
        try:
            self.logger.info(f"Starting job deletion pipeline for job ID: {job_id}")

            # Step 1: Delete from MongoDB
            job_deleted = self.mongo_handler.delete_job(job_id)
            if not job_deleted:
                self.logger.error(f"Failed to delete job from MongoDB: {job_id}")
                return {
                    "success": False,
                    "job_id": job_id,
                    "job_deleted": False,
                    "vector_deleted": False,
                    "error": f"Failed to delete job from MongoDB: {job_id}"
                }
            else:
                self.logger.info(f"Successfully deleted job from MongoDB: {job_id}")

            # Step 2: Delete vector from Qdrant
            vector_deleted = self.vector_handler.delete_job_vector(job_id)
            if not vector_deleted:
                self.logger.error(f"Failed to delete job vector from Qdrant: {job_id}")
            else:
                self.logger.info(f"Successfully deleted job vector from Qdrant: {job_id}")

            return {
                "success": True,
                "job_id": job_id,
                "job_deleted": True,
                "vector_deleted": bool(vector_deleted)
            }

        except Exception as e:
            self.logger.error(f"Error in deleting job: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return {"success": False, "error": str(e)}
