from flask import Flask, render_template, redirect, request, session, url_for, flash, jsonify, abort, send_file
from german.german import german_app
from forms import ContactForm, BlogSubmitForm
from datetime import datetime
import secrets
from models import messages, BlogPost, Tag, Image, ImageRef, ImageRefUsage
from extensions import db
from functools import wraps
from flask_session import Session
import redis
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import logging
from sqlalchemy import desc
from sqlalchemy import text as sqlalchemytext
from markdown import markdown
import random
import string
import hashlib
from sqlalchemy.orm.exc import NoResultFound
import io
import re

logging.basicConfig(filename='record.log', level=logging.DEBUG)


# Instantiate the Flask application
app = Flask(__name__)


""" Specify static pathway locations. In this case, I am using both 
regular static within the Flask app, and an external directory where 
userfiles are to be located """
# Server static files from the regular Flask app location
app.static_folder = 'static'
app.static_url_path = '/static'


# Serve static files from a directory outside the Flask app directory
app.add_url_rule('/userdata/<path:filename>', endpoint='userdata', view_func=app.send_static_file, subdomain='', defaults={'filename': ''})
app.config['EXTERNAL_STATIC_FOLDER'] = '/home/matthew/userdata'


# Load environment variables from file and make accessible to project
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "environmentvariables.env")    )
flask_environment = os.getenv("FLASK_ENV")
print("flask environment:" + str(flask_environment))


# Return German learning game as a blueprint/modular app
app.register_blueprint(german_app, url_prefix="/german")
    

# Create secret key securely
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)


# Set redis connection details
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
redis_password = os.getenv("REDIS_PASSWORD", "")

# Register static route for image upload path
app.add_url_rule('/userdata/<path:filename>', endpoint='userdata', view_func=app.send_static_file, subdomain='')


