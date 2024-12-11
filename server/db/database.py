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
    db = get_sql_db()
    db.session.add(record)
    db.session.commit()

def save_multiple_records(records):
    db = get_sql_db()
    for record in records:
        db.session.add(record)
    db.session.commit()