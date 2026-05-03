# build_chroma_db.py

import os
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "chroma_db"
COLLECTION_NAME = "documents"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

documents = {
    "document1.txt": "i love ice cream .",
    "document2.txt": "it is sunny .",
    "document3.txt": "we have a prime minister ."
}

for filename, text in documents.items():
    print(f"Processing: {filename}, Text: {text}")
    embedding = model.encode(text).tolist()

    collection.add(
        ids=[filename],
        embeddings=[embedding]
    )

    print(f"Added: {filename}")

print("Done.")
print(f"Database saved in: {DB_PATH}")

#get the closest document to the query "it is raining ."
query = "I would love to eat"
query_embedding = model.encode(query).tolist()
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
#print the results
print("Query:", query)
print("Closest document:", results['ids'][0][0])
#for document in results['ids'][0]:
#    print(similarity_score)

print("Distances:", results['distances'])
