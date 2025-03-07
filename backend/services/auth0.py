from authlib.integrations.flask_client import OAuth
from flask import current_app, jsonify, session
from config.settings import settings
from functools import wraps

class Auth0Service:
    def __init__(self, app=None):
        self.oauth = OAuth(app or current_app)
        self.auth0 = self.oauth.register(
            'auth0',
            client_id=settings.AUTH0_CLIENT_ID,
            client_secret=settings.AUTH0_CLIENT_SECRET,
            api_base_url=f"https://{settings.AUTH0_DOMAIN}",
            access_token_url=f"https://{settings.AUTH0_DOMAIN}/oauth/token",
            authorize_url=f"https://{settings.AUTH0_DOMAIN}/authorize",
            server_metadata_url=f'https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid profile email',
                'response_type': 'code',
                'token_endpoint_auth_method': 'client_secret_post'
            }
        )

    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session:
                return jsonify({'message': 'Unauthorized'}), 401
            return f(*args, **kwargs)
        return decorated

    def get_auth0(self):
        return self.auth0
        