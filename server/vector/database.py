import os

from constants import *

from qdrant_client import QdrantClient

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, cache_folder=EMBEDDING_MODEL_DIR)
url = os.getenv('VECTOR_DB_URL') + os.getenv('VECTOR_DB_HTTP_PORT')
client =  QdrantClient(url=url)
vector_store = QdrantVectorStore (
        client = client,
        embedding = embeddings,
        collection_name="products"
    )

def get_n_similar_value(text, n):
    res = vector_store.similarity_search(text, k = n)
    return res
    
