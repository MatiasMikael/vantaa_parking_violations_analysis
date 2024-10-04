from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
import logging

# Load environment variables from the .env file
load_dotenv()

def load_data():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Connect to the PostgreSQL database using environment variables
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()

    # Truncate the parking_violations table to remove existing data
    cursor.execute('TRUNCATE TABLE parking_violations;')
    conn.commit()
    logging.info("Truncated the parking_violations table to remove existing data.")

    # Read the corrected CSV file with the appropriate separator and encoding
    df = pd.read_csv('Pysakointivirheet_Vantaalla_fixed.csv', encoding='utf-8', sep=';')
    logging.info(f"Read {len(df)} rows from CSV.")
    logging.info(f"Columns in CSV: {df.columns.tolist()}")

    # Map dataframe columns to table columns
    df = df.rename(columns={
        'Virheen tekovuosi': 'year',
        'Paikannimi': 'location_name',
        'Yhteensä': 'total_violations'
    })

    # Combine different variations of location names
    df['location_name'] = df['location_name'].replace(
        regex=[r'^Asematie\b.*'], value='Asematie (Stationsvägen)'
    )
    df['location_name'] = df['location_name'].replace(
        regex=[r'^Neilikkatie\b.*'], value='Neilikkatie (Nejlikvägen)'
    )

    # Convert DataFrame to list of tuples for efficient insertion
    data_tuples = [tuple(x) for x in df[['year', 'location_name', 'total_violations']].to_numpy()]

    # Define the INSERT query
    insert_query = '''
    INSERT INTO parking_violations (
        year, location_name, total_violations
    ) VALUES %s;
    '''

    # Insert the data into the database using execute_values for efficiency
    execute_values(cursor, insert_query, data_tuples)
    conn.commit()
    logging.info(f"Inserted {len(df)} rows into the database.")

    # Close the cursor and connection
    cursor.close()
    conn.close()

    logging.info("Data loaded successfully.")

if __name__ == "__main__":
    load_data()