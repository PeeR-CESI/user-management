from flask import Blueprint, request
from .service import register_user, login_user, authenticate_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Inscription d'un nouvel utilisateur
    ---
    tags:
      - auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: Données de l'utilisateur à inscrire
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Utilisateur enregistré avec succès
      400:
        description: Erreur de validation des données d'entrée
    """
    return register_user(request)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Connexion d'un utilisateur existant
    ---
    tags:
      - auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: Identifiants de l'utilisateur pour la connexion
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Connexion réussie, token JWT fourni
      401:
        description: Mot de passe incorrect
      404:
        description: Nom d'utilisateur non trouvé
    """
    return login_user(request)

@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    """
    Authentification d'un utilisateur via token JWT
    ---
    tags:
      - auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: Token JWT à vérifier
        required: true
        schema:
          type: object
          required:
            - token
          properties:
            token:
              type: string
    responses:
      200:
        description: Token est valide
      401:
        description: Token est invalide ou expiré
    """
    return authenticate_user(request)