# Configure image uploads
app_root = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = "/home/matthew/userdata/admin"
ALLOWED_EXTENSIONS = {'svg', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER







# Configure SQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure session cookies
app.config['SESSION_COOKIE_DOMAIN'] = '.matthewmoonen.com'
app.config['SESSION_COOKIE_PATH'] = '/'
if os.getenv("FLASK_ENV")  == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True


# Configuration of Redis which allows multiple workers to access the same session credentials on the VPS
app.config['SESSION_TYPE'] = 'redis'
app.config["SESSION_REDIS"] = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
if os.getenv("FLASK_ENV") == 'production':
    Session(app)


# Initialise the database
db.init_app(app)


# Create DB for contact form if not already exists
with app.app_context():
    db.create_all()




def create_sqlite_triggers():

    delete_orphan_images_trigger = sqlalchemytext("""
    CREATE TRIGGER IF NOT EXISTS delete_orphaned_images
    AFTER DELETE ON image_refs
    BEGIN
        DELETE FROM image
        WHERE id = OLD.image_id
        AND NOT EXISTS (SELECT 1 FROM image_refs WHERE image_id = OLD.image_id);
    END;
    """)

    # Trigger to update ImageRef with blogpost_id
    update_trigger_sql = sqlalchemytext("""
    CREATE TRIGGER IF NOT EXISTS update_image_refs
    AFTER INSERT ON image_ref_usage
    BEGIN
        UPDATE image_refs
        SET blogpost_id = (SELECT MAX(id) FROM blogposts)
        WHERE id = NEW.id;
    END;
    """)

    # Trigger to delete unused image references
    delete_trigger_sql = sqlalchemytext("""
    CREATE TRIGGER IF NOT EXISTS delete_unused_images
    AFTER INSERT ON image_ref_usage
    BEGIN
        DELETE FROM image_refs
        WHERE blogpost_id IS NULL
        AND id NOT IN (SELECT id FROM image_ref_usage);
    END;
    """)


    # delete_blogpost_images = sqlalchemytext("""
    # CREATE TRIGGER IF NOT EXISTS delete_blogpost_images
    # AFTER DELETE ON blogposts
    # BEGIN
    #     DELETE FROM image_refs
    #     WHERE blogpost_id = OLD.id;
    # END;
    # """)

    with db.engine.connect() as connection:
        connection.execute(delete_orphan_images_trigger)
        connection.execute(update_trigger_sql)
        connection.execute(delete_trigger_sql)
        # connection.execute(delete_blogpost_images)



def create_image_ref_usage_table():
    

    with db.engine.connect() as connection:
        connection.execute(sqlalchemytext("""
        CREATE TABLE IF NOT EXISTS image_ref_usage (
            id TEXT PRIMARY KEY
        );
        """))


with app.app_context():
    create_image_ref_usage_table()
    create_sqlite_triggers()


# Store hashed password for admin panel in .env to prevent exposing to GitHub
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")



# Start of routes. Index is the landing page.
@app.route("/", methods=['GET', 'POST'])
    # # Uncomment to enable debugging of this route or copy/paste to another route to start debugging
    # app.logger.info('Hello, world!')
    # app.debug = True
    # app.logger.debug('this is a DEBUG message')
    # app.logger.info('this is an INFO message')
    # app.logger.warning('this is a WARNING message')
    # app.logger.error('this is an ERROR message')
    # app.logger.critical('this is a CRITICAL message')

    # Contact form submits to a SQL database. 
    # If using this form, you need a separate Python script and chron job to forward the emails.
    
def index():
    recent_posts = db.session.query(BlogPost).order_by(BlogPost.id.desc()).limit(4).all()
    for i, post in enumerate(recent_posts):
        post.number = i
        parsed_date = datetime.strptime(post.date_created, "%Y-%m-%d, %H:%M:%S")
        post.formatted_date = parsed_date.strftime("%B %d, %Y")

        # Use default image path if title_image is None
        post.title_image_url = "/static/img/terminal.png" if post.title_image is None else f"/image/{post.id}"

    form = ContactForm()
    if form.is_submitted():
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        subject = request.form['subject']
        honey1 = request.form['message']
        honey2 = request.form['phone']
        message = request.form['address']
        date_created = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

        # Get client IP address:
        if 'X-Forwarded-For' in request.headers:
            ip_address = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
        else:
            ip_address = request.remote_addr or 'untrackable'

        is_forwarded = 0

        """
        Spam = 0: Neither of the honeypot entries have been filled. Likely legit.
        Spam = 1: One of the honeypot entries has been filled. Almost certainly spam.
        Spam = 2: Neither of the honeypot entries have ben filled but there's no message body. A bit suspect.
        """
        if honey1 != "" or honey2 != "":
            spam = 1
        elif message == "":
            spam = 2
        else:
            spam = 0

        formdata = messages(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message, date_created=date_created, ip_address=ip_address, is_forwarded=is_forwarded, spam=spam)
        try:
            db.session.add(formdata)
            db.session.commit()
        except Exception as e:
            print(e)
            return render_template('oops.html')
        else:
            return render_template('thanks.html', first_name=first_name)


    return render_template("index.html", recent_posts=recent_posts)




def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session or os.getenv('FLASK_ENV') == 'development':
            return f(*args, **kwargs)
        else:
            flash("You need to log in first!")
            return redirect(url_for("login"))
    return wrap



@app.route("/admin/")
@login_required
def admin():
    session["mykey"] = "myvalue"
    posts = db.session.query(BlogPost).all()
    return render_template("admin.html", posts=posts)


# Check that uploaded image's file extension is valid.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/messages')
@login_required
def display_messages():
    messages_list = db.session.query(
        messages.id,
        messages.first_name,
        messages.last_name,
        messages.email,
        messages.subject,
        messages.message,
        messages.date_created,
        messages.ip_address
    ).filter(
        messages.spam == 0,
        messages.is_forwarded == 0
    ).order_by(desc(messages.date_created)).all()

    return render_template('messages.html', messages=messages_list)



@app.route('/spam')
@login_required
def display_spam():
    messages_list = db.session.query(
        messages.id,
        messages.first_name,
        messages.last_name,
        messages.email,
        messages.subject,
        messages.message,
        messages.date_created,
        messages.ip_address
    ).filter(
        messages.spam.in_([1, 2]),
        messages.is_forwarded == 0
    ).order_by(
        desc(messages.spam),
        desc(messages.date_created)
    ).all()

    return render_template('spam.html', messages=messages_list)



@app.route('/delete_spam/<int:message_id>', methods=['POST'])
@login_required
def mark_spam_deleted(message_id):
    message_to_update = db.session.get(messages, message_id)
    try:
        message_to_update.is_forwarded = 2
        db.session.commit()
        flash('Message marked as deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating message: ' + str(e), 'danger')
    return redirect(url_for('display_spam'))



@app.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def mark_as_deleted(message_id):
    message_to_update = db.session.get(messages, message_id)
    try:
        message_to_update.is_forwarded = 2
        db.session.commit()
        flash('Message marked as deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating message: ' + str(e), 'danger')
    return redirect(url_for('display_messages'))


# # Handle upload
# """ TODO: See here to improve security and performance
# https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
# """
# @app.route('/upload', methods=['GET', 'POST'])
# @login_required
# def upload_file():
#     session["mykey"] = "myvalue"
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('admin', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''



@app.route('/blog/<slug>/')
def blog_post(slug):
    post = db.session.query(BlogPost).filter_by(slug=slug).first()
    if post:
        
        parsed_date = datetime.strptime(post.date_created, "%Y-%m-%d, %H:%M:%S")
        formatted_date = parsed_date.strftime("%B %d, %Y")

        hero_image_url = (
            f"/blog/{post.slug}/hero/hero-image.png"
            if post.hero_image
            else "/static/img/hero.jpg"
        )

        return render_template("base/blog-template.html", post=post, slug=slug, hero_image_url=hero_image_url, formatted_date=formatted_date)
    else:
        return f"404"


@app.route("/mostrecent/")
def most_recent():
    recent_posts = db.session.query(BlogPost).order_by(BlogPost.id.desc()).limit(2).all()
    return render_template("most_recent.html", recent_posts=recent_posts)


@app.route("/blog/")
def blog():
    posts = db.session.query(BlogPost).all()
    return render_template("blog.html", posts=posts)



def ensure_unique_slug(slug):
    base_slug = slug.strip().replace(" ", "-")
    existing_slug = BlogPost.query.filter_by(slug=base_slug).first()
    if not existing_slug:
        return base_slug
    else:
        characters = string.ascii_letters + string.digits
        return f"{base_slug}-{''.join(random.choices(characters, k=11))}"

def title_to_slug(blogpost_title):
    blogpost_title = blogpost_title.lower()
    blogpost_title = re.sub(r'[^a-z0-9\s]', '', blogpost_title)
    blogpost_title = re.sub(r'\s+', '-', blogpost_title)
    blogpost_title = blogpost_title.strip('-')
    return blogpost_title



def generate_random_string(length=11):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def extract_image_references(text_body):
    # List to store extracted references
    references = []

    # Regex for HTML <img> tags (extract `src` attribute)
    html_img_regex = r'<img\s+[^>]*src="([^"]+)"'
    html_matches = re.findall(html_img_regex, text_body)
    for match in html_matches:
        # Extract filename from the src URL
        filename = match.split("/")[-1].split(".")[0]  # Extract filename without extension
        references.append(filename)

    # Regex for Markdown ![]() image references
    markdown_img_regex = r'!\[.*?\]\(([^)]+)\)'
    markdown_matches = re.findall(markdown_img_regex, text_body)
    for match in markdown_matches:
        # Extract filename from the URL
        filename = match.split("/")[-1].split(".")[0]  # Extract filename without extension
        references.append(filename)

    return references












def replace_reference(text, slug, reference):
    
    pattern = rf'(/images/){re.escape(reference)}(\.[a-zA-Z0-9]+)'

    def fetch_filename(match):
        ref_id = reference
        image_ref = ImageRef.query.filter_by(id=ref_id).first()
        if image_ref:
            return f"/blog/{slug}/{image_ref.filename}.{image_ref.extension}"
        else:
            return match.group(0)

    replaced_text = re.sub(pattern, fetch_filename, text)

    return replaced_text


@app.route('/add_entry/', methods=['GET'])
@login_required
def render_add_entry():
    return render_template('add_entry.html')

@app.route('/add_entry/', methods=['POST'])
@login_required
def add_entry():
    title = request.form['title']
    body = request.form['body']
    blurb = request.form['blurb']
    slug = request.form['slug'] or title.lower().replace(' ', '-')
    slug = re.sub(r'[^a-zA-Z0-9-]', '', slug)
    date_created = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    references = extract_image_references(body)
    ImageRefUsage.query.delete()
    
    for reference in references:
        body = replace_reference(text=body, slug=slug, reference=reference)
        db.session.add(ImageRefUsage(id=reference))
    db.session.commit()

    blogdata = BlogPost(
        title=title,
        body_markdown=body,
        body_html=markdown(body),
        slug=slug,
        blurb=blurb,
        date_created=date_created
    )
    db.session.add(blogdata)
    db.session.commit()

    # Update `ImageRef` with blogpost_id
    used_refs = ImageRefUsage.query.all()
    used_ids = [ref.id for ref in used_refs]
    ImageRef.query.filter(ImageRef.id.in_(used_ids)).update(
        {"blogpost_id": blogdata.id}, synchronize_session=False
    )

    # Delete unused `ImageRef` entries
    unused_refs = ImageRef.query.filter(ImageRef.blogpost_id.is_(None)).all()
    for unused in unused_refs:
        db.session.delete(unused)
    db.session.commit()

    flash("New entry was successfully added")
    return redirect(url_for("admin"))



@app.route('/upload_images', methods=['POST'])
@login_required
def upload_images():
    if 'images' not in request.files:
        return jsonify({"success": False, "error": "No files uploaded"})

    uploaded_files = request.files.getlist('images')
    new_refs = []

    for file in uploaded_files:
        if allowed_file(file.filename):
            file_data = file.read()

            # Extract filename and extension
            filename, file_extension = os.path.splitext(file.filename)
            file_extension = file_extension.lower().lstrip('.')

            # Check if the image already exists in the database
            existing_image = Image.query.filter_by(data=file_data).first()

            # If the image does not exist, add it to the Image table
            if not existing_image:
                new_image = Image(data=file_data, extension=file_extension)
                db.session.add(new_image)
                db.session.flush()  # Flush to get the new image ID
                image_id = new_image.id
            else:
                image_id = existing_image.id

            # Generate a new reference ID
            ref_id = generate_random_string()

            # Check for filename conflicts
            existing_ref = ImageRef.query.filter_by(
                filename=filename, extension=file_extension, blogpost_id=None
            ).first()

            if existing_ref:
                # Adjust filename to include the new reference
                filename = f"{filename}-{ref_id}"

            # Add a reference to the image_refs table
            new_ref = ImageRef(
                id=ref_id,
                blogpost_id=None,
                filename=filename,
                extension=file_extension,
                image_id=image_id
            )
            db.session.add(new_ref)
            new_refs.append({
                "ref_id": ref_id,
                "filename": f"{filename}.{file_extension}",
                "image_id": image_id
            })

    db.session.commit()
    return jsonify({"success": True, "new_refs": new_refs})






@app.route('/delete_image/<string:ref_id>', methods=['POST'])
@login_required
def delete_image(ref_id):
    # Query the ImageRef entry using the primary key
    image_ref = ImageRef.query.get(ref_id)
    if not image_ref:
        return jsonify({"success": False, "error": "Image reference not found"})

    # Delete the ImageRef entry
    db.session.delete(image_ref)
    db.session.commit()

    # Fetch remaining references
    remaining_refs = [
        {"id": ref.id, "filename": f"{ref.filename}.{ref.extension}"}
        for ref in ImageRef.query.all()
    ]
    return jsonify({"success": True, "remaining_refs": remaining_refs})


@app.route('/images/<string:primary_key>', methods=['GET'])
@app.route('/images/<string:primary_key>.<string:extension>', methods=['GET'])
@app.route('/images/<string:primary_key>/<string:filename>.<string:extension>', methods=['GET'])
def serve_image(primary_key, filename=None, extension=None):
    # Query the ImageRef entry using the primary key
    if extension:
        image_ref = ImageRef.query.filter_by(id=primary_key, extension=extension).first()
    else:
        image_ref = ImageRef.query.filter_by(id=primary_key).first()

    if not image_ref:
        abort(404, description="Image reference not found")

    # Ensure the filename matches if provided
    if filename and image_ref.filename != filename:
        abort(404, description="Filename mismatch")

    # Query the corresponding Image entry
    image = db.session.get(Image, image_ref.image_id)
    
    if not image:
        abort(404, description="Image not found")

    # Serve the image data
    return send_file(
        io.BytesIO(image.data),
        mimetype=f"image/{image_ref.extension}",
        as_attachment=False,
        download_name=f"{image_ref.filename}.{image_ref.extension}"
    )




@app.route('/blog/<string:slug>/<string:filename>.<string:extension>', methods=['GET'])
def serve_blog_image(slug, filename, extension):
    # Query the BlogPost using the slug
    blog_post = BlogPost.query.filter_by(slug=slug).first()
    if not blog_post:
        abort(404, description="Blog post not found")

    # Query the ImageRef entry using the blogpost ID, filename, and extension
    image_ref = ImageRef.query.filter_by(
        blogpost_id=blog_post.id,
        filename=filename,
        extension=extension
    ).first()

    if not image_ref:
        abort(404, description="Image reference not found")

    image = db.session.get(Image, image_ref.image_id)
    if not image:
        abort(404, description="Image not found")

    # Serve the image data
    return send_file(
        io.BytesIO(image.data),
        mimetype=f"image/{image_ref.extension}",
        as_attachment=False,
        download_name=f"{image_ref.filename}.{image_ref.extension}"
    )




@app.route('/update_image_filename/<string:ref_id>', methods=['POST'])
@login_required
def update_image_filename(ref_id):
    data = request.get_json()
    new_filename = data.get('filename')

    if not new_filename:
        return jsonify({"success": False, "error": "Filename is required"})

    # Query the ImageRef entry
    image_ref = ImageRef.query.get(ref_id)
    if not image_ref:
        return jsonify({"success": False, "error": "Image reference not found"})

    # Check for duplicate filename and extension with blogpost_id = NULL
    duplicate_ref = ImageRef.query.filter_by(
        filename=new_filename,
        extension=image_ref.extension,
        blogpost_id=None
    ).first()

    if duplicate_ref and duplicate_ref.id != ref_id:
        return jsonify({
            "success": False,
            "error": "Duplicate filename detected.",
            "original_filename": image_ref.filename
        })

    # Update the filename
    image_ref.filename = new_filename
    db.session.commit()

    return jsonify({"success": True, "filename": new_filename})



@app.route('/get_uploaded_images', methods=['GET'])
@login_required
def get_uploaded_images():
    # Query ImageRef entries where blogpost_id is NULL
    image_refs = ImageRef.query.filter_by(blogpost_id=None).all()
    
    # Create a list of dictionaries with the required fields
    images = [
        {"id": img_ref.id, "filename": img_ref.filename, "extension": img_ref.extension}
        for img_ref in image_refs
    ]
    
    return jsonify({"success": True, "images": images})



@app.route('/edit_entry/<int:id>/', methods=['GET'])
@login_required
def render_edit_entry(id):
    post = BlogPost.query.filter_by(id=id).first()
    if post is None:
        abort(404)

    form = BlogSubmitForm(obj=post)
    form.markdown_body.data = post.body_markdown
    form.slug.data = post.slug
    form.blurb.data = post.blurb
    
    return render_template('edit_entry.html', form=form, post=post, id=id)


@app.route('/edit_entry/<int:id>', methods=['POST'])
@login_required
def edit_entry(id):
    form = BlogSubmitForm()
    if form.is_submitted():
        title = request.form['title']
        body_markdown = request.form['body']
        blurb = request.form['blurb']
        slug = request.form['slug']
        if slug == "":
            slug = title_to_slug(title)
        
        tags_input = request.form['tags']

        blogpost = db.session.get(BlogPost, id)
        if not blogpost:
            abort(404)
        if not blogpost.slug == slug:
            slug = ensure_unique_slug(slug)

        blogpost.title = title
        blogpost.body_markdown = body_markdown
        blogpost.body_html = markdown(body_markdown)
        blogpost.blurb = blurb
        blogpost.slug = slug

        blogpost.tags = []
        if tags_input:
            tags = {tag.strip().upper() for tag in tags_input.split(',')}

            for tag_name in tags:
                if tag_name == "":
                    continue
                else:
                    existing_tag = Tag.query.filter_by(name=tag_name).first()
                    if existing_tag:
                        blogpost.tags.append(existing_tag)
                    else:
                        new_tag = Tag(name=tag_name)
                        blogpost.tags.append(new_tag)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"
        else:
            flash('Entry was successfully edited')
            return redirect(url_for('admin'))



# @app.route('/ul')
# def ul():

#     images = Image.query.all()
#     return render_template('upload.html', images=images)


# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'images' not in request.files:
#         flash('No file part')
#         return redirect(request.url)

#     files = request.files.getlist('images')

#     if not files:
#         flash('No selected file')
#         return redirect(request.url)

#     for file in files:
#         if file.filename:
#             new_image = Image(filename=file.filename, data=file.read())
#             db.session.add(new_image)

#     db.session.commit()
#     flash('Files successfully uploaded!')
#     return redirect(url_for('ul'))

# @app.route('/delete/<int:image_id>', methods=['POST'])
# def delete_image(image_id):
#     image = Image.query.get_or_404(image_id)
#     db.session.delete(image)
#     db.session.commit()
#     flash(f'{image.filename} has been deleted.')
#     return redirect(url_for('ul'))


# Login route. Currently there is only one login user as admin.
@app.route("/login/", methods=['GET', 'POST'])
def login():
    # If admin user already logged in, redirect to admin page.
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('admin'))
    error = None
    # Verify username/password for admin user logging in.
    if request.method == 'POST':
        # Handle incorrect credentials
        if request.form['username'] != 'admin' or not check_password_hash(ADMIN_PASSWORD_HASH, request.form['password']):
            error = 'invalid credentials; please try again'
        # Handle correct credentials
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('admin'))
    return render_template("login.html", error=error)


