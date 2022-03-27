from http.client import HTTPException
import json
from flask import Flask, render_template, request
from typing import *
import sqlite3

app = Flask(__name__)

def insert_table(table: str, value_map: Dict[str, Union[str, int]]) -> int:
    """
    Insert tuple into database table
    """
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    columns = f"({','.join(value_map.keys())})"
    values = tuple(value_map.values())
    values_bind_string = f"({','.join(['?'] * len(value_map))})"
    query = f"INSERT INTO {table}{columns} VALUES {values_bind_string}"
    cur.execute(query, values)
    db_conn.commit()
    return cur.lastrowid

def select_table(table: str, attributes: str) -> str:
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    out = []
    for row in cur.execute(f"SELECT {attributes} FROM {table}"):
        out.append(row)
    return json.dumps(out)

def raw_select_query(query: str):
    """
    Execute raw select sql query against db
    Assumes that query is a select query. Caller must check this invariant
    """
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    out = []
    for row in cur.execute(query):
        out.append(row)
    return json.dumps(out)


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/customers')
def customer():
    return render_template('customer.html')

@app.route('/address')
def address():
    return render_template('address.html')

@app.route('/drivers')
def drivers():
    return render_template('drivers.html')

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html')

# Example url: http://127.0.0.1:5000/tables/Driver?attributes=first_name,last_name
# If you want all the attributes in a table, don't include the attributes query parameter:
# http://127.0.0.1:5000/tables/Driver

@app.route("/tables/<tablename>", methods=['GET'])
def table(tablename: str):
    attributes = request.args.get("attributes")
    if attributes is None:
        attributes = "*"
    return select_table(tablename, attributes)

# Example: http://127.0.0.1:5000/raw-query?query=<SELECT query goes here>
@app.route("/raw-query", methods=['GET'])
def raw_query():
    query = request.args.get("query")
    if query is None or query.find("SELECT") != 0:
        raise HTTPException("Must pass a select query in the `query` param")
    return raw_select_query(query)

# Example URL: http://127.0.0.1:5000/tables/Driver
# Must use PUT method
# Content-type header must be application/json
# Values to insert must be passed in request body as json object
# E.g '{"driver_id": 7, "first_name": "Bob", "last_name": "Builder", "drivers_license_number": 95444792}'
@app.route("/tables/<tablename>", methods=['PUT'])
def insert(tablename: str):
    return json.dumps({"row_id": insert_table(tablename, request.json)})

if __name__ == '__name__':
    app.run(port=5000,debug=True)
