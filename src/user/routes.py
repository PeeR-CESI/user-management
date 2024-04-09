from flask import Blueprint, request, jsonify
from .service import add_user_service, update_user_service, delete_user_service, get_user_service, get_all_users_service

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/create', methods=['POST'])
def create_user():
    """
    Création d'un nouvel utilisateur
    ---
    tags:
      - user
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: Données de l'utilisateur à créer
        required: true
        schema:
          type: object
          required:
            - nom
            - prenom
            - email
            - adresse
            - role
            - username
            - password
          properties:
            nom:
              type: string
            prenom:
              type: string
            email:
              type: string
            adresse:
              type: string
            role:
              type: string
              enum: [demandeur, presta, admin]
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Utilisateur créé avec succès
      400:
        description: Erreur de validation des données d'entrée
    """
    user_data = request.json
    result, status = add_user_service(user_data)
    return jsonify(result), status

@user_bp.route('/update/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Mise à jour des informations d'un utilisateur
    ---
    tags:
      - user
    consumes:
      - application/json
    parameters:
      - name: user_id
        in: path
        required: true
        type: string
      - in: body
        name: body
        description: Données de l'utilisateur à mettre à jour
        required: true
        schema:
          type: object
          properties:
            nom:
              type: string
            prenom:
              type: string
            email:
              type: string
            adresse:
              type: string
            role:
              type: string
              enum: [demandeur, presta, admin]
            username:
              type: string
            password:
              type: string
            service_ids:
              type: string
            sold_service_ids:
              type: string
    responses:
      200:
        description: Utilisateur mis à jour avec succès
      400:
        description: ID utilisateur invalide ou erreur de validation des données
    """
    user_data = request.json
    return update_user_service(user_id, user_data)

@user_bp.route('/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Suppression d'un utilisateur
    ---
    tags:
      - user
    parameters:
      - name: user_id
        in: path
        required: true
        type: string
    responses:
      204:
        description: Utilisateur supprimé avec succès
    """
    result, status = delete_user_service(user_id)
    return jsonify(result), status

@user_bp.route('/find/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Recherche d'un utilisateur par son ID
    ---
    tags:
      - user
    parameters:
      - name: user_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Utilisateur trouvé
      404:
        description: Utilisateur non trouvé
    """
    return get_user_service(user_id)

@user_bp.route('/all', methods=['GET'])
def get_all_users():
    """
    Récupération de tous les utilisateurs
    ---
    tags:
      - user
    responses:
      200:
        description: Liste de tous les utilisateurs récupérée avec succès
      500:
        description: Erreur interne du serveur
    """
    users_data, status = get_all_users_service()
    return jsonify(users_data), status