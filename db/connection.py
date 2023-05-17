import os
import sqlite3
from sqlite3 import Error


def create_connection():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    conn = None
    try:
        conn = sqlite3.connect(f"{ROOT_DIR}/test_db.db")
        return conn
    except Error as e:
        print(e)

    return conn
