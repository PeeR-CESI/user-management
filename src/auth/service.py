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

    # Vérification que les deux champs sont fournis
    if not username or not password:
        return jsonify({'message': 'Le nom d’utilisateur et le mot de passe sont requis.'}), 400

    # Recherche de l'utilisateur par nom d'utilisateur
    user = find_user_by_username(username)
    if user:
        # Vérification du mot de passe en comparant les hachages
        hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input_password == user['password']:
            # Si les mots de passe correspondent, générer un token JWT
            token = jwt.encode({
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")
            return jsonify({'message': 'Connexion réussie', 'token': token}), 200
        else:
            return jsonify({'message': 'Mot de passe incorrect.'}), 401
    else:
        return jsonify({'message': 'Nom d’utilisateur incorrect ou utilisateur non trouvé.'}), 404

def authenticate_user(request):
    token = request.json['token']
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({'message' : 'Token is valid', 'data': data})
    except:
        return jsonify({'message' : 'Token is invalid'})
