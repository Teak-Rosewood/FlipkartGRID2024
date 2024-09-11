from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient

load_dotenv()

SQL_URL = os.getenv('POSTGRESQL_DB_URL')
VECTOR_URL = os.getenv('VECTOR_DB_URL')

client = QdrantClient(VECTOR_URL)
engine = create_async_engine(SQL_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

def get_vector_db():
    return client

async def get_sql_db():
    async with SessionLocal() as session:
        yield session