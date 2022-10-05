from flask import Blueprint

admin_app = Blueprint("admin_app", __name__, url_prefix="/admin", template_folder='templates')

from . import admin
