import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "ops_cli.db")

con = sqlite3.connect(db_path)
cur = con.cursor()


def query(type):
    sql = f"select * from certi where type = '{type}'"
    return cur.execute(sql)


def fetch_all():
    return cur.execute("select * from certi")