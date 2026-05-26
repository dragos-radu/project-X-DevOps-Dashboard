import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_database_config():
    return {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT")
    }

def get_database_connection():
    config = get_database_config()
    return psycopg2.connect(**config)

def check_database_connection():
    config = get_database_config()
    try:
        conn = psycopg2.connect(**config)
        conn.close()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False