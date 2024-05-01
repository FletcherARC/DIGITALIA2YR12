import sqlite3

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except:
        print("No")
    finally:
        if conn:
            conn.close()

create_connection("Games_Table.db")