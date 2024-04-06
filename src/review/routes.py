from flask import Blueprint, request, jsonify
from .service import add_review, delete_review, get_reviews_by_presta

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/add', methods=['POST'])
def add():
    """
    Ajoute une review pour un prestataire
    ---
    tags:
      - review
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: Données de la review et l'ID du prestataire
        required: true
        schema:
          type: object
          required:
            - presta_id
            - comment
            - rating
          properties:
            presta_id:
              type: integer
              description: L'ID du prestataire ciblé
            comment:
              type: string
              description: Le commentaire sur le service du prestataire
            rating:
              type: integer
              description: La note attribuée (de 1 à 5)
              minimum: 1
              maximum: 5
    responses:
      201:
        description: Review ajoutée avec succès
      400:
        description: Données invalides fournies
      404:
        description: Prestataire non trouvé
    """
    data = request.json
    return add_review(data['presta_id'], data)

@review_bp.route('/delete/<int:review_id>', methods=['DELETE'])
def delete(review_id):
    """
    Supprime une review existante
    ---
    tags:
      - review
    parameters:
      - name: review_id
        in: path
        required: true
        type: integer
        description: L'ID de la review à supprimer
    responses:
      204:
        description: Review supprimée avec succès
      404:
        description: Review non trouvée
    """
    return delete_review(review_id)

@review_bp.route('/<int:presta_id>', methods=['GET'])
def get_reviews(presta_id):
    """
    Récupère les reviews et la note moyenne pour un prestataire
    ---
    tags:
      - review
    parameters:
      - name: presta_id
        in: path
        required: true
        type: integer
        description: L'ID du prestataire
    responses:
      200:
        description: Reviews et note moyenne récupérées avec succès
      404:
        description: Prestataire non trouvé
    """
    return get_reviews_by_presta(presta_id)
