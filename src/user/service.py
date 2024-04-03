from .model import User
from bson import ObjectId

required_fields = ["nom", "prenom", "email", "adresse", "role"]
valid_roles = ["demandeur", "presta", "admin"]

def validate_user_data(user_data):
    # Vérifier la présence de tous les champs requis
    if not all(field in user_data for field in required_fields):
        return False, "Tous les champs requis doivent être fournis."

    # Vérifier la validité du rôle
    if user_data["role"] not in valid_roles:
        return False, "Rôle invalide."

    # Ici, ajoutez d'autres validations selon vos besoins (ex : format de l'email)

    return True, "Données valides."

def add_user_service(user_data):
    is_valid, message = validate_user_data(user_data)
    if not is_valid:
        return None, message

    user_id = User.create(user_data)
    return user_id, "Utilisateur créé avec succès."

def update_user_service(user_id, user_data):
    # Validation du format ici
    is_valid, message = validate_user_data(user_data)
    if not is_valid:
        return {"message": message}, 400

    # Opération de mise à jour
    success, message = User.update(user_id, user_data)
    if not success:
        return {"message": message}, 404 if message == "Utilisateur non trouvé." else 400

    return {"message": message}, 200



def delete_user_service(user_id):
    # Logique supplémentaire avant suppression pourrait aller ici
    User.delete(user_id)
    return "Utilisateur supprimé avec succès."

def find_user_service(user_id):
    user = User.find(user_id)
    if user:
        # Assurez-vous de convertir ObjectId en string si nécessaire ici
        user['_id'] = str(user['_id'])
        return user, 200  # Renvoie l'utilisateur et le code de statut HTTP 200
    else:
        return {"message": "Utilisateur non trouvé."}, 404  # Renvoie un message d'erreur et le code de statut HTTP 404

