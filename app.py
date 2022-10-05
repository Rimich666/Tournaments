from flask import (
    redirect,
    url_for)
from flask_login import current_user
from flask_principal import (
    UserNeed,
    RoleNeed,
    identity_loaded
)

from web_app import create_app

app = create_app()


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role.role))


@app.route('/')
def index():
    return redirect(url_for('start_app.start'))
    #return redirect(url_for('login_app.login'))


if __name__ == '__main__':
    app.run(debug=True)
