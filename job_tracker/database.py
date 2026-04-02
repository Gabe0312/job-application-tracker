import os

import mysql.connector

try:
    from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
except ImportError:
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'job_tracker'
    DB_PORT = 3306


def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', DB_HOST),
        user=os.getenv('DB_USER', DB_USER),
        password=os.getenv('DB_PASSWORD', DB_PASSWORD),
        database=os.getenv('DB_NAME', DB_NAME),
        port=int(os.getenv('DB_PORT', str(DB_PORT))),
    )
