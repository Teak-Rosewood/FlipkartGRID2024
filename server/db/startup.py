from sqlalchemy import create_engine
from models import Base
import os

POSTGRES_URL = os.getenv('POSTGRESQL_DB_URL')

engine = create_engine