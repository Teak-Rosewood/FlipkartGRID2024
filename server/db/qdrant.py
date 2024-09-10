from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

def get_vector_db(): 
    return client