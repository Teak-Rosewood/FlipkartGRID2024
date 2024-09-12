import os

from constants import *

from qdrant_client import QdrantClient

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import VectorParams, Distance

def create_collection(collection, client):
    
    if client.collection_exists(collection):
        print("Collection exits: products")
        return
    client.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE)
    )
    print("Created collection:", collection)

def setup_vector_db():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, cache_folder=EMBEDDING_MODEL_DIR)
    url = os.getenv('VECTOR_DB_URL') + os.getenv('VECTOR_DB_HTTP_PORT')
    client =  QdrantClient(url=url)
    QdrantVectorStore (
        client = client,
        embedding = embeddings,
        collection_name="products"
    )
    create_collection("products", client)
    print("Initialized Vector DB")