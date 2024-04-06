from flask import Flask
from flasgger import Swagger
from src.auth.routes import auth_bp
from src.helloWorld.routes import test_bp
from src.user.routes import user_bp
from src.user.model import db

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'objet SQLAlchemy
db.init_app(app)

# Créez les tables
with app.app_context():
    db.create_all()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # Toutes les règles correspondent
            "model_filter": lambda tag: True,  # Tous les modèles
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

app.register_blueprint(test_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == "__main__":
    app.run(port=5000)