from werkzeug.exceptions import InternalServerError
from sqlalchemy.exc import IntegrityError
from flask import (
    render_template,
    redirect,
    request,
    url_for)
from sqlalchemy import (
    inspect)
from sqlalchemy.sql import sqltypes
import json

from ..functions.debug_info import debug_info
from ..globals import (
    db,
    admin
)
from ..models import (
    User,
    Role
)
from ..functions import (
    QueryTable,
    delete_data,
    make_test_data,
    TableInform
)
from ..forms import AddDefault
from ..forms.login_forms import RegForm
from ..admin import admin_app

DATA = 'Data'
METADATA = 'Metadata'
ADMIN_INDEX = "admin/admin_index.html"

param = {
    'tables': {t: TableInform(db.metadata.tables[t].info) for t in db.metadata.tables.keys()},
    'cur_table': '_',
    'navtabs': [DATA, METADATA],
    'cur_navtab': 'Data',
    'data': False,
    'fields': []
}


def get_data(qt):
    return db.session.query(qt.table).all()


def get_metadata(qt):
    dct = {}
    if len(qt.columns) > 0:
        dct['columns'] = qt.table_col
    if len(qt.foreign_keys) > 0:
        dct['foreign_keys'] = qt.foreign_keys
    if len(qt.indexes):
        dct['indexes'] = qt.indexes
    dct['primary_key'] = [qt.primary_key]
    return dct


functions = {DATA: get_data, METADATA: get_metadata}


def columns(table):
    eng = db.get_engine()
    insp = inspect(eng)
    cols = insp.get_columns(table)
    for col in cols:
        if isinstance(col['type'], sqltypes.INTEGER) or isinstance(col['type'], sqltypes.NUMERIC):
            col['type_field'] = 'number'
        elif isinstance(col['type'], sqltypes.DATETIME) or isinstance(col['type'], sqltypes.TIMESTAMP):
            col['type_field'] = 'datetime'
        else:
            col['type_field'] = 'text'
    return columns


@admin_app.route("/", endpoint='index')
@admin.require()
def list_tables():
    debug_info(param)
    return render_template(ADMIN_INDEX, param=param)


@admin_app.route("/delete_all", endpoint='delete_all')
@admin.require()
def delete_all():
    delete_data()
    return redirect(url_for('admin_app.index'))


@admin_app.route("/load_trial", endpoint='load_trial')
@admin.require()
def load_data():
    make_test_data()
    return redirect(url_for('admin_app.index'))


@admin_app.route("/<navtab>/<table>", endpoint='table')
@admin.require()
def sel_table(table, navtab):
    if table == '_':
        return render_template(ADMIN_INDEX, param=param)
    qt = QueryTable(table)
    param['cur_table'] = table
    param['cur_navtab'] = navtab
    keys = db.metadata.tables.keys()
    if table in keys:
        primary_key = qt.primary_key['constrained_columns']
        param['fields'] = [{'name': col, 'pk': col in primary_key} for col in qt.columns]
        param['data'] = functions[navtab](qt)
        param['exist_pk'] = (len(primary_key) > 0)
    templ_name = 'admin/' + navtab.lower() + '.html'
    return render_template(templ_name, param=param)


@admin_app.route("/Data/<table>/<key_fields>/", endpoint="details")
@admin.require()
def get_details(table, key_fields):
    templ_name = 'admin/details.html'
    kf = json.loads(key_fields.replace('{{', '{').replace('}}', '}'))
    qr = QueryTable(table)
    param['fields'] = qr.fields(kf)

    return render_template(templ_name, param=param)


@admin_app.route("/Data/<table>/<key_fields>/delete", endpoint="delete")
@admin.require()
def delete_record(table, key_fields):
    kf = json.loads(key_fields.replace('{{', '{').replace('}}', '}'))
    if table == 'users':
        user = User.query.filter_by(id=kf['id']).first()
        if user.role.role == 'admin':
            return redirect(url_for('admin_app.table', table=table, navtab='Data'))
    if table == 'roles':
        role = Role.query.filter_by(id=kf['id']).first()
        if role.role == 'admin':
            return redirect(url_for('admin_app.table', table=table, navtab='Data'))

    qt = QueryTable(table)
    qt.delete(kf)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InternalServerError("could not delete data from the database")
    return redirect(url_for('admin_app.table', table=table, navtab='Data'))
    pass


@admin_app.route("/Data/<table>/add", methods=['GET', 'POST'])
@admin.require()
def add(table):
    qr = QueryTable(table)
    if table == 'users':
        form = RegForm()
        form.role.choices = [(r.id, r.role) for r in Role.query.filter(Role.role != 'admin').all()]
    else:
        form = AddDefault(qr.table_col)
    template = 'admin/' + qr.model.add_templ + '.html'
    if request.method == 'GET':
        return render_template(template, form=form, param=param)

    if form.validate_on_submit():
        if table == 'users':
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            user.role_id = int(form.role.data)
            user.phone_number = form.phone.data
            db.session.add(user)
        else:
            qr.add(form)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise InternalServerError("failed to write data to the database")
    else:
        debug_info(form.errors)

    return redirect(url_for('admin_app.table', table=table, navtab='Data'))

    pass
