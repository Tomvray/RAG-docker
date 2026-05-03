import faiss
from FlagEmbedding import FlagModel

corpus = [
    "Michael Jackson was a legendary pop icon known for his record-breaking music and dance innovations. Fei-Fei Li is a professor in Stanford University, revolutionized computer vision with the ImageNet project.",
    "Brad Pitt is a versatile actor and producer known for his roles in films like 'Fight Club' and 'Once Upon a Time in Hollywood.'",
    "Geoffrey Hinton, as a foundational figure in AI, received Turing Award for his contribution in deep learning.",
    "Eminem is a renowned rapper and one of the best-selling music artists of all time.",
    "Taylor Swift is a Grammy-winning singer-songwriter known for her narrative-driven music.",
    "Sam Altman leads OpenAI as its CEO, with astonishing works of GPT series and pursuing safe and beneficial AI.",
    "Morgan Freeman is an acclaimed actor famous for his distinctive voice and diverse roles.",
    "Andrew Ng spread AI knowledge globally via public courses on Coursera and Stanford University.",
    "Robert Downey Jr. is an iconic actor best known for playing Iron Man in the Marvel Cinematic Universe.",
]

# get the BGE embedding model
model = FlagModel('BAAI/bge-m3',
                  use_fp16=True)

# get the embedding of the corpus
corpus_embeddings = model.encode(corpus)['dense_vecs']

print("shape of the corpus embeddings:", corpus_embeddings.shape)
print("data type of the embeddings: ", corpus_embeddings.dtype)

import numpy as np

corpus_embeddings = corpus_embeddings.astype(np.float32)

import faiss

# get the length of our embedding vectors, vectors by bge-base-en-v1.5 have length 768
dim = corpus_embeddings.shape[-1]

# create the faiss index and store the corpus embeddings into the vector space
index = faiss.index_factory(dim, 'Flat', faiss.METRIC_INNER_PRODUCT)

# if you installed faiss-gpu, uncomment the following lines to make the index on your GPUs.

# co = faiss.GpuMultipleClonerOptions()
# index = faiss.index_cpu_to_all_gpus(index, co)