import os
import subprocess

def run_migrations():
    # Ensure alembic is installed
    try:
        import alembic.config
    except ImportError:
        raise ImportError("Alembic is not installed. Run `pip install alembic` to install it.")

    # Path to Alembic's migration folder (adjust path as needed)
    alembic_cfg = os.path.join(os.getcwd(), "alembic.ini")

    if os.path.exists(alembic_cfg):
        # Run Alembic upgrade to the latest migration
        print("Running Alembic migrations...")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Database migrations completed.")
    else:
        print("Alembic config not found. Please initialize Alembic.")

if __name__ == "__main__":
    print("Setting up the project...")
    
    # Add more setup tasks if needed (installing packages, etc.)
    
    # Run Alembic migrations as part of the setup
    run_migrations()
