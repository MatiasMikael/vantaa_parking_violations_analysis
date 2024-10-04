from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables from .env file
load_dotenv()

def create_tables():
    # Connect to the PostgreSQL database using environment variables
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    # Drop the parking_violations table if it exists and create a new one
    cur.execute('''
    DROP TABLE IF EXISTS parking_violations;
    CREATE TABLE parking_violations (
        year INT,
        location_name VARCHAR,
        total_violations INT
    );
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()