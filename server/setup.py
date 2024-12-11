from db.setup import setup_sql_db
from vector.setup import setup_vector_db

from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    setup_sql_db()
    # setup_vector_db()
    print("Setup complete")