from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from flask_login import UserMixin
from sqlalchemy.orm import (relationship)
from ..globals import db, login
from ..forms import (
    Templ,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model, Templ):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(String(10), unique=True, nullable=False)
    users = relationship('User', back_populates='role')

    def __init__(self, id=None, role=''):
        self.id = id
        self.role = role

    pass


class User(db.Model, Templ, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id, ondelete='CASCADE'))
    phone_number = Column(String(12), unique=False)
    password_hash = db.Column(db.String(128))
    role = relationship('Role', back_populates='users')

    add_templ = "register"

    def __init__(self, id=None, username='', role_id=0, phone_number=''):
        self.id = id
        self.username = username
        self.role_id = role_id
        self.phone_number = phone_number

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

    pass

