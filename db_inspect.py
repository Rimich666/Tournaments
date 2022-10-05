from app import app
from datetime import datetime

from web_app.functions import QueryTable
from web_app.functions.debug_info import debug_info
from web_app.globals import db

if __name__ == '__main__':
    with app.app_context():
        qt = QueryTable('places')
        debug_info(qt.table.name)
        debug_info(qt.table.info)
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
