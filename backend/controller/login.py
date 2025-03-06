from flask import Blueprint, request, jsonify
from controller.validator import Auth0JWTBearerTokenValidator, create_or_update_auth0_user