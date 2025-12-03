import sqlite3
from contextlib import closing
import os

DB_PATH = "grocery.db"

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cur = conn.cursor()

        with open("grocery_schema.sql", "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cur.executescript(schema_sql)

        with open("sample_data.sql", "r", encoding="utf-8") as f:
            data_sql = f.read()
        cur.executescript(data_sql)

        conn.commit()

if __name__ == "__main__":
    init_db()
