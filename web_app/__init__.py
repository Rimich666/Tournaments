from flask import (
    Flask)
from config import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    register_blueprints(app)
    init_extensions(app)
    bind_model(app.name)
    return app


def bind_model(app_name):
    from web_app.globals import models
    from web_app.functions.bind_models import bind
    bind(app_name)


def init_extensions(app):
    from web_app.functions import TableInform
    from web_app.globals import (
        login,
        db,
        principals,
        socketio,
        migrate,
    )
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    principals.init_app(app)
    socketio.init_app(app)


def register_blueprints(app):
    from web_app.admin import admin_app
    from web_app.login import login_app
    from web_app.start import start_app
    from web_app.tournaments import tours_app
    from web_app.tournaments import places_app

    app.register_blueprint(admin_app)
    app.register_blueprint(login_app)
    app.register_blueprint(start_app)
    app.register_blueprint(tours_app)
