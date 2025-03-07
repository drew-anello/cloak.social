from authlib.integrations.flask_client import OAuth
from flask import current_app, jsonify, session
from config.settings import settings
from functools import wraps

# Initialize OAuth client with the current Flask app context
oauth = OAuth(current_app)

# Register Auth0 client with OAuth
auth0 = oauth.register(
    'auth0',
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    api_base_url=f"https://{settings.AUTH0_DOMAIN}",
    access_token_url=f"https://{settings.AUTH0_DOMAIN}/oauth/token",
    authorize_url=f"https://{settings.AUTH0_DOMAIN}/authorize",
    client_kwargs={
        'audience': settings.AUTH0_AUDIENCE,
        'scope': 'openid profile email read:current_user update:current_user delete:current_user'
    }
)

# Define a decorator to require authentication
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated
        