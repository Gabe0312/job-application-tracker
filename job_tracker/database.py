import mysql.connector

def get_db():
    return mysql.connector.connect(
        host='localhost', user='root',
        password='Chewie@1977', database='job_tracker'
    )