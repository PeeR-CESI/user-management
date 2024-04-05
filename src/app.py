from flask import Flask
from flasgger import Swagger
from auth.routes import auth_bp
from helloWorld.routes import test_bp
from user.routes import user_bp

app = Flask(__name__)

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