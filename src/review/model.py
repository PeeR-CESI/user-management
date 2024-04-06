from src.user.model import db, User

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    presta_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    presta = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
