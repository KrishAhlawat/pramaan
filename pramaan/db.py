import psycopg
from pgvector.psycopg import register_vector

from .config import DATABASE_URL


def connect() -> psycopg.Connection:
    conn = psycopg.connect(DATABASE_URL, autocommit=False)
    register_vector(conn)
    return conn
