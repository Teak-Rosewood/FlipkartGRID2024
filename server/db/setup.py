import os
import subprocess

def run_migrations():
    """Run Alembic migrations to upgrade the database schema."""
    # Ensure alembic is installed
    try:
        import alembic.config
    except ImportError:
        raise ImportError("Alembic is not installed. Run `pip install alembic` to install it.")
    
    # Path to Alembic's configuration file (adjust path as needed)
    alembic_cfg_path = os.path.join(os.getcwd(), "alembic.ini")

    if os.path.exists(alembic_cfg_path):
        # Run Alembic upgrade to the latest migration
        print("Running Alembic migrations...")
        try:
            result = subprocess.run(["alembic", "upgrade", "head"], check=True, capture_output=True, text=True)
            print("Database migrations completed successfully.")
            print(result.stdout)  # Optional: Print the stdout from Alembic
        except subprocess.CalledProcessError as e:
            print("Error during Alembic migration:")
            print(e.stderr)  # Print the stderr from Alembic
    else:
        print("Alembic config not found. Please initialize Alembic.")

def generate_migration(message):
    """Generate a new Alembic migration script."""
    # Ensure alembic is installed
    try:
        import alembic.config
    except ImportError:
        raise ImportError("Alembic is not installed. Run `pip install alembic` to install it.")
    
    # Path to Alembic's configuration file (adjust path as needed)
    alembic_cfg_path = os.path.join(os.getcwd(), "alembic.ini")

    if os.path.exists(alembic_cfg_path):
        print(f"Generating new migration script: {message}")
        try:
            result = subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], check=True, capture_output=True, text=True)
            print("Migration script generated successfully.")
            print(result.stdout)  # Optional: Print the stdout from Alembic
        except subprocess.CalledProcessError as e:
            print("Error during Alembic migration script generation:")
            print(e.stderr)  # Print the stderr from Alembic
    else:
        print("Alembic config not found. Please initialize Alembic.")

if __name__ == "__main__":
    print("Setting up the project...")
    
    # Add more setup tasks if needed (installing packages, etc.)

    # Generate a new migration script
    migration_message = "Description of the changes"
    generate_migration(migration_message)

    # Run Alembic migrations as part of the setup
    run_migrations()