# User automatically logged out when they visit here
@app.route("/logout/")
@login_required
def logout():
    session["mykey"] = "myvalue"
    # "pop" the key off the session cookie
    session.pop("logged_in", None)
    flash("You were just logged out!")
    return redirect(url_for('logged_out'))


@app.route("/logged_out/")
def logged_out():
    return render_template("logged_out.html")


# TODO: combine into the regular index page.
@app.route("/icons/")
def show_icons():
    return render_template("icons.html")


@app.route("/blogcards")
def show_cards():

    return render_template("blogcards.html")


# Navbar is part of the base html/css elements.
@app.route("/navbar/")
def navbar():
    return render_template("base/navbar.html")


@app.route("/navbar2/")
def navbar2():
    return render_template("base/navbar2.html")


@app.route('/delete_post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    images = ImageRef.query.filter_by(blogpost_id=post_id)
    if not post:
        flash("Post not found")
        return redirect(url_for('admin'))

    try:
        for image in images:
            db.session.delete(image)
        db.session.delete(post)
        db.session.commit()
        flash('The post was successfully deleted')
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash(f"An error occurred: {str(e)}")
    return redirect(url_for('admin'))  # Always return a response


if __name__ == "__main__":
    if flask_environment  == 'production':
        app.run(host='0.0.0.0', port=8000)

    elif flask_environment == 'development':
        app.run(debug=True)
