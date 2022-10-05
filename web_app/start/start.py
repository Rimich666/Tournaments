from flask import render_template
from flask_login import current_user

from web_app.start import start_app


@start_app.route('/', endpoint='start')
def start_app():
    return render_template('start/start.html', user="Нет юзера")
