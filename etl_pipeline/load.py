# load.py — Step L in ETL
# Saves clean data to SQLite and provides query helper

import sqlite3
import pandas as pd
from config import DB_PATH

def load_to_db(df):
    # Connect to database
    # If weather.db does not exist yet, SQLite creates it automatically
    conn = sqlite3.connect(DB_PATH)

    # Save DataFrame to a table called "weather_readings"
    # if_exists="append" means: add rows, do not overwrite old data
    # index=False means: do not save the row numbers (0,1,2...) as a column
    df.to_sql(
        name="weather_readings",
        con=conn,
        if_exists="append",
        index=False
    )
    conn.close()
    print(f"Loaded {len(df)} rows into weather.db")

def query_db(sql_query):
    # Helper function to run any SQL query and get a DataFrame back
    # Use this to check what is in your database at any time
    conn   = sqlite3.connect(DB_PATH)
    result = pd.read_sql(sql_query, conn)
    conn.close()
    return result

# Test: check what is in the database
if __name__ == "__main__":

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table';
    """)

    print(cursor.fetchall())

    conn.close()

