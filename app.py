from flask import Flask, request, jsonify
from db import get_connection, init_db

app = Flask(__name__)

# Inicializar base de datos
init_db()


# ======================
# USERS
# ======================
@app.route("/users", methods=["GET", "POST"])
def users():
    conn = get_connection()
    cursor = conn.cursor()

    # GET: listar usuarios
    if request.method == "GET":
        cursor.execute("SELECT * FROM users")
        users = [
            {"id": r[0], "name": r[1], "email": r[2]}
            for r in cursor.fetchall()
        ]
        conn.close()
        return jsonify(users)

    # POST: crear usuario
    if request.method == "POST":
        data = request.json

        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (data["name"], data["email"])
        )
        conn.commit()

        user_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "User created",
            "id": user_id
        }), 201


# ======================
# PRODUCTS
# ======================
@app.route("/products", methods=["GET", "POST"])
def products():
    conn = get_connection()
    cursor = conn.cursor()

    # GET
    if request.method == "GET":
        cursor.execute("SELECT * FROM products")
        products = [
            {
                "id": r[0],
                "name": r[1],
                "price": r[2],
                "stock": r[3]
            }
            for r in cursor.fetchall()
        ]
        conn.close()
        return jsonify(products)

    # POST
    if request.method == "POST":
        data = request.json

        cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            (data["name"], data["price"], data["stock"])
        )
        conn.commit()

        product_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "Product created",
            "id": product_id
        }), 201


# ======================
# CREATE ORDER
# ======================
@app.route("/orders", methods=["POST"])
def create_order():
    conn = get_connection()
    cursor = conn.cursor()

    data = request.json
    user_id = data["user_id"]
    items = data["items"]

    total = 0

    # calcular total
    for item in items:
        cursor.execute(
            "SELECT price, stock FROM products WHERE id=?",
            (item["product_id"],)
        )
        result = cursor.fetchone()

        if not result:
            conn.close()
            return jsonify({"error": "Product not found"}), 404

        price, stock = result

        if stock < item["quantity"]:
            conn.close()
            return jsonify({"error": "Not enough stock"}), 400

        total += price * item["quantity"]

    # crear orden
    cursor.execute(
        "INSERT INTO orders (user_id, total) VALUES (?, ?)",
        (user_id, total)
    )
    order_id = cursor.lastrowid

    # insertar items + actualizar stock
    for item in items:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_id, item["product_id"], item["quantity"])
        )

        cursor.execute(
            "UPDATE products SET stock = stock - ? WHERE id=?",
            (item["quantity"], item["product_id"])
        )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Order created",
        "order_id": order_id,
        "total": total
    }), 201


# ======================
# GET ORDERS
# ======================
@app.route("/orders", methods=["GET"])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    orders = [
        {"id": r[0], "user_id": r[1], "total": r[2]}
        for r in cursor.fetchall()
    ]

    conn.close()
    return jsonify(orders)


# ======================
# ORDER DETAIL
# ======================
@app.route("/orders/<int:id>", methods=["GET"])
def order_detail(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE id=?", (id,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        return jsonify({"error": "Order not found"}), 404

    cursor.execute("""
        SELECT p.name, oi.quantity, p.price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """, (id,))

    items = [
        {
            "product": r[0],
            "quantity": r[1],
            "price": r[2]
        }
        for r in cursor.fetchall()
    ]

    conn.close()

    return jsonify({
        "id": order[0],
        "user_id": order[1],
        "total": order[2],
        "items": items
    })


# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)