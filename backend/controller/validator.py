import json
from urllib.request import urlopen
from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from database import SessionLocal
from Models import User
from datetime import datetime
import os

# custom validator for Auth0 JWT tokens
class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):   
    def __init__(self, domain, audience):
        issuer = f"https://{domain}/"
        jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(json.load(jsonurl))
        super(Auth0JWTBearerTokenValidator, self).__init__(public_key)

        self.claims_options = {            
            "exp": {"essential": True},            
            "aud": {"essential": True, "value": audience},            
            "iss": {"essential": True, "value": audience},
        }

    def create_or_update_auth0_user(self, auth0_user):
        """Create or update user from Auth0 data"""
        db = SessionLocal()
        try:
            # Try to find existing user
            user = db.query(User).filter(User.email == auth0_user['email']).first()
            
            if not user:
                user = User(
                    username=auth0_user.get('nickname', auth0_user['email']),
                    email=auth0_user['email'],
                    password='auth0_user',  # placeholder since Auth0 handles auth
                    dob=datetime.now(),
                    account_type='standard',
                    is_active=True,
                    is_admin=False,
                    admin_level=0,
                    auth_token=auth0_user.get('sub')  # Store Auth0 user ID
                )
                db.add(user)
            else:
                user.last_login = datetime.now()
                user.auth_token = auth0_user.get('sub')
            
            db.commit()
            db.refresh(user)
            return user, None
            
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()

