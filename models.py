from extensions import db


class messages(db.Model):
    __tablename__ = "mymessages"
    id = db.Column("id", db.Integer, primary_key=True)
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
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    markdown_raw = db.Column(db.String, nullable=True)
    body_markdown = db.Column(db.String, nullable=True)
    body_html = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String, nullable=True) 
    blurb = db.Column(db.String(300))
    date_created = db.Column(db.String(30))
    title_image = db.Column(db.LargeBinary, nullable=True)
    hero_image = db.Column(db.LargeBinary, nullable=True)
    title_image_extension = db.Column(db.String(10), nullable=True)
    hero_image_extension = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(10), nullable=False, default='draft')  # 'draft' or 'published'

    tags = db.relationship(
        "Tag",
        secondary=blogpost_tags,
        backref=db.backref("blogposts", lazy="dynamic")
    )

    published_post = db.relationship("PublishedPost", uselist=False, backref="blogpost", lazy="joined")

    __table_args__ = (
        db.CheckConstraint(
            "(status = 'draft') OR (title IS NOT NULL AND body_html IS NOT NULL)",
            name="ck_published_non_null"
        ),
    )

    def __init__(self, title=None, markdown_raw=None, body_markdown=None, body_html=None, slug=None, date_created=None, blurb=None, 
                 title_image=None, title_image_extension=None, hero_image=None, hero_image_extension=None, status='draft'):
        self.title = title
        self.markdown_raw = markdown_raw
        self.body_markdown = body_markdown
        self.body_html = body_html
        self.slug = slug
        self.blurb = blurb
        self.date_created = date_created
        self.title_image = title_image
        self.title_image_extension = title_image_extension
        self.hero_image = hero_image
        self.hero_image_extension = hero_image_extension
        self.status = status

    @property
    def published_slug(self):
        """Returns the slug from the published_posts table if available."""
        return self.published_post.slug if self.published_post else None

    @property
    def is_published(self):
        """Checks if the post is published based on the published_posts table."""
        return self.published_post is not None

    def publish(self):
        """Creates a published post entry for the blog post."""
        if not self.published_post:
            new_published_post = PublishedPost(blogpost_id=self.id, slug=self.slug)
            db.session.add(new_published_post)
            db.session.commit()
            self.status = 'published'
            db.session.commit()






class PublishedPost(db.Model):
    __tablename__ = "published_posts"
    slug = db.Column(db.String(150), primary_key=True)
    blogpost_id = db.Column(db.Integer, db.ForeignKey("blogposts.id"))


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    extension = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Image ID: {self.id}, Extension: {self.extension}>"


class ImageRef(db.Model):
    __tablename__ = "image_refs"
    id = db.Column(db.String(50), primary_key=True)  # Random string identifier
    blogpost_id = db.Column(db.Integer, db.ForeignKey("blogposts.id"), nullable=True)  # Nullable foreign key to BlogPost
    filename = db.Column(db.String(100), nullable=False)  # Original filename
    extension = db.Column(db.String(10), nullable=False)  # File extension (e.g., jpg, png)
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"), nullable=False)  # Non-nullable reference to Image

    blogpost = db.relationship("BlogPost", backref="image_refs")
    image = db.relationship("Image", backref="image_refs")

    def __init__(self, id, blogpost_id, filename, extension, image_id):
        self.id = id
        self.blogpost_id = blogpost_id
        self.filename = filename
        self.extension = extension
        self.image_id = image_id

    def __repr__(self):
        return f"<ImageRef {self.filename}.{self.extension} (ID: {self.id}, Image ID: {self.image_id})>"


class ImageRefUsage(db.Model):
    __tablename__ = "image_ref_usage"
    id = db.Column(db.String(50), primary_key=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"<ImageRefUsage ID: {self.id}>"
