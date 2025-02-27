import os
from flask import Flask, jsonify
from database import SessionLocal
from Models import User

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/test-db')
def test_db():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return jsonify([user.to_dict() for user in users])
    finally:
        db.close()

# Public routes
@app.route('/public')
def public_route():
    return jsonify({"message": "This is public"})

# Protected routes
@app.route('/protected')
@verify_token
def protected_route():
    return jsonify({"message": "This is protected"})