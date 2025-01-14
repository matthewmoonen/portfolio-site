from flask import Flask, render_template, redirect, request, session, url_for, flash, jsonify
from german.german import german_app
from forms import ContactForm, BlogSubmitForm
from datetime import datetime
import secrets
from models import messages, BlogPost, Tag, Image
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
import re
from markdown import markdown
import random
import string
from sqlalchemy.orm.exc import NoResultFound


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
    recent_posts = db.session.query(BlogPost).order_by(BlogPost._id.desc()).limit(4).all()
    for i, post in enumerate(recent_posts):
        post.number = i
        parsed_date = datetime.strptime(post.date_created, "%Y-%m-%d, %H:%M:%S")
        post.formatted_date = parsed_date.strftime("%B %d, %Y")
        post.image = post.image if hasattr(post, 'image') and post.image else "terminal.png"
        
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


# Admin panel primarily for creating blog posts
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
        messages._id,
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
        messages._id,
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


# Retrieve blog post via URL slug. Display 404 error if post not available.
@app.route('/blog/<slug>/')
def blog_post(slug):
    post = db.session.query(BlogPost).filter_by(slug=slug).first()
    if post:
        # Reformat date as MMMM dd, yy
        parsed_date = datetime.strptime(post.date_created, "%Y-%m-%d, %H:%M:%S")
        formatted_date = parsed_date.strftime("%B %d, %Y")
        return render_template("base/blog-template.html", post=post, slug=slug, formatted_date=formatted_date)
    else:
        return f"404"


@app.route("/mostrecent/")
def most_recent():
    recent_posts = db.session.query(BlogPost).order_by(BlogPost._id.desc()).limit(2).all()
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


@app.route('/add_entry/', methods=['GET'])
@login_required
def render_add_entry():
    return render_template('add_entry.html')



@app.route('/add_entry/', methods=['POST'])
@login_required
def add_entry():
    form = BlogSubmitForm()
    if form.is_submitted():
        title = request.form['title']
        body = request.form['body']
        blurb = request.form['blurb']
        slug = request.form['slug']
        if slug == "":
            slug = title_to_slug(title)
        slug = ensure_unique_slug(slug)
        tags_input = request.form['tags'] 
        date_created = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

        blogdata = BlogPost(title=title, body_markdown=body, body_html=markdown(body), slug=slug, blurb=blurb, date_created=date_created)

        if tags_input:
            tags = {tag.strip().upper() for tag in tags_input.split(',')}
            for tag_name in tags:
                # Check if the tag already exists
                existing_tag = Tag.query.filter_by(name=tag_name).first()
                if existing_tag:
                    blogdata.tags.append(existing_tag)
                else:
                    # Create a new tag and append it
                    new_tag = Tag(name=tag_name)
                    blogdata.tags.append(new_tag)

        try:
            db.session.add(blogdata)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"
        else:
            flash('New entry was successfully added')
            return redirect(url_for('admin'))



@app.route('/upload_images', methods=['POST'])
@login_required
def upload_images():
    if 'images' not in request.files:
        return jsonify({"success": False, "error": "No files uploaded"})

    uploaded_files = request.files.getlist('images')
    new_images = []

    for file in uploaded_files:
        if allowed_file(file.filename):
            new_image = Image(filename=file.filename, data=file.read())
            db.session.add(new_image)
            db.session.flush()  # Generate ID without committing
            new_images.append({"id": new_image.id, "filename": file.filename})
        else:
            return jsonify({"success": False, "error": "Invalid file type"})

    db.session.commit()
    return jsonify({"success": True, "new_images": new_images})


@app.route('/get_uploaded_images', methods=['GET'])
@login_required
def get_uploaded_images():
    images = [{"id": img.id, "filename": img.filename} for img in Image.query.all()]
    return jsonify({"success": True, "images": images})




@app.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"success": False, "error": "Image not found"})

    db.session.delete(image)
    db.session.commit()

    remaining_images = [{"id": img.id, "filename": img.filename} for img in Image.query.all()]
    return jsonify({"success": True, "images": remaining_images})


@app.route('/edit_entry/<int:_id>/', methods=['GET'])
@login_required
def render_edit_entry(_id):
    post = BlogPost.query.filter_by(_id=_id).first()
    if post is None:
        abort(404)

    form = BlogSubmitForm(obj=post)
    form.markdown_body.data = post.body_markdown
    form.slug.data = post.slug
    form.blurb.data = post.blurb
    
    return render_template('edit_entry.html', form=form, post=post, _id=_id)


@app.route('/edit_entry/<int:_id>', methods=['POST'])
@login_required
def edit_entry(_id):
    form = BlogSubmitForm()
    if form.is_submitted():
        title = request.form['title']
        body_markdown = request.form['body']
        blurb = request.form['blurb']
        slug = request.form['slug']
        if slug == "":
            slug = title_to_slug(title)
        
        tags_input = request.form['tags']

        blogpost = db.session.get(BlogPost, _id)
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


# Handle admin deleting post from the admin page
@app.route('/delete_post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):

    post = BlogPost.query.filter_by(_id=post_id).first()
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('The post was successfully deleted')
    except:
        flash("an error occurred")
    else:
        return redirect(url_for('admin'))


if __name__ == "__main__":
    if flask_environment  == 'production':
        app.run(host='0.0.0.0', port=8000)

    elif flask_environment == 'development':
        app.run(debug=True)
