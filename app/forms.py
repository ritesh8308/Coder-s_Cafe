from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectMultipleField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    table_number = IntegerField("Table Number", validators=[DataRequired()])
    menu_items = SelectMultipleField("Select Items", coerce=int, validators=[DataRequired()])
