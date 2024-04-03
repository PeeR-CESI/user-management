from flask import Flask
from auth.routes import auth_bp
from helloWorld.routes import test_bp
from user.routes import user_bp

app = Flask(__name__)

app.register_blueprint(test_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == "__main__":
    app.run(port=3000)