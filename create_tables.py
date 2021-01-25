import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    This function deletes existing tables from the database.
    Arguments:
    - cur: cursor to the database
    - conn: connection to the database
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This function creates tables in the database.
    Arguments:
    - cur: cursor to the database
    - conn: connection to the database
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """Core part of our application"""
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # create connection to the database with config settings stored in dwh.cfg
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    # drop tables if they already exist and create new ones
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()