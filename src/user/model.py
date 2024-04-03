from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client.user_database
users_collection = db.users

class User:
    def __init__(self, nom, prenom, email, adresse, role):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.adresse = adresse
        self.role = role

    @staticmethod
    def create(user_data):
        # Insérer l'utilisateur dans la base de données et retourner l'ID
        inserted_id = users_collection.insert_one(user_data).inserted_id
        return str(inserted_id)

    @staticmethod
    def update(user_id, user_data):
        if not ObjectId.is_valid(user_id):
            return False, "ID utilisateur invalide."
        result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
        if result.matched_count == 0:
            return False, "Utilisateur non trouvé."
        return True, "Utilisateur mis à jour avec succès."

    @staticmethod
    def delete(user_id):
        # Suppression de l'utilisateur
        users_collection.delete_one({"_id": ObjectId(user_id)})

    @staticmethod
    def find(user_id):
        # Recherche d'un utilisateur par son ID
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])  # Convertir ObjectId en String
            return user
        return None
