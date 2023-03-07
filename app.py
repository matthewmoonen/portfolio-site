from flask import Flask, render_template, redirect, request, session, url_for, flash
from german.german import german_app
from forms import ContactForm, BlogSubmitForm
from datetime import datetime
import secrets
from models import messages, BlogPost
from extensions import db
from functools import wraps
from flask_session import Session
import redis
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.register_blueprint(german_app, url_prefix="/german")

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

# Set Redis connection details
redis_host = "localhost"
redis_port = 6379

# TODO: Update this 
redis_password = "banana"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_DOMAIN'] = '.matthewmoonen.com'
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_TYPE'] = 'redis'
app.config["SESSION_REDIS"] = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
Session(app)
db.init_app(app)

with app.app_context():
    """Create DB for contact form if not already exists"""
    db.create_all()

with open('secret-files/admin_password_hash.txt', 'r') as file:
    ADMIN_PASSWORD_HASH = file.read().strip()

@app.route("/")
def index():
    return render_template("index.html")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to log in first!")
            return redirect(url_for("login"))
    return wrap

@app.route("/admin")
@login_required
def admin():
    session["mykey"] = "myvalue"
    posts = db.session.query(BlogPost).all()
    return render_template("admin.html", posts=posts)

# route for rendering the form
@app.route('/add_entry', methods=['GET'])
@login_required
def render_add_entry():
    return render_template('add_entry.html')

# route for handling the form submission
@app.route('/add_entry', methods=['POST'])
@login_required
def add_entry():
    form = BlogSubmitForm()
    if form.is_submitted():
        title = request.form['title']
        body = request.form['body']
        date_created = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")


    # blogdata = BlogPost(id=id, title=title, body=body, date_created=date_created)
    blogdata = BlogPost(title=title, body=body, date_created=date_created)


    try:
        db.session.add(blogdata)
        db.session.commit()
    except:
        return "an error occurred"
    else:
        flash('New entry was successfully added')
        return redirect(url_for('admin'))

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('admin'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or not check_password_hash(ADMIN_PASSWORD_HASH, request.form['password']):
            error = 'invalid credentials; please try again'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('admin'))
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    session["mykey"] = "myvalue"
    session.pop("logged_in", None)
    flash("You were just logged out!")
    return redirect(url_for('welcome'))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
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
    return render_template("contact.html")

@app.route("/icons")
def show_icons():
    return render_template("icons.html")

@app.route("/navbar")
def navbar():
    return render_template("base/navbar1.html")

@app.route("/code")
def code():
    return render_template("code.html")

@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    # return f"<h1>{post_id}</h1>"

    post = BlogPost.query.filter_by(id=post_id).first_or_404()
    try:
        db.session.delete(post)
        db.session.commit()
        flash('The post was successfully deleted')
    except:
        flash("an error occurred")
    else:
        return redirect(url_for('admin'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run(debug=True)