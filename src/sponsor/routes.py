from flask import Blueprint, request, jsonify
from .service import send_invitation_email

sponsor_bp = Blueprint('sponsor_bp', __name__)

@sponsor_bp.route('/send', methods=['POST'])
def send_email():
    """
    Envoie un lien de parrainage par email
    ---
    tags:
      - sponsor
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
              example: "user@example.com"
    responses:
      200:
        description: Email envoyé avec succès
      500:
        description: Erreur lors de l'envoi de l'email
    """
    data = request.json
    email_address = data.get('email')

    # Vérifier si l'adresse email est fournie
    if email_address:
        # Appeler la fonction d'envoi d'email
        send_invitation_email(email_address, "http://peer.cesi/account")
        # Répondre que l'invitation a été envoyée
        return jsonify({'message': 'Invitation envoyée avec succès à ' + email_address}), 200
    else:
        # Répondre en cas d'erreur
        return jsonify({'error': 'Adresse email manquante'}), 400
