from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret (detected by Gitleaks)
DB_PASSWORD = "supersecret123"

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
    # VULNERABILITY 2: SQL Injection (detected by Bandit)
    result = conn.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchall()
    return jsonify(result)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
