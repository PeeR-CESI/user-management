from flask import current_app, Flask
from flask_mail import Mail, Message

def send_invitation_email(email_address, invite_link):
    app = Flask(__name__)
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='peer.cesi@gmail.com',
        MAIL_PASSWORD='m r p d b t k z c b p v n au j'
    )

    with app.app_context():
        mail = Mail(app)
        msg = Message("Invitation à rejoindre notre plateforme",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email_address])
        msg.body = f"Bonjour, \n\nVous êtes invité à rejoindre notre plateforme. Veuillez utiliser ce lien pour vous inscrire: {'http://peer.cesi/register'}"

        mail.send(msg)
