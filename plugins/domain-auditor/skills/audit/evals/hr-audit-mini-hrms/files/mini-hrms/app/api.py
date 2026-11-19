import hashlib
import sqlite3

from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = "supersecret123"


def db():
    con = sqlite3.connect("db/hr.sqlite")
    con.row_factory = sqlite3.Row
    return con


@app.post("/login")
def login():
    u = request.json["username"]
    p = hashlib.md5(request.json["password"].encode()).hexdigest()
    row = db().execute(f"SELECT * FROM users WHERE username='{u}' AND password_md5='{p}'").fetchone()
    if row:
        session["user"] = dict(row)
        return jsonify(ok=True)
    return jsonify(ok=False), 401


@app.get("/employees")
def employees():
    rows = db().execute("SELECT * FROM employees").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/employees/<int:emp_id>")
def employee(emp_id):
    if "user" not in session:
        return jsonify(error="login"), 401
    row = db().execute("SELECT * FROM employees WHERE id=?", (emp_id,)).fetchone()
    return jsonify(dict(row))


@app.delete("/orders/<int:order_id>")
def delete_order(order_id):
    con = db()
    con.execute("DELETE FROM orders WHERE id=?", (order_id,))
    con.commit()
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=True)
