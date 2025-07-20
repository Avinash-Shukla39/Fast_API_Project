import psycopg2
from psycopg2 import pool
from app.config import Config

connection_pool = None

def init_db_pool():
    global connection_pool
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 10, Config.DATABASE_URL
    )

def get_db_connection():
    if connection_pool is None:
        init_db_pool()
    return connection_pool.getconn()

def release_db_connection(connection):
    connection_pool.putconn(connection)