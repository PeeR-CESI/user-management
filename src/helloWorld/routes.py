from flask import Blueprint, jsonify

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/')
def hello_world():
    return jsonify({"message": "Hello World"})