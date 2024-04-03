from flask import Blueprint, request, jsonify
from .service import add_user_service, update_user_service, delete_user_service, find_user_service

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/create', methods=['POST'])
def create_user():
    user_data = request.json
    user_id, message = add_user_service(user_data)
    if user_id:
        return jsonify({"message": message, "user_id": user_id}), 201
    else:
        return jsonify({"error": message}), 400

@user_bp.route('/update/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    message, success = update_user_service(user_id, user_data)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400

@user_bp.route('/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = delete_user_service(user_id)
    return jsonify(result), 204

@user_bp.route('/find/<user_id>', methods=['GET'])
def get_user(user_id):
    result, status = find_user_service(user_id)
    return jsonify(result), status
