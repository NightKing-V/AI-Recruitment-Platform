from services.JobHandler import jobHandler
from data.mongodb.MongoClient import MongoDBHandler
from data.embeddings.EmbeddingHandler import EmbeddingHandler




class JobPipeline:
    def __init__ (self):
        self.job_handler = jobHandler()
        self.mongo_handler = MongoDBHandler()
        self.embedding_handler = EmbeddingHandler()
        
    def generation_pipeline(self, job_num: int, job_domain: list) -> list:
        
        jobs = self.job_handler.generate_job_descriptions(
            job_num=job_num,
            job_domain=job_domain
        )
        
        job_ids = self.mongo_handler.store_jobs(jobs)
        self.embedding_handler.get_embeddings(jobs)