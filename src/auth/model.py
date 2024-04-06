from src.user.model import db

class AuthUser(db.Model):
    __tablename__ = 'auth_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
