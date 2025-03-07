from flask import Blueprint, request, jsonify
from services.user import UserService

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_service = UserService()
    user, error = user_service.create_or_update_auth0_user(data)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(user.to_dict()), 201
