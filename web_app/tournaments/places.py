from flask import (
    render_template,
    redirect,
    url_for,
    request
)
from web_app.models import Place
from ..globals import db
from flask_login import current_user
from web_app.tournaments import places_app


@places_app.route('/', endpoint='places')
def places():
    res = db.session.execute(db.select(Place)).scalars()
    rows = []
    count = 1
    for row in res:
        rows.append({
            'id': row.id,
            'place': row.place,
            'location': {
                'lat': row.lat,
                'lng': row.lng,
            },
            'address': row.address
         })
        for photo in row.photos:
            print(photo)
        count += count
        print(row.place)
    return render_template('places.html', user=current_user, auth=current_user.is_authenticated,
                           rows=rows, count=count)


@places_app.route('/new', endpoint='new')
def place():
    return render_template('place.html', new=True)


@places_app.route('/add', endpoint='add', methods=['POST'])
def add_place():
    if request.method == 'POST':
        print('add place post')
    return 'add place'
