from flask import Flask, render_template, request
import os
import sqlite3

app = Flask(__name__)

@app.route("/")
def show_signup_form():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def execute_query():
    sql = request.form["sql"]
    sql = sql.lower()  # convert to lowercase
    conn = sqlite3.connect(os.path.join(app.static_folder, "sakila.sqlite"))
    conn.create_collation("NOCASE", lambda x, y: x.lower() == y.lower())
    conn.row_factory = sqlite3.Row  # return results as dictionary
    c = conn.cursor()
    c.execute("PRAGMA case_sensitive_like = OFF")  # make LIKE operator case-insensitive
    c.execute(sql)
    result = c.fetchall()
    conn.close()
    return render_template("query_result.html", result=result)

