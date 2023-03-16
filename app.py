from flask import Flask, render_template, redirect, request, session, url_for, flash, jsonify
from german.german import german_app
from forms import ContactForm, BlogSubmitForm
from datetime import datetime
import secrets
from models import messages, BlogPost
from extensions import db
from functools import wraps
from flask_session import Session
import redis
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import logging


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
load_dotenv("/home/matthew/portfolio-site/environmentvariables.env")


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
def index():
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
    
    recent_posts = db.session.query(BlogPost).order_by(BlogPost._id.desc()).limit(2).all()
    form = ContactForm()
    if form.is_submitted():
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        date_created = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

        # Get client IP address:
        if 'X-Forwarded-For' in request.headers:
            ip_address = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
        else:
            ip_address = request.remote_addr or 'untrackable'

        is_forwarded = 0
        formdata = messages(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message, date_created=date_created, ip_address=ip_address, is_forwarded=is_forwarded)

        try:
            db.session.add(formdata)
            db.session.commit()
        except:
            print('error 400')
            return render_template('oops.html')
        else:
            return render_template('thanks.html', first_name=first_name)
        

        
        for post in recent_posts:
            parsed_date = datetime.strptime(post.date_created, "%Y-%m-%d, %H:%M:%S")
            post.formatted_date = parsed_date.strftime("%B %d, %Y")



    return render_template("index.html", recent_posts=recent_posts)


# A decorator function that creates login requirement for certain views.
def login_required(f):
    # Wraps decorator preserves the original function's name and docstring
    @wraps(f)
    def wrap(*args, **kwargs):
        # Check whether user is logged in
        if "logged_in" in session:
            return f(*args, **kwargs)
        # Handle user not logged in trying to access page that requires login
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


# Handle upload
""" TODO: See here to improve security and performance
https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
"""
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    session["mykey"] = "myvalue"
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('admin', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


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


# route for rendering the post blog form
@app.route('/add_entry/', methods=['GET'])
@login_required
def render_add_entry():
    return render_template('add_entry.html')


# route for handling post blog form submission
@app.route('/add_entry/', methods=['POST'])
@login_required
def add_entry():
    form = BlogSubmitForm()
    if form.is_submitted():
        title = request.form['title']
        body = request.form['body']
        blurb = request.form['blurb']
        slug = request.form['slug']
        date_created = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    blogdata = BlogPost(title=title, body=body, slug=slug, blurb=blurb, date_created=date_created)

    try:
        db.session.add(blogdata)
        db.session.commit()
    except:
        return "an error occurred"
    else:
        flash('New entry was successfully added')
        return redirect(url_for('admin'))



"""TODO: create base.html for add post and edit post page/admin pages"""
# # route for rendering the post edit form
# @app.route('/edit_entry/<int:_id>/', methods=['GET'])
# @login_required
# def render_edit_entry(_id):
#     post = BlogPost.query.filter_by(_id=_id).first()
#     if post is None:
#         abort(404)
#     form = BlogSubmitForm(obj=post)
#     return render_template('edit_entry.html', form=form, _id=_id)


# Route for rendering post edit form
@app.route('/edit_entry/<int:_id>/', methods=['GET'])
@login_required
def render_edit_entry(_id):
    post = BlogPost.query.filter_by(_id=_id).first()
    if post is None:
        abort(404)
    form = BlogSubmitForm(obj=post)
    # Get the slug value from the database and pass it to the form
    slug = BlogPost.query.filter_by(_id=_id).first().slug
    form.slug.data = slug
    blurb = BlogPost.query.filter_by(_id=_id).first().blurb
    form.blurb.data = blurb
    return render_template('edit_entry.html', form=form, post=post, _id=_id)


# Route for submitting post edit form
@app.route('/edit_entry/<int:_id>', methods=['POST'])
@login_required
def edit_entry(_id):
    form = BlogSubmitForm()
    if form.is_submitted():
        title = request.form['title']
        body = request.form['body']
        blurb = request.form['blurb']
        slug = request.form['slug']
        # Query the blog post from the database
        blogpost = BlogPost.query.get(_id)
        if not blogpost:
            abort(404)
        # Update the blog post data
        blogpost.title = title
        blogpost.body = body
        blogpost.blurb = blurb
        blogpost.slug = slug
        try:
            db.session.commit()
        except:
            return "an error occurred"
        else:
            flash('Entry was successfully edited')
            return redirect(url_for('admin'))


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

    post = BlogPost.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash('The post was successfully deleted')
    except:
        flash("an error occurred")
    else:
        return redirect(url_for('admin'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    # app.run(debug=True)
