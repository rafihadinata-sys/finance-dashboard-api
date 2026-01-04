from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "database.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            gig TEXT,
            usd REAL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT date, gig, usd FROM transactions")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.json
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO transactions (date, gig, usd) VALUES (?, ?, ?)",
        (data["date"], data["gig"], data["usd"])
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
