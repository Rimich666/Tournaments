from flask import (
    render_template,
    redirect,
    url_for
)
from web_app.models import Place
from ..globals import db
from flask_login import current_user
from web_app.tournaments import places_app


@places_app.route()
def places():
    res = db.session.execute(db.select(Place)).scalars()
