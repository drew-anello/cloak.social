import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE')
    PSQLURI = os.environ.get('PSQLURI')
    PSQLDBNAME = os.environ.get('PSQLDBNAME')
    SQLALCHEMY_DATABASE_URI = f"{PSQLURI}{PSQLDBNAME}"
    MONGOURI = os.getenv('MONGOURI')
    MONGODBNAME = os.getenv('MONGODBNAME')
    JWT_SECRET = os.getenv('JWT_SECRET')
    JWT_EXPIRY = os.getenv('JWT_EXPIRY')
    FLASKAPIURL = os.getenv('FLASKAPIURL')

    def __init__(self):
        print(f"AUTH0_CLIENT_ID: {self.AUTH0_CLIENT_ID}")

settings = Config()