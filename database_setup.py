import pandas as pd
import logging
from config import get_database_engine

logging.basicConfig(level=logging.INFO)

def create_and_populate_db(csv_path: str):
    """
    Creates (or replaces) a PostgreSQL database table with data from a CSV.

    - csv_path: path to the CSV file
    """
    try:
        # 1. Read CSV
        df = pd.read_csv(csv_path)
        logging.info(f"Loaded CSV data: {df.shape[0]} rows, {df.shape[1]} columns.")

        # 2. Create a database engine
        engine = get_database_engine()

        # 3. Write DataFrame to the database
        df.to_sql('my_data_table', con=engine, if_exists='replace', index=False)
        logging.info("Data successfully written to 'my_data_table'.")
    except Exception as e:
        logging.error(f"Error creating or populating database: {e}")

if __name__ == "__main__":
    create_and_populate_db('time_slot.csv')
