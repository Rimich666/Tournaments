from ..globals import db
from werkzeug.exceptions import InternalServerError
from sqlalchemy.exc import IntegrityError
import json
from . import QueryTable


def make_test_data():
    with open("./dataJSON.json", "r", encoding='utf-8-sig') as read_file:
        data = json.load(read_file)
    for tbl in db.metadata.sorted_tables:
        #    for tb in data:
        tb = tbl.name
        qt = QueryTable(tb)
        pk = qt.primary_key['constrained_columns']
        if tb in data.keys():
            for rec in data[tb]:
                if len(pk) > 0:
                    st = {col: rec[col] for col in pk}
                else:
                    st = rec
                if qt.query(st) is None:
                    qt.add(rec)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InternalServerError("failed to write data to the database")


def delete_data():
    eng = db.get_engine()
    for tbl in reversed(db.metadata.sorted_tables):
        eng.execute(tbl.delete())
    pass
