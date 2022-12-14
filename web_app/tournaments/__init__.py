from flask import Blueprint

tours_app = Blueprint("tours_app", __name__, url_prefix="/tours", template_folder='templates')
places_app = Blueprint("places_app", __name__, url_prefix="/places", template_folder='templates')
references_app = Blueprint("references_app", __name__, url_prefix="/references", template_folder='templates')

from . import tours
from . import places
from . import references

# list_reference = [
#     'teams',
#     'persons',
#     'referees',
#     'sport_types',
#     'speciality',
#     'category',
#     'cards',
# ]
