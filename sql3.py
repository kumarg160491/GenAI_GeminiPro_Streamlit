import sqlite3
import pandas as pd

# Function to create a SQLite database and table
def create_table():
    conn = sqlite3.connect('covid19.db')
    cursor = conn.cursor()

    # Change the table name and column names according to your Excel file
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS covid19 (
            ObservationDate datetime,
            State Varchar(255),
            Region Varchar(255),
            LastUpdate datetime,
            Confirmed int,
            Deaths int,
            Recovered int
            
        );
    '''
    cursor.execute(create_table_query)

    conn.commit()
    conn.close()

# Function to insert data from Excel into SQLite table
def insert_data_from_csv(csv_file):
    conn = sqlite3.connect('covid19.db')
    cursor = conn.cursor()

    # Change the table name and column names according to your Excel file
    df = pd.read_csv(csv_file)
    print(df.head())
    df.to_sql('covid19', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()


# Example usage
create_table()
insert_data_from_csv(r"covid_19_data.csv")