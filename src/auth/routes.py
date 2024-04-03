from flask import Blueprint, request
from .service import register_user, login_user, authenticate_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    return register_user(request)

@auth_bp.route('/login', methods=['POST'])
def login():
    return login_user(request)

@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    return authenticate_user(request)