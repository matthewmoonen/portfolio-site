from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField

class ContactForm(FlaskForm):
    first_name = StringField('firstName')
    last_name = StringField('lastName')
    email = EmailField('email')
    message = StringField('message')
    submit = SubmitField('submit')

class BlogSubmitForm(FlaskForm):
    title = StringField('title')
    markdown_body = StringField('markdown_body')
    html_body = StringField('html_body')
    blurb = StringField('blurb')
    slug = SubmitField('slug')
    submit = SubmitField('submit')