import json
from flask import Flask
from typing import *
import sqlite3

app = Flask(__name__)

def insert(table: str, values: Dict[str, Union[str, int]]):
    """
    Insert tuple into database table
    """
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    cur.execute("""INSERT INTO ? VALUES ?""", table, values)
    return

def select_table(table: str) -> str:
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    out = []
    for row in cur.execute(f"SELECT * FROM {table}"):
        out.append(row)
    return json.dumps(out)


@app.route("/")
def hello_world():
    return "</p>UBER EATS</p>"

@app.route("/tables/<tablename>")
def table(tablename: str):
    return select_table(tablename)