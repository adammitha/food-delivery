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
    return out;

def delete_table_row(table: str, condition_map: Dict[str, Union[str, int]]):
    """
    Deletes row(s) from table that matches the condition_map
    """
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    conditions = " AND ".join([f"{key}=?" for key in condition_map.keys()])
    query = f"DELETE FROM {table} WHERE {conditions}"
    cur.execute(query, tuple(condition_map.values()))
    db_conn.commit()
    return 

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
    db_conn = sqlite3.connect("food_delivery.db");
    cur = db_conn.cursor();
    tableData =  table("Customer");
    db_conn.close()  
    print(tableData)
    return render_template('customer.html', tableData = tableData);

@app.route('/address')
def address():
    db_conn = sqlite3.connect("food_delivery.db");
    cur = db_conn.cursor();
    tableData =  table("Address");
    db_conn.close() 
    return render_template('address.html', tableData = tableData)

@app.route('/drivers')
def drivers():
    db_conn = sqlite3.connect("food_delivery.db");
    cur = db_conn.cursor();
    tableData =  table("Driver");
    db_conn.close() 
    return render_template('drivers.html', tableData = tableData)

@app.route('/restaurants')
def restaurants():
    db_conn = sqlite3.connect("food_delivery.db");
    cur = db_conn.cursor();
    tableData =  table("Restaurant");
    db_conn.close() 
    return render_template('restaurants.html', tableData = tableData)

@app.route('/vehicles')
def vehicles():
    db_conn = sqlite3.connect("food_delivery.db");
    cur = db_conn.cursor();
    tableData =  table("VehicleDrives");
    db_conn.close() 
    return render_template('vehicles.html', tableData = tableData);

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

# Example URL: http://127.0.0.1:5000/tables/Driver
# Must use DELETE method
# Content-type header must be application/json
# Conditions for row(s) to delete must be passed in request body as json object {attribute: value}
# E.g. '{"first_name": "Ben", "last_name": "Kenobi"}'
@app.route("/tables/<tablename>", methods=['DELETE'])
def delete(tablename: str):
    delete_table_row(tablename, request.json)
    return json.dumps({"result": "Success"})

if __name__ == '__name__':
    app.run(port=5000,debug=True)
