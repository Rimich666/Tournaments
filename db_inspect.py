from app import app
from datetime import datetime

from web_app.functions import QueryTable
from web_app.functions.debug_info import debug_info
from web_app.globals import db
from web_app.globals import models
fields = {
    'teams': ['team'],
    'persons': ['surname', 'name', 'patronymic', 'birthday', 'gender'],
    'referees': ['pers_id'],
    'sport_types': ['type'],
    'speciality': ['spec', 'type_id'],
    'category': ['category'],
    'cards': ['number', 'hard_id'],
    'sportsmen': ['person', 'team']
}

if __name__ == '__main__':
    with app.app_context():
        qt = QueryTable('persons')
        # debug_info(qt.table.name)
        # debug_info(qt.table.info)
        # debug_info(qt.model.metadata.tables['persons'].info)
        # for col in qt.columns:
        #     debug_info(getattr(qt.model, col).info)
        #

        #qt = QueryTable(tn)
        # sportsmen = qt.model
        # debug_info(getattr(sportsmen, 'person'))
        tn = 'sportsmen'
        obj = models[tn]
        columns = fields[tn]
        for col in columns:
            debug_info(getattr(obj, col).info['alt_name'])
            debug_info(getattr(obj, col))
        res = db.session.execute(db.select(obj)).scalars()
        for row in res:
            debug_info(f'{getattr(row, "person")}, {row.team}')
#     #        make_test_data()
#     dt = datetime.now()
#     product_id = 2
#     pt_id = 1
#     prices = db.session.query(Price).filter(Price.pt_id == pt_id, Price.product_id == product_id,
#                                             Price.date <= dt).order_by(Price.date.desc()).all()
#     price = db.session.query(Price).filter(Price.pt_id == pt_id, Price.product_id == product_id,
#                                             Price.date <= dt).order_by(Price.date.desc()).first()
#     print(price.id, price.date, price.product.product_name, price.price)
#     print('======================')
#     for price in prices:
#         print(price.id, price.date, price.product.product_name, price.price)
#     print(type(rows))
pass
