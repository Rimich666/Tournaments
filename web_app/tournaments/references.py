import json

from flask import (
    render_template,
    # redirect,
    url_for,
    request,
    make_response
)
from flask_login import current_user
from werkzeug.urls import url_parse
from ..globals import db

from web_app.tournaments import references_app
from web_app.globals import models
from web_app.functions.debug_info import debug_info

# list_reference = [
#     ['teams', 'Команды'],
#     ['persons', 'Персоны'],
#     ['referees', 'Судьи'],
#     ['sport_types', 'Виды спорта'],
#     ['speciality', 'Дисциплины'],
#     ['category', 'Категории'],
#     ['cards', 'Карточки'],
# ]

list_reference = [
    'teams',
    'persons',
    'referees',
    'sport_types',
    'speciality',
    'category',
    'cards',
]

fields = {
    'teams': ['team'],
    'persons': ['surname', 'name', 'patronymic', 'birthday', 'gender'],
    'referees': ['pers_id'],
    'sport_types': ['type'],
    'speciality': ['type_id', 'spec'],
    'category': ['category'],
    'cards': ['number', 'hard_id'],
}


def get_table_caption(name):
    if 'alt_name' in db.metadata.tables[name].info:
        return db.metadata.tables[name].info['alt_name']
    return name


def get_column_caption(mod, name):
    col = getattr(mod, name)
    if 'alt_name' in col.info:
        return col.info['alt_name']
    return name


def get_columns_captions(ind):
    tn = list_reference[ind]
    columns = fields[tn]
    return [get_column_caption(models[tn], c) for c in columns]


@references_app.route('/<int:ind>', endpoint='ind')
def reference(ind):
    if 'Referer' not in request.headers or url_parse(request.headers['Referer']).path != url_for(
            'references_app.references'):
        return make_response('Нет такой страницы', 404)
    tn = list_reference[ind]
    res = db.session.execute(db.select(models[tn])).scalars()

    returned = {
        'name': tn,
        'fields': fields[tn],
        'head': get_table_caption(tn),
        'captions': get_columns_captions(ind),
        'rows': [[str(getattr(r, f)) for f in fields[tn]] for r in res]
    }

    return json.dumps(returned)


@references_app.route('/', endpoint='references')
def references():
    # res = db.session.execute(db.select(Place)).scalars()
    # rows = []
    # count = 1
    # for row in res:
    #     rows.append({
    #         'id': row.id,
    #         'place': row.place,
    #         'location': {
    #             'lat': row.lat,
    #             'lng': row.lng,
    #         },
    #         'address': row.address
    #     })
    #     for photo in row.photos:
    #         print(photo)
    #     count += count
    #     print(row.place)
    captions = [get_table_caption(r) for r in list_reference]
    return render_template('references.html', user=current_user, auth=current_user.is_authenticated,
                           references=captions
                           )
