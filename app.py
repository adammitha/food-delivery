import json
from flask import Flask, request
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

def select_table(table: str, attributes: str) -> str:
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    out = []
    for row in cur.execute(f"SELECT {attributes} FROM {table}"):
        out.append(row)
    return json.dumps(out)


@app.route("/")
def hello_world():
    return "</p>UBER EATS</p>"

# Example url: http://127.0.0.1:5000/tables/Driver?attributes=first_name,last_name
# If you want all the attributes in a table, don't include the attributes query parameter:
# http://127.0.0.1:5000/tables/Driver
@app.route("/tables/<tablename>", method=['GET'])
def table(tablename: str):
    attributes = request.args.get("attributes")
    if attributes is None:
        attributes = "*"
    return select_table(tablename, attributes)
