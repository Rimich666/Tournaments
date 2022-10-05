from flask import Blueprint

start_app = Blueprint("start_app", __name__, url_prefix="/start", template_folder='templates')

from . import start
