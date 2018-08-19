#encoding: utf-8

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_openid import OpenID
# from flask_principal import Principal, Permission, RoleNeed
# from flask_bootstrap import Bootstrap
from flask_celery import Celery
from flask_mail import Mail
from flask_cache import Cache
# from flask_assets import Environment, Bundle
from flask_restful import Api
# from flask_admin import Admin

# Create the Flask-Bcrypt's instance

bcrypt = Bcrypt()

# Create the Flask-OpenID's instance
openid = OpenID()

# Create the Flask-Login's instance
login_manager = LoginManager()

# Create the Flask-Principal's instance
# principals = Principal()

# Create the Bootstrap's instance
# Bootstrap = Bootstrap()

# Create the Flask-Celery-Helper's instance
# flask_celery = Celery()

# Create the Flask-Mail's instance
mail = Mail()

# Create the Flask-Cache's instance
cache = Cache()

#### Create the Flask-Restful's instance
restful_api = Api()
#### Create the Flask-Admin's instance
# flask_admin = Admin()

# Create the Flask-Assets's instance
# assets_env = Environment()
# Define the set for js and css file.
# main_css = Bundle(
#     'css/bootstrap.css',
#     'css/bootstrap-theme.css',
#     filters='cssmin',
#     output='assets/css/common.css')
#
# main_js = Bundle(
#     'js/bootstrap.js',
#     filters='jsmin',
#     output='assets/js/common.js')

# 这里设定了 3 种权限, 这些权限会被绑定到 Identity 之后才会发挥作用.
# Init the role permission via RoleNeed(Need).
# admin_permission = Permission(RoleNeed('admin'))
# poster_permission = Permission(RoleNeed('poster'))
# default_permission = Permission(RoleNeed('default'))


# Setup the configuration for login manager.
#     1. Set the login page.
#     2. Set the more stronger auth-protection.
#     3. Show the information when you are logging.
#     4. Set the Login Messages type as `information`.
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Load the user's info."""

    from app.models import User
    return User.query.filter_by(id=user_id).first()