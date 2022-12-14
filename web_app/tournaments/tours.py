from flask import (
    render_template,
    redirect,
    url_for
)
from web_app.models import Tournament, Place
from ..globals import db
from flask_login import current_user
from web_app.tournaments import tours_app


@tours_app.route('/main', endpoint='main')
def main_page():
    if current_user.is_authenticated:
        return redirect(url_for('tours_app.tours'))
    else:
        return redirect(url_for('start_app.start'))


@tours_app.route('/', endpoint='tours')
def tours():
    res = db.session.execute(db.select(Tournament)).scalars()
    rows = []
    count = 1
    for row in res:
        rows.append({
            'id': row.id,
            'tournament': row.tournament.strip(),
            'start': row.start.strftime("%d.%m.%Y"),
            'finish': row.finish.strftime("%d.%m.%Y"),
            'place': row.place.place.strip(),
            'state': row.state
        })
        count += count
        print(row.place.place.strip())
    return render_template('tournaments.html', user=current_user, auth=current_user.is_authenticated,
                           rows=rows, count=count)


@tours_app.route('/add', endpoint="add")
def add_tour():
    return render_template('tours_add.html')


@tours_app.route('/get_places', endpoint="get_places")
def places():
    res = db.session.execute(db.select(Place)).scalars()
    rows = []
    for row in res:
        rows.append({
            'id': row.id,
            'place': row.place
        })
    return rows
