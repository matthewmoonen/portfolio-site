# from datetime import datetime
from extensions import db


class messages(db.Model):
    __tablename__ = "mymessages"
    _id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100))
    message = db.Column(db.String(2000), nullable=False)
    date_created = db.Column(db.String(30))
    ip_address = db.Column(db.String)
    is_forwarded = db.Column(db.Integer, nullable=False)


    def __init__(self, first_name, last_name, email, subject, message, date_created, ip_address, is_forwarded):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.subject = subject
        self.message = message
        self.date_created = date_created
        self.ip_address = ip_address
        self.is_forwarded = is_forwarded


class BlogPost(db.Model):
    __tablename__ = "blogposts"
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)
    blurb = db.Column(db.String(300))
    date_created = db.Column(db.String(30))


    def __init__(self, title, body, slug, date_created, blurb):
        self.title = title
        self.body = body
        self.slug = slug
        self.blurb = blurb
        self.date_created = date_created