import os
from flask import Flask, request

app = Flask(__name__, static_folder='static')

@app.route('/')
def main():
    return app.send_static_file('index.html')