from flask import Blueprint

tours_app = Blueprint("tours_app", __name__, url_prefix="/tours", template_folder='templates')

from . import tours
