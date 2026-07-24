import sys
import time
# pyrefly: ignore [missing-import]
from sqlalchemy import text

# Add the current directory to python path to import the app module
sys.path.append(".")

try:
    from app.database import engine, DATABASE_URL
except ImportError as e:
    print("[ERROR] Could not import database configuration from 'app.database'.")
    print(f"Details: {e}")
    sys.exit(1)

def test_db_connection():
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    print(f"Target URL: {DATABASE_URL}")
    print("Connecting to database...")
    
    start_time = time.time()
    try:
        # Create a connection and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            val = result.scalar()
            elapsed_time = time.time() - start_time
            
            if val == 1:
                print(f"Response time: {elapsed_time:.3f} seconds")
                print("\n[SUCCESS] Database is connected and responding properly!")
                print("=" * 60)
                return True
            else:
                print(f"\n[WARNING] Connection succeeded but query returned unexpected value: {val}")
                print("=" * 60)
                return False
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"Failed after {elapsed_time:.3f} seconds")
        print("\n[CONNECTION FAILED]")
        print("-" * 60)
        print("Detailed Error Message:")
        print(e)
        print("-" * 60)
        print("\nPlease check the following:")
        print("1. Is your PostgreSQL database server running?")
        print("2. Are the host (localhost), port (5432), user (postgres), and password correct?")
        print("3. Does the database 'notes-api-fastapi' exist?")
        print("=" * 60)
        return False

if __name__ == "__main__":
    test_db_connection()
