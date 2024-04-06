from flask import jsonify, Blueprint
from src.user.model import User
import jwt
import datetime
import hashlib

# Configuration de votre Blueprint et SECRET_KEY
auth_bp = Blueprint('auth_bp', __name__)
SECRET_KEY = "your_secret_key"
REFRESH_SECRET_KEY = "your_refresh_secret_key"

def login_user(request):
    auth_data = request.json
    username = auth_data.get('username')
    password = auth_data.get('password')

    if not username or not password:
        return jsonify({'message': 'Le nom d’utilisateur et le mot de passe sont requis.'}), 400

    # Trouver l'utilisateur dans la base de données
    user = User.query.filter_by(username=username).first()

    if user:
        # Vérifier le mot de passe
        hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input_password == user.password:
            access_token = jwt.encode({
                'user_id': user.id,
                'role': user.role,  # Ajoutez le rôle dans le payload du token si nécessaire
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
            }, SECRET_KEY, algorithm="HS256")

            refresh_token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            }, REFRESH_SECRET_KEY, algorithm="HS256")

            return jsonify({
                'message': 'Connexion réussie',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'role': user.role  # Retournez le rôle de l'utilisateur
            }), 200
        else:
            return jsonify({'message': 'Mot de passe incorrect.'}), 401
    else:
        return jsonify({'message': 'Nom d’utilisateur incorrect ou utilisateur non trouvé.'}), 404

def authenticate_user(request):
    data = request.json
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')

    try:
        if access_token:
            access_data = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            return jsonify({'message' : 'Access token is valid', 'data': access_data}), 200

        if refresh_token:
            refresh_data = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
            return jsonify({'message' : 'Refresh token is valid', 'data': refresh_data}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'message' : 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message' : 'Token is invalid'}), 401
