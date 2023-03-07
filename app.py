from flask import Flask, render_template, redirect, request, session, url_for
from german.german import german_app
from forms import ContactForm
from datetime import datetime
import secrets
# from models import messages
from extensions import db

app = Flask(__name__)
app.register_blueprint(german_app, url_prefix="/german")

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    """Create DB for contact form if not already exists"""
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/navbar")
def navbar():
    return render_template("base/navbar1.html")

@app.route("/code")
def code():
    return render_template("code.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run(debug=True)

from models import *