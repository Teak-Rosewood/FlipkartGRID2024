from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQL_URL = os.getenv('POSTGRESQL_DB_URL')

engine = create_engine(SQL_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_sql_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def save_record(record):
    db = SessionLocal()
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def save_multiple_records(records):
    db = SessionLocal()
    try:
        for record in records:
            db.add(record)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()