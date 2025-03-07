import os
from flask import Flask, jsonify
from Models.user import User
from database.database import Base, engine, SessionLocal
from config.settings import settings
from services.auth0 import Auth0Service
from routes.auth import auth_bp
from routes.register import register_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Configure session
app.config.update(
    SESSION_COOKIE_SECURE=True,  # For HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# Initialize Auth0 service
auth0_service = Auth0Service(app)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(register_bp)

@app.route('/')
def hello():
    return jsonify({"message": "Hello, World!"})    

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        port=3002, 
        debug=True,
        ssl_context=('cert.pem', 'key.pem')
    )