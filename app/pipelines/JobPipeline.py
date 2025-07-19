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

            if jobs:
                self.logger.info(f"DEBUG: First job keys: {list(jobs[0].keys())}")
                self.logger.info(f"DEBUG: First job sample: {dict(list(jobs[0].items())[:3])}")

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
                    
                    # DEBUG: Check job structure before embedding
                    self.logger.info(f"DEBUG: Job {i+1} keys: {list(job.keys())}")
                    
                    # Pass single job as a list (since get_job_embeddings expects List[dict])
                    # and get back a list with one embedding
                    job_embeddings = self.embedding_handler.get_job_embeddings([job])
                    
                    if job_embeddings and len(job_embeddings) > 0:
                        # Extract the single embedding from the list
                        embedding = job_embeddings[0]
                        embeddings.append(embedding)
                        self.logger.info(f"✓ Generated embedding for job {i+1}/{job_count} - dimension: {len(embedding)}")
                        
                        # DEBUG: Check embedding type and first few values
                        self.logger.info(f"DEBUG: Embedding type: {type(embedding)}, first 3 values: {embedding[:3]}")
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

            # Step 3: Store vectors in Qdrant
            self.logger.info("Storing vectors in Qdrant...")
            vector_results = []
            successful_jobs = []

            # Process each valid job, embedding, job_id tuple
            for i, (job, embedding, job_id) in enumerate(valid_data):
                try:
                    self.logger.info(f"Storing vector for job {i+1}/{len(valid_data)}: {job.get('job_title', 'No title')} (ID: {job_id})")
                    
                    # DEBUG: Check data before storing
                    self.logger.info(f"DEBUG: Job ID type: {type(job_id)}, value: {job_id}")
                    self.logger.info(f"DEBUG: Embedding type: {type(embedding)}, length: {len(embedding)}")
                    self.logger.info(f"DEBUG: Job data keys: {list(job.keys())}")
                    
                    # Check if vector handler is properly initialized
                    if self.vector_handler.client is None:
                        self.logger.error("Vector handler client is None - connection failed")
                        vector_results.append(False)
                        continue
                    
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
                    import traceback
                    self.logger.error(f"Traceback: {traceback.format_exc()}")
                    vector_results.append(False)

            successful_vectors = sum(vector_results)
            self.logger.info(f"Successfully stored {successful_vectors}/{len(valid_data)} vectors")

            # DEBUG: Check Qdrant collection status after storing
            try:
                collection_info = self.vector_handler.get_collection_info()
                self.logger.info(f"DEBUG: Collection info after storing: {collection_info}")
            except Exception as e:
                self.logger.error(f"DEBUG: Failed to get collection info: {e}")

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


    def delete_job_pipeline(self, job_id: str) -> Dict[str, Any]:
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