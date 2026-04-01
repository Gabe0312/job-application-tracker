import os

import mysql.connector


def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        # password=os.getenv('DB_PASSWORD', 'TheGabeProg@1203'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'job_tracker'),
        port=int(os.getenv('DB_PORT', '3306')),
    )
