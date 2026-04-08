from flask import Flask, jsonify, request
from flask_cors import CORS
import oracledb

app = Flask(__name__)
CORS(app)

connection = oracledb.connect(
    user="system",
    password="Yugin@1263",
    dsn="localhost/XEPDB1"
)
cursor = connection.cursor()

@app.route('/products', methods=['GET'])
def get_products():
    cursor.execute("SELECT * FROM system.product")
    rows = cursor.fetchall()
    return jsonify([{"id":r[0],"name":r[1],"category":r[2],"price":r[3],"quantity":r[4],"supplier":r[5]} for r in rows])

@app.route('/products', methods=['POST'])
def add_product():
    d = request.json
    cursor.execute("INSERT INTO system.product VALUES(:1,:2,:3,:4,:5,:6)",
        (d['id'],d['name'],d['category'],d['price'],d['quantity'],d['supplier']))
    connection.commit()
    return jsonify({"status": "ok"})

@app.route('/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    cursor.execute("DELETE FROM system.product WHERE product_id=:1", (pid,))
    connection.commit()
    return jsonify({"status": "ok"})

@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    cursor.execute("SELECT * FROM supplier")
    rows = cursor.fetchall()
    return jsonify([{"id":r[0],"name":r[1],"phone":r[2],"address":r[3]} for r in rows])

@app.route('/orders', methods=['GET'])
def get_orders():
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    return jsonify([{"id":r[0],"customer_id":r[1],"date":str(r[2]),"total":r[3]} for r in rows])

@app.route('/products/<int:pid>/quantity', methods=['PUT'])
def update_quantity(pid):
    d = request.json
    cursor.execute("UPDATE system.product SET quantity=:1 WHERE product_id=:2",
        (d['quantity'], pid))
    connection.commit()
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)