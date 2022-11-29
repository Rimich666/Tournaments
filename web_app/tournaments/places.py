from flask import (
    render_template,
    redirect,
    url_for,
    request,
    make_response
)
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError
from web_app.models import (Place, PlacePhotos)
from ..globals import db
from flask_login import current_user
from web_app.tournaments import places_app
import json
from config import Config

PLACE_PATH_TAIL = 'places_photos'


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


def get_ext(filename):
    return filename.rsplit('.', 1)[1].lower()


class Result:
    def __init__(self, result, message=''):
        self.result = result
        self.message = message


def validateForm(form):
    name = form.get('name')
    if not name:
        return Result(False, 'Не заполнено поле наименования')
    if db.session.execute(db.select(db.exists(Place).where(Place.place == name))).scalar():
        return Result(False, 'Место с таким наименованием в базе уже существует')
    return Result(True)


@places_app.route('/add', endpoint='add', methods=['POST'])
def add_place():
    if request.method == 'POST':
        validation = validateForm(request.form)
        if not validation.result:
            return json.dumps({
                'error': validation.message
            })
        new_place = Place(
            request.form.get('name'),
            json.loads(request.form.get('location')),
            request.form.get('address')
        )
        db.session.add(new_place)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return make_response(json.dumps({
                'status': 633,
                'statusText': f'не удалось добавить place "{request.form.get("name")}"'
            }), 633)
        if len(request.files) == 0:
            return json.dumps({
                'res': 'place добавлен, с фотографиями было б веселее, не находите? '
            })
        attributes = json.loads(request.form.get('attributes'))
        print(attributes)
        path = Config.SOURCE_PATH.joinpath(PLACE_PATH_TAIL, str(new_place.id))
        if not path.exists():
            path.mkdir(parents=True)
        for key in request.files.keys():
            file = request.files[key]
            ext = get_ext(file.filename)
            photo = PlacePhotos(new_place.id, ext, attributes[key])
            db.session.add(photo)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                continue
            file.save(path.joinpath(str(photo.id)).with_suffix(f'.{ext}'))
    return json.dumps({
        'res': 'place добавлен'
    })
