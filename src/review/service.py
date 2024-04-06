from .model import Review
from src.user.model import User, db
from flask import jsonify

def add_review(presta_id, data):
    presta = User.query.get(presta_id)
    if presta is None or presta.role != 'presta':
        return jsonify({"error": "Utilisateur non trouvé ou n'est pas un prestataire."}), 404

    review = Review(comment=data['comment'], rating=data['rating'], presta_id=presta_id)
    review.save_to_db()
    return jsonify({"message": "Avis ajouté avec succès.", "review_id": review.id}), 201

def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Avis supprimé avec succès."}), 200
    return jsonify({"error": "Avis non trouvé."}), 404

def get_reviews_by_presta(presta_id):
    presta = User.query.get(presta_id)
    if presta:
        reviews = presta.reviews
        avg_rating = sum([review.rating for review in reviews])/len(reviews) if reviews else 0
        return jsonify({
            "presta": presta.username,
            "average_rating": avg_rating,
            "reviews": [{"comment": review.comment, "rating": review.rating} for review in reviews]
        }), 200
    return jsonify({"error": "Prestataire non trouvé."}), 404
