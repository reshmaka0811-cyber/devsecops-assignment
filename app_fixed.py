from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# FIX 1: Secret loaded from environment variable (not hardcoded)
DB_PASSWORD = os.environ.get("DB_PASSWORD")

def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    conn.execute("INSERT INTO users VALUES (2, 'Bob')")
    conn.commit()
    return conn

@app.route("/search")
def search():
    name = request.args.get("name", "")
    conn = get_db()
    # FIX 2: Parameterized query — prevents SQL Injection
    result = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
    return jsonify(result)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # FIX 3: debug=False in production
    app.run(debug=False)
