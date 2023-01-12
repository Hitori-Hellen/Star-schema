import psycopg2
from Project_Sql_Queries import *

def create_database():
    conn = psycopg2.connect("host=localhost user=postgres password=root port=5432")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    cur.execute("DROP DATABASE IF EXISTS songstarschema")
    cur.execute("CREATE DATABASE songstarschema WITH ENCODING 'utf8' TEMPLATE template0")
    
    cur.close()
    conn.close()

def connect_database():
    conn = psycopg2.connect("host=localhost dbname=songstarschema user=postgres password=root port=5432")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    return cur, conn

def create_table(cur, conn):
    for query in create_table_sql:
        cur.execute(query)
        conn.commit()

def drop_table(cur, conn):
    for query in drop_table_sql:
        cur.execute(query)
        conn.commit()

def main():
    create_database()
    cur, conn = connect_database()
    
    # Delete old table
    drop_table(cur, conn)
    
    # Create new
    create_table(cur, conn)
    
    conn.close()

if __name__ == "__main__":
    main()