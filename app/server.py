"""
Mock Product API — a tiny Flask app that talks to PostgreSQL.
Used to demonstrate multi-container Docker Compose for QE.
"""
from flask import Flask, jsonify, request
import psycopg2
import os
import time

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "testdb"),
    "user": os.environ.get("DB_USER", "testuser"),
    "password": os.environ.get("DB_PASSWORD", "testpass"),
}


def get_db():
    return psycopg2.connect(**DB_CONFIG)


def wait_for_db(retries=10, delay=2):
    """Wait for PostgreSQL to be ready — containers start in parallel."""
    for attempt in range(retries):
        try:
            conn = get_db()
            conn.close()
            print(f"Database ready after {attempt + 1} attempt(s)")
            return
        except psycopg2.OperationalError:
            print(f"DB not ready, retrying in {delay}s... ({attempt + 1}/{retries})")
            time.sleep(delay)
    raise Exception("Database never became ready")


def init_db():
    """Create tables and seed test data."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price NUMERIC(10,2) NOT NULL,
            in_stock BOOLEAN DEFAULT TRUE
        )
    """)
    # Seed data — only if table is empty
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO products (name, price, in_stock) VALUES
            ('Sauce Labs Backpack', 29.99, TRUE),
            ('Sauce Labs Bike Light', 9.99, TRUE),
            ('Sauce Labs Bolt T-Shirt', 15.99, TRUE),
            ('Sauce Labs Fleece Jacket', 49.99, FALSE)
        """)
    conn.commit()
    cur.close()
    conn.close()


# ─── Routes ──────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint — CI and Docker use this to know the app is ready."""
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


@app.route("/api/products", methods=["GET"])
def get_products():
    """GET all products."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, in_stock FROM products ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    products = [
        {"id": r[0], "name": r[1], "price": float(r[2]), "in_stock": r[3]}
        for r in rows
    ]
    return jsonify(products), 200


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """GET a single product by ID."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, in_stock FROM products WHERE id = %s", (product_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"id": row[0], "name": row[1], "price": float(row[2]), "in_stock": row[3]}), 200


@app.route("/api/products", methods=["POST"])
def create_product():
    """POST — create a new product."""
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "name and price are required"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price, in_stock) VALUES (%s, %s, %s) RETURNING id",
        (data["name"], data["price"], data.get("in_stock", True)),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "name": data["name"], "price": data["price"], "in_stock": data.get("in_stock", True)}), 201


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """DELETE a product by ID."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = %s RETURNING id", (product_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": f"Product {product_id} deleted"}), 200


# ─── Startup ─────────────────────────────────────────────

if __name__ == "__main__":
    wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=5000)
