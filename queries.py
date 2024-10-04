from dotenv import load_dotenv
import os
import psycopg2
import csv

# Load environment variables from .env file
load_dotenv()

def run_queries():
    # Connect to the PostgreSQL database using environment variables
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = connection.cursor()

    # Query 1: Total violations per year
    cursor.execute("""
    SELECT year, SUM(total_violations) AS total_violations
    FROM parking_violations
    GROUP BY year
    ORDER BY year;
    """)
    results_year = cursor.fetchall()

    # Save Query 1 results to CSV with formatted numbers
    with open('query_results_total_violations_per_year.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Total Violations'])
        formatted_results_year = [(row[0], "{:,}".format(row[1])) for row in results_year]
        writer.writerows(formatted_results_year)

    # Query 2: Top 10 locations with most violations overall
    cursor.execute("""
    SELECT location_name, SUM(total_violations) AS total_violations
    FROM parking_violations
    GROUP BY location_name
    ORDER BY total_violations DESC
    LIMIT 10;
    """)
    results_top_locations = cursor.fetchall()

    # Save Query 2 results to CSV with formatted numbers
    with open('query_results_top_locations.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Location', 'Total Violations'])
        formatted_results_top_locations = [(row[0], "{:,}".format(row[1])) for row in results_top_locations]
        writer.writerows(formatted_results_top_locations)

    # Query 3: Violations per year for Asematie (Stationsvägen)
    cursor.execute("""
    SELECT year, SUM(total_violations) AS total_violations
    FROM parking_violations
    WHERE location_name LIKE 'Asematie%'
    GROUP BY year
    ORDER BY year;
    """)
    results_top_location_per_year = cursor.fetchall()

    # Save Query 3 results to CSV with formatted numbers
    with open('query_results_top_location_per_year.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Total Violations at Asematie (Stationsvägen)'])
        formatted_results = [(row[0], "{:,}".format(row[1])) for row in results_top_location_per_year]
        writer.writerows(formatted_results)

    print("Results saved to files: query_results_total_violations_per_year.csv, query_results_top_locations.csv, query_results_top_location_per_year.csv")

    # Close the cursor and connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    run_queries()