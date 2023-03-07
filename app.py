from flask import Flask, render_template, redirect, request, session, url_for, flash
from german.german import german_app
from forms import ContactForm
from datetime import datetime
import secrets
from models import messages, BlogPost
from extensions import db
from functools import wraps



app = Flask(__name__)
app.register_blueprint(german_app, url_prefix="/german")

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_COOKIE_DOMAIN'] = '.matthewmoonen.com'
app.config['SESSION_COOKIE_PATH'] = '/'




db.init_app(app)

with app.app_context():
    """Create DB for contact form if not already exists"""
    db.create_all()


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


@app.route("/blog")
@login_required
def blog():
    posts = db.session.query(BlogPost).all()
    return render_template("blog.html", posts=posts)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'invalid credentials; please try again'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('blog'))
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run(debug=True)

