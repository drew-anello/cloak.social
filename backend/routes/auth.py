from flask import Blueprint, request, jsonify, session, redirect, url_for, current_app
from services.auth0 import Auth0Service
from services.user import UserService
from config.settings import settings
from urllib.parse import urlencode
from datetime import datetime

auth_bp = Blueprint('auth', __name__)
auth0_service = Auth0Service()
user_service = UserService()
auth0 = auth0_service.get_auth0()

@auth_bp.route('/login')
def login():
    try:
        redirect_uri = url_for('auth.callback', _external=True, _scheme='https')
        print(f"Login attempt with client_id: {settings.AUTH0_CLIENT_ID}")
        print(f"Redirect URI: {redirect_uri}")
        return auth0.authorize_redirect(
            redirect_uri=redirect_uri,
            audience=settings.AUTH0_AUDIENCE
        )
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/callback')
def callback():
    try:
        print("Callback route hit")
        print(f"Request args: {request.args}")
        print(f"Request headers: {dict(request.headers)}")  # Add headers logging
        
        try:
            print("Attempting to get access token...")
            # Add more parameters to the token exchange
            token = auth0.authorize_access_token(
                redirect_uri=url_for('auth.callback', _external=True, _scheme='https')
            )
            print(f"Access token obtained: {token}")
        except Exception as token_error:
            print(f"Error getting access token: {str(token_error)}")
            print(f"Token error details: {repr(token_error)}")
            return jsonify({"error": f"Token error: {str(token_error)}"}), 400
        
        try:
            print("Attempting to get user info...")
            resp = auth0.get('userinfo')
            userinfo = resp.json()
            print(f"User info obtained: {userinfo}")

            # Handle different social login providers
            email = userinfo.get('email')
            if not email and 'sub' in userinfo:
                # For social logins that might not provide email immediately
                provider_id = userinfo['sub']
                email = f"{provider_id}@{provider_id.split('|')[0]}.user"
                print(f"Generated email for social login: {email}")

            username = email.split('@')[0] if email else userinfo.get('nickname', 'user')

            # Create or update user in database
            user_data = {
                'username': username,
                'email': email,
                'password': 'auth0_user',  # placeholder since Auth0 handles auth
                'is_active': True,
                'is_admin': False,
                'admin_level': 0,
                'dob': datetime.now(),  # You might want to collect this separately
                'account_type': 'standard',
                'auth_token': userinfo['sub']  # Store Auth0 user ID
            }
            
            print(f"Attempting to create/update user with data: {user_data}")
            user, error = user_service.create_or_update_auth0_user(user_data)
            if error:
                print(f"Error saving user to database: {error}")
                return jsonify({"error": f"Database error: {error}"}), 500

            print(f"User successfully saved: {user}")
            session['jwt_payload'] = userinfo
            session['profile'] = {
                'user_id': userinfo['sub'],
                'name': userinfo.get('name', username),
                'email': email,
                'db_id': user.id if user else None,
                'provider': userinfo['sub'].split('|')[0]  # Add provider information
            }
            print(f"Session data set: {session['profile']}")
            return redirect('/dashboard')
        except Exception as userinfo_error:
            print(f"Error getting user info: {str(userinfo_error)}")
            print(f"User info error details: {repr(userinfo_error)}")
            return jsonify({"error": f"User info error: {str(userinfo_error)}"}), 400

    except Exception as e:
        print(f"Callback error: {str(e)}")
        print(f"Full error details: {repr(e)}")
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/dashboard')
@auth0_service.requires_auth
def dashboard():
    profile = session.get('profile', {})
    if profile.get('db_id'):
        user = user_service.get_user_by_auth_token(profile['user_id'])
        if user:
            return jsonify({
                **profile,
                'account_type': user.account_type,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            })
    return jsonify(profile)