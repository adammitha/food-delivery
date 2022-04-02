from distutils.log import debug
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
    return out

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
    return out

def update_table(table: str, condition_map: Dict[str, Union[str, int]], value_map: Dict[str, Union[str, int]]):
    """
    Updates rows matching condition_map with new values in value_map
    """
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    values_bind_string = ", ".join([f"{key}=?" for key in value_map.keys()])
    conditions = " AND ".join([f"{key}=?" for key in condition_map.keys()])
    query = f"UPDATE {table} SET {values_bind_string} WHERE {conditions}"
    print(query)
    bind_tuple = tuple(value_map.values()) + tuple(condition_map.values())
    cur.execute(query, bind_tuple)
    db_conn.commit()
    return

def average_order_total() -> Dict[int, float]:
    averageOrderTotalQuery = "SELECT O.customer_id, AVG(O.total) FROM OrderTakesHas O WHERE O.customer_id IN (SELECT customer_id FROM Customer) GROUP BY O.customer_id"
    avgOrderTotal = {id: avg for (id, avg) in raw_select_query(averageOrderTotalQuery)}
    return avgOrderTotal


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/customers')
def customer():
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    tableData =  table("Customer")
    db_conn.close()  
    print(tableData)
    return render_template('customer.html', tableData = tableData, avgOrderTotal = average_order_total())

@app.route('/address')
def address():
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    tableData =  table("Address")
    db_conn.close() 
    return render_template('address.html', tableData = tableData)

@app.route('/drivers')
def drivers():
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    tableData =  table("Driver")
    db_conn.close() 
    return render_template('drivers.html', tableData = tableData)

@app.route('/restaurants')
def restaurants():
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    tableData =  table("Restaurant")
    db_conn.close() 
    return render_template('restaurants.html', tableData = tableData)

@app.route('/vehicles', methods=["GET", "POST"])
def vehicles():
    tableData =  table("VehicleDrives")
    totalDistanceDriven = None
    if request.method == "POST":
        totalDistanceDriven = raw_select_query("SELECT SUM(Distance) FROM VehicleDrives")[0][0]
    return render_template('vehicles.html', tableData = tableData, totalDistanceDriven = totalDistanceDriven)

@app.route('/addcustomer')
def customeradd():
    return render_template('addcustomer.html')

@app.route('/addrestaurant')
def restaurantadd():
    return render_template('addrestaurant.html')



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
@app.route("/addcustomer", methods=['PUT'])
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


#app.py
@app.route('/tables/customer', methods=['POST'])
def delete_customer():
    db_conn = sqlite3.connect("food_delivery.db")
    cur = db_conn.cursor()
    cur.execute('DELETE FROM customer WHERE last_name = ?', [request.form['last__name_to_delete']])
    db_conn.commit()
    tableData =  table("Customer")
    return render_template('customer.html', tableData = tableData, avgOrderTotal = average_order_total())

@app.route('/addcustomer', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        customer_address = request.form['customer_address']
        db_conn = sqlite3.connect("food_delivery.db")
        db_conn.execute('INSERT INTO customer (customer_id, customer_address, first_name, last_name) VALUES (?, ?, ?, ?)',
                        (customer_id, customer_address, first_name, last_name))
        db_conn.commit()
        tableData =  table("Customer")
        return render_template('customer.html', tableData= tableData, avgOrderTotal = average_order_total())
    else:
        return render_template('customer.html', tableData= tableData, avgOrderTotal = average_order_total())


def get_customer(customer_id):
    conn = sqlite3.connect('food_delivery.db')
    cust = conn.execute('SELECT * FROM customer WHERE customer_id = ?',
                        (customer_id,)).fetchone()
    print(cust)
    conn.close()
    if cust is None:
        abort(404)
    return cust


@app.route('/<int:customer_id>')
def customer_helper(customer_id):
    customer = get_customer(customer_id)
    return render_template('customerProfile.html', customer=customer)

@app.route('/join')
def customer_restaurants():
    tableData = raw_select_query("SELECT * FROM Customer C, OrderTakesHas O WHERE O.customer_id = C.customer_id")
    return render_template('customerOrder.html', tableData = tableData)


@app.route('/division')
def customer_restaurants_orders():
    tableData = raw_select_query("SELECT * FROM Customer c WHERE NOT EXISTS (SELECT r.restaurant_id FROM  Restaurant r EXCEPT SELECT DISTINCT o.restaurant_id FROM OrderTakesHas o WHERE o.customer_id = c.customer_id)")
    return render_template('customerRestaurant.html', tableData = tableData)

@app.route('/<int:customer_id>/edit', methods=('GET', 'POST'))
def edit(customer_id):
    customer = get_customer(customer_id)
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        addressID = request.form['addressID']
        db_conn = sqlite3.connect("food_delivery.db")
        db_conn.execute('UPDATE customer SET first_name = ?, last_name = ?, addressID = ?'
                         ' WHERE customer_id = ?',
                         (first_name, last_name, addressID, customer_id))
        db_conn.commit()
        db_conn.close()
        tableData =  table("Customer");
        return render_template('customer.html', tableData= tableData, customer = customer, avgOrderTota = average_order_total())
    else:
        return render_template('editcustomer.html', customer = customer)




@app.route('/selection')
def restaurants_orders_select():
    tableData = raw_select_query("SELECT * FROM Restaurant R WHERE R.cuisine = 'French'")
    return render_template('customerSelect.html', tableData = tableData)

@app.route('/projection')
def customer_names():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        customer_address = request.form.get("customer_address")
        tableData = raw_select_query("SELECT ")

    tableData = raw_select_query("SELECT c.first_name, c.last_name FROM Customer c")
    return render_template('customerNames.html', tableData = tableData)
