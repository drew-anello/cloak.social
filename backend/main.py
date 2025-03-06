import os
from flask import Flask, jsonify
from Models import User
from database.database import Base, engine, SessionLocal

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello, World!"})    



if __name__ == '__main__':
    app.run(debug=True)