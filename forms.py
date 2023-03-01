from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField

class ContactForm(FlaskForm):
    first_name = StringField('firstName')
    last_name = StringField('lastName')
    email = EmailField('email')
    message = StringField('message')
    submit = SubmitField('submit')