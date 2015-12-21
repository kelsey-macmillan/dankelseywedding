import os
import psycopg2
from flask import Flask, request

app = Flask(__name__, static_folder='static')

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/rsvp-get/<name>')
def rsvp_get(name):
    conn = psycopg2.connect("dbname=Kelsey user=Kelsey")
    cur = conn.cursor()
    cur.execute('SELECT * FROM guest;')
    data=cur.fetchone()
    cur.close()
    conn.close()
    return str(data)

if __name__ == "__main__":
    app.debug = True
    app.run()
