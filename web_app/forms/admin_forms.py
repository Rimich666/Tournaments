from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DecimalField,
    DateTimeField,
)
from wtforms.widgets import TextInput
from wtforms.widgets import (
    NumberInput,
    DateTimeInput,

)
from wtforms.validators import (
    InputRequired,
)

from web_app.functions.debug_info import debug_info

types_field = {
    'VARCHAR': {'ftype': StringField, 'widget': TextInput()},
    'INTEGER': {'ftype': IntegerField, 'widget': NumberInput()},
    'NUMERIC': {'ftype': DecimalField, 'widget': NumberInput()},
    'TIMESTAMP': {'ftype': DateTimeField, 'widget': DateTimeInput()},
    'DATETIME': {'ftype': DateTimeField, 'widget': DateTimeInput()},
    'DATE': {'ftype': DateTimeField, 'widget': DateTimeInput()}
}


def create_add_form(Class):
    def create_form(columns):
        field_list = Class.field_list
        for field in field_list:
            delattr(Class, field)

        field_list = []
        for col in columns:
            if col['autoincrement']:
                continue
            fieldname = col['name']
            strt = col['type'].__visit_name__
            setattr(Class, fieldname,
                    types_field[strt]['ftype'](fieldname.capitalize(), validators=[InputRequired()],
                                               widget=types_field[strt]['widget']))
            field_list.append(fieldname)
            setattr(Class, 'List', StringField(str(field_list)))
        Class.field_list = field_list
        form = Class()
        return form

    return create_form


@create_add_form
class AddDefault(FlaskForm):
    # field_list = HiddenField(None)
    field_list = []
    # def __init__(self, field_list):
    #     self.field_list = ",".join(field_list)

    pass


class Templ:
    add_templ = 'add_default'
    repr_templ = ''
    many_to_many = False
    headers = {'default': 'Заголовок не задан'}
    relations = {}
    is_association = False

    def header(self, col, obj):
        if col in self.headers.keys():
            return self.headers[col]
        else:
            if obj == self:
                return col
            else:
                return self.headers['default']

    def repr(self, col=''):
        return getattr(self, col)

    def relation(self, col):
        if col in self.relations.keys():
            return getattr(self, self.relations[col])
        else:
            return self
