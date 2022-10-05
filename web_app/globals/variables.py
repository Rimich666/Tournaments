from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import (
    Principal,
    Permission,
    RoleNeed
)
from flask_socketio import SocketIO

db = SQLAlchemy()
login = LoginManager()
principals = Principal()
admin = Permission(RoleNeed('admin'))
socketio = SocketIO()
migrate = Migrate()

