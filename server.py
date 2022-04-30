from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import os
import psycopg2


app = Flask(__name__)

def exec_statement(conn, stmt):
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            row = cur.fetchone()
            conn.commit()
            if row: print(row[0])
    except psycopg2.ProgrammingError:
        return


def exec_statements(statements):
    connection = psycopg2.connect(os.environ['DATABASE_URL'])
    for statement in statements:
        exec_statement(connection, statement)
    connection.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    return render_template("edit.html", id=id)

@app.route('/stream/<id>', methods=['GET'])
def stream(id):
    return render_template("stream.html", id=id)


# API routes




if __name__ == "__main__" :
    app.run(debug = True)

