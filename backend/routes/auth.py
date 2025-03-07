from flask import Blueprint, request, jsonify, session, redirect, url_for
from services.auth0 import Auth0Service
from config.settings import settings
from urllib.parse import urlencode

auth_bp = Blueprint('auth', __name__)
auth0_service = Auth0Service()
auth0 = auth0_service.get_auth0()

@auth_bp.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('auth.callback', _external=True))

@auth_bp.route('/callback')
def callback():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'email': userinfo['email']
    }
    return redirect('/dashboard')

@auth_bp.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('home', _external=True), 'client_id': settings.AUTH0_CLIENT_ID
    }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@auth_bp.route('/dashboard')
@auth0_service.requires_auth
def dashboard():
    return jsonify(session['profile'])