import os
from flask import Flask, jsonify
from Models.user import User
from database.database import Base, engine, SessionLocal
from config.settings import settings
from services.auth0 import Auth0Service
from routes.auth import auth_bp
app = Flask(__name__)
# Initialize OAuth from Auth0Service
auth0 = Auth0Service()

# Create database tables
Base.metadata.create_all(bind=engine)

app.register_blueprint(auth_bp)
@app.route('/')
def hello():
    return jsonify({"message": "Hello, World!"})    

if __name__ == '__main__':
    app.run(debug=True)