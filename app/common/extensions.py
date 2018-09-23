#encoding: utf-8

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_openid import OpenID
from flask_mail import Mail
from flask_cache import Cache
from flask_restful import Api

bcrypt = Bcrypt()

openid = OpenID()

mail = Mail()

cache = Cache()

restful_api = Api()

# Create the Flask-Login's instance
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Load the user's info."""

    from app.models import User
    return User.query.filter_by(id=user_id).first()