from database import Database
from sentence_transformers import SentenceTransformer
import faiss

print(faiss.__version__)
class Pipeline:
    def __init__(self):
        self.db = Database(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password=" "
        )
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(384) # 384 is the dimension of the embedding


    def embedd_claims(self):
        #get all patent IDs that have claims in the database
        patent_ids = self.db.get_claims_ids()

        for patent_id in patent_ids:
            claims_str = self.db.get_claims_str(patent_id)
            #embed claims_str using openai embeddings API
            embedding = self.model.encode(claims_str)
            #store embedding in faiss index


     

if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.embedd_claims()