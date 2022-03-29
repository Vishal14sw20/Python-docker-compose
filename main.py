#!/usr/bin/python
import psycopg2
from config import get_connection
from crud import inset_data
from pgtocsv import pg_to_csv
from pathlib import Path
from yaml import safe_load as yload
import time


def main():
    conn = None
    try:
        # get postgres connection
        conn = get_connection()
        # create a cursor
        cur = conn.cursor()
        start_time = time.time()
        find_and_insert_data(cur)
        print("Tables created and Data inserted")

        all_pg_to_csv(conn)
        print("All records fetched and stored")
        print("total time {} seconds".format(time.time() - start_time))

        # close the communication with the PostgreSQL
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# finds all json file in specified folder and then pass all json files to insert data function one by one
def find_and_insert_data(cur):
    directory = "data"
    files = Path(directory).glob('*')
    for file in files:
        # execute a statement
        cur.execute(inset_data(file))


# take all queries from sql.yml and execute them
# after that generate csv files for result set
def all_pg_to_csv(orm_conn):
    query_list = list_select_query()
    for filename, query in query_list.items():
        pg_to_csv(filename, query, orm_conn)


# get all select queries
def list_select_query():
    with open("sql.yml") as fi:
        di = yload(fi)
    return di["sql"]


if __name__ == '__main__':
    main()
