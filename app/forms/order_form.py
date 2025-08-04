# app/forms/order_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField  

class OrderForm(FlaskForm):
    customer_name = StringField('Customer Name')
    menu_items = SelectMultipleField('Select Items')  
    submit = SubmitField('Place Order')
