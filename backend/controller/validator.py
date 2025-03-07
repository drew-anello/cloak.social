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

