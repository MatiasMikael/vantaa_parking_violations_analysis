# Vantaa Parking Violations Analysis

This project analyzes parking violations in Vantaa, Finland, based on open data provided by Vantaa's City Environment Division. The data includes information on parking violations from 2015 to 2021 across various locations in Vantaa.

## Project Overview
The project consists of four main parts:
1. **Fixing Special Characters**: The data is preprocessed to fix incorrect or garbled special characters (e.g., ä, ö, å).
2. **Creating Tables**: A PostgreSQL table is created to store parking violations data.
3. **Loading Data**: A cleaned CSV file containing parking violations is loaded into the PostgreSQL database.
4. **Running Queries**: Several SQL queries are executed to generate insights from the data, including the total violations per year and the top 10 locations with the most violations.

## Data Source
The data used in this project is open data available from (https://www.avoindata.fi/data/fi/dataset/pysakointivirheet-vantaalla). The dataset is provided under the Creative Commons Attribution 4.0 International License.

### CSV File: `Pysakointivirheet_Vantaalla_fixed.csv`
The data file used in this project is a cleaned version of the original, formatted to correct any inconsistencies, especially regarding special characters.

## Setup

### Clone the repository
```bash
git clone https://github.com/MatiasMikael/vantaa_parking_violations_analysis.git
cd vantaa_parking_violations_analysis
```
```pip install -r requirements.txt
```
The project uses environment variables to store database connection information. You will need to create a .env file in the root of the project with the following format:
```DB_NAME=pysakointi_data
DB_USER=postgres
DB_PASS=your_database_password_here
DB_HOST=localhost
DB_PORT=5433
```
**Note:** Do not share your password or commit it to version control. Ensure your .env file is listed in .gitignore to keep it private.
```python fix_special_characters.py```
```python create_tables.py```
```python load_data.py
```

## Scripts

### `fix_special_characters.py`
This script reads the original CSV file (`Pysakointivirheet_Vantaalla.csv`), fixes issues with special characters (ä, ö, å), and saves the corrected data to `Pysakointivirheet_Vantaalla_fixed.csv`. If the CSV has mixed encoding, it attempts to handle both ISO-8859-1 and Windows-1252 encodings.

### `create_tables.py`
This script creates the `parking_violations` table in the PostgreSQL database. If the table already exists, it will be dropped and recreated.

### `load_data.py`
This script loads the cleaned CSV file `Pysakointivirheet_Vantaalla_fixed.csv` into the `parking_violations` table. It reads the CSV, processes the data, and inserts it efficiently using the `psycopg2` `execute_values` method.

### `queries.py`
This script runs three main queries on the database:

1. **Total Violations Per Year**: The total number of parking violations per year from 2015 to 2021.
2. **Top 10 Locations with Most Violations**: The top 10 locations with the highest number of violations across all years.
3. **Violations Per Year for Asematie (Stationsvägen)**: A detailed look at violations that occurred on Asematie (Stationsvägen), a street near the Tikkurila station.

The results of these queries are saved as CSV files:
- `query_results_total_violations_per_year.csv`
- `query_results_top_locations.csv`
- `query_results_top_location_per_year.csv`

## Queries and Results

### Query: Total Violations Per Year
The data shows the total number of parking violations per year from 2015 to 2021. These results can be found in `query_results_total_violations_per_year.csv`.

### Query: Top 10 Locations with Most Violations
This query lists the top 10 locations in Vantaa with the most parking violations from 2015 to 2021. The results are saved in `query_results_top_locations.csv`. Note that this file includes all violations across the entire period.

### Query: Violations at Asematie (Stationsvägen)
The number of parking violations at Asematie for each year is detailed in `query_results_top_location_per_year.csv`. **Note:** The lower numbers of violations in 2018 and 2019 are likely due to construction work on Asematie, according to information found through online searches.

## License
This work is licensed under the MIT License, but the data used in this project is provided by the City of Vantaa and published under the Creative Commons Attribution 4.0 International License: https://creativecommons.org/licenses/by/4.0/.
