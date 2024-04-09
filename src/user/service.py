from .model import User, db
import hashlib
from flask import jsonify

required_fields = ["nom", "prenom", "email", "adresse", "role", "username", "password"]
valid_roles = ["demandeur", "presta", "admin", "dev"]

def validate_user_data(user_data):
    missing_or_empty_fields = [field for field in required_fields if not user_data.get(field)]
    if missing_or_empty_fields:
        return False, f"Champs manquants ou vides: {', '.join(missing_or_empty_fields)}."

    if user_data["role"] not in valid_roles:
        return False, f"Rôle invalide. Les rôles valides sont: {', '.join(valid_roles)}."

    return True, "Validation réussie."

def add_user_service(user_data):
    # Vérifier si l'email ou le nom d'utilisateur existe déjà
    user_exists = User.query.filter(
        (User.email == user_data['email']) | (User.username == user_data['username'])
    ).first()

    if user_exists:
        return {"error": "L'email ou le nom d'utilisateur existe déjà."}, 400

    try:
        # Hachage du mot de passe
        hashed_password = hashlib.sha256(user_data['password'].encode('utf-8')).hexdigest()

        # Création de l'instance User
        new_user = User(
            nom=user_data['nom'],
            prenom=user_data['prenom'],
            email=user_data['email'],
            adresse=user_data['adresse'],
            role=user_data['role'],
            username=user_data['username'],
            password=hashed_password
        )

        # Ajout à la base de données et commit
        db.session.add(new_user)
        db.session.commit()

        # Retourne un dictionnaire sérialisable en JSON et un code de statut HTTP
        return {"message": "Utilisateur créé avec succès", "user_id": new_user.id}, 201
    except Exception as e:
        # En cas d'erreur, effectuer un rollback et retourner un message d'erreur
        db.session.rollback()
        return {"error": f"Erreur lors de la création de l'utilisateur: {str(e)}"}, 500

def update_user_service(user_id, user_data):
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"message": "ID utilisateur invalide."}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé."}), 404

    # Vérification si le username ou l'email existe déjà pour un autre utilisateur
    if 'username' in user_data:
        existing_user_by_username = User.query.filter(
            User.username == user_data['username'],
            User.id != user_id
        ).first()
        if existing_user_by_username:
            return jsonify({"error": "Le nom d'utilisateur est déjà utilisé par un autre compte."}), 400

    if 'email' in user_data:
        existing_user_by_email = User.query.filter(
            User.email == user_data['email'],
            User.id != user_id
        ).first()
        if existing_user_by_email:
            return jsonify({"error": "L'adresse email est déjà utilisée par un autre compte."}), 400

    # Mise à jour des champs de l'utilisateur
    for key, value in user_data.items():
        if hasattr(user, key)and key not in ['service_ids', 'sold_service_ids']:
            setattr(user, key, value)

    # Gérer la mise à jour des ID de services et services vendus
    if 'service_ids' in user_data:
        user.service_ids = ",".join(map(str, user_data['service_ids']))
    if 'sold_service_ids' in user_data:
        user.sold_service_ids = ",".join(map(str, user_data['sold_service_ids']))

    try:
        db.session.commit()
        return jsonify({"message": "Utilisateur mis à jour avec succès."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erreur lors de la mise à jour de l'utilisateur: " + str(e)}), 500

def delete_user_service(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "Utilisateur non trouvé."}, 404

    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "Utilisateur supprimé avec succès."}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erreur lors de la suppression de l'utilisateur: {str(e)}"}, 500


def get_user_service(user_id):
    # Rechercher l'utilisateur par son ID
    user = User.query.get(user_id)

    if user:
        # Si l'utilisateur existe, retournez ses données
        user_data = {
            "id": user.id,
            "nom": user.nom,
            "prenom": user.prenom,
            "email": user.email,
            "adresse": user.adresse,
            "role": user.role,
            "username": user.username,
            "service_ids": user.service_ids.split(",") if user.service_ids else [],
            "sold_service_ids": user.sold_service_ids.split(",") if user.sold_service_ids else [],
        }
        return jsonify(user_data), 200
    else:
        # Si l'utilisateur n'existe pas, retournez un message d'erreur
        return jsonify({"error": "Utilisateur non trouvé."}), 404

def get_all_users_service():
    try:
        users = User.query.all()
        users_data = [
            {
                "id": user.id,
                "nom": user.nom,
                "prenom": user.prenom,
                "email": user.email,
                "adresse": user.adresse,
                "role": user.role,
                "username": user.username
            }
            for user in users
        ]
        return users_data, 200
    except Exception as e:
        return {"error": str(e)}, 500
