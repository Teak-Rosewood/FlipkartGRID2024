from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient

load_dotenv()

SQL_URL = os.getenv('POSTGRESQL_DB_URL')
VECTOR_URL = os.getenv('VECTOR_DB_URL')

client = QdrantClient(VECTOR_URL)
engine = create_engine(SQL_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_vector_db():
    return client

def get_sql_db():
    session = SessionLocal()
    try: 
        yield session
    finally:
        session.close()