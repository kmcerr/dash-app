import pandas as pd
import logging
from config import get_database_engine

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

def load_data_from_db():
    """
    Load data from the PostgreSQL database (table: 'my_data_table').
    Performs transformations and returns a cleaned DataFrame.
    """
    try:
        engine = get_database_engine()
        df = pd.read_sql('SELECT * FROM my_data_table', con=engine)

        # Transformations (e.g., date parsing)
        df['date'] = pd.to_datetime(df['date'])
        df['month_year'] = df['date'].dt.to_period('M').astype(str)
        df['month'] = pd.Categorical(df['date'].dt.strftime('%b'), categories=MONTHS, ordered=True)
        df['year'] = df['date'].dt.year
        df['day'] = df['date'].dt.day_name()
        # Convert time to HH:MM format
        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.strftime('%H:%M')

        # Categorize month for proper ordering
        df['month'] = pd.Categorical(df['month'], categories=MONTHS, ordered=True)

        # Map 'received' column to more human-readable values
        received_mapping = {
            1: 'Received', 0: 'Not Received',
            '1': 'Received', '0': 'Not Received',
            'received': 'Received', 'not_received': 'Not Received'
        }
        df['received'] = df['received'].map(received_mapping)

        return df.sort_values(by=['year', 'month', 'time'])
    except Exception as e:
        logging.error(f"Error loading data from the database: {e}")
        return pd.DataFrame()

def calculate_percentages(grouped_data):
    """
    Takes a DataFrame that is the result of a groupby().size().unstack()
    and calculates percentages (row-wise). Returns a DataFrame of percentages.
    """
    try:
        total = grouped_data.sum(axis=1)
        percentages = grouped_data.div(total, axis=0) * 100
        return percentages.round(2)
    except Exception as e:
        logging.error(f"Error in calculate_percentages: {e}")
        return pd.DataFrame()
