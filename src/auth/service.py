from flask import jsonify, make_response, Blueprint
from .model import create_user, find_user_by_username
import jwt
import datetime
import hashlib

# Configuration de votre Blueprint et SECRET_KEY
auth_bp = Blueprint('auth_bp', __name__)
SECRET_KEY = "your_secret_key"

def register_user(request):
    data = request.json
    # Utilisation de hashlib pour le hachage SHA-256
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    create_user({'username': data['username'], 'password': hashed_password})
    return make_response(jsonify({"message": "Registered successfully"}), 201)

def login_user(request):
    auth_data = request.json
    username = auth_data.get('username')
    password = auth_data.get('password')

    # Vérification de la présence de username et password
    if not username or not password:
        return jsonify({'message': 'Login et mot de passe requis'}), 400

    # Trouver l'utilisateur dans la base de données
    user = find_user_by_username(username)

    # Utilisation de hashlib pour vérifier le hachage du mot de passe
    hashed_input_password = hashlib.sha256(password.encode()).hexdigest()

    # Vérifier si l'utilisateur existe et si le mot de passe haché correspond
    if user and hashed_input_password == user['password']:
        # Générer le token JWT
        token = jwt.encode({
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({'message': 'Connexion réussie', 'token': token}), 200
    else:
        # Si l'utilisateur n'existe pas ou si le mot de passe ne correspond pas
        return jsonify({'message': 'Login ou mot de passe incorrect'}), 401

def authenticate_user(request):
    token = request.json['token']
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({'message' : 'Token is valid', 'data': data})
    except:
        return jsonify({'message' : 'Token is invalid'})
