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
    spam = db.Column(db.Integer, nullable=False)

    def __init__(self, first_name, last_name, email, subject, message, date_created, ip_address, is_forwarded, spam):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.subject = subject
        self.message = message
        self.date_created = date_created
        self.ip_address = ip_address
        self.is_forwarded = is_forwarded
        self.spam = spam


blogpost_tags = db.Table(
    "blogpost_tags",
    db.Column("blogpost_id", db.Integer, db.ForeignKey("blogposts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)


class BlogPost(db.Model):
    __tablename__ = "blogposts"
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body_markdown = db.Column(db.String, nullable=False)
    body_html = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True) 
    blurb = db.Column(db.String(300))
    date_created = db.Column(db.String(30))
    tags = db.relationship(
        "Tag",
        secondary=blogpost_tags,
        backref=db.backref("blogposts", lazy="dynamic")
    )

    def __init__(self, title, body_markdown, body_html, slug, date_created, blurb):
        self.title = title
        self.body_markdown = body_markdown
        self.body_html = body_html
        self.slug = slug
        self.blurb = blurb
        self.date_created = date_created



class Tag(db.Model):
    __tablename__ = "tags"
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f"<Image {self.filename}>"
