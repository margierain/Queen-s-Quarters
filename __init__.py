from flask.ext.login import LoginManager
from flask import Blueprint
from app import views

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

auth = Blueprint('auth', __name__)