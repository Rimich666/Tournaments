from flask import Blueprint

login_app = Blueprint("login_app", __name__, url_prefix="/login", template_folder='templates')

from .login import login
