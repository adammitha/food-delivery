from flask import Flask
from typing import *
import sqlite3

app = Flask(__name__)
db_conn = sqlite3.connect("food_delivery.db")

def insert(table: str, values: Dict[str, Union[str, int]]):
    """
    Insert tuple into database table
    """
    cur = db_conn.cursor()
    cur.execute("""INSERT INTO ? VALUES ?""", table, values)
    return

@app.route("/")
def hello_world():
    return "</p>UBER EATS</p>"
