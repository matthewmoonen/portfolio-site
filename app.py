from flask import Flask, render_template, redirect, request, session, url_for
from german_json import lesson_json
from forms import ContactForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets



app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)




class messages(db.Model):
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


@app.route("/german")
def german():
    return render_template("german.html")

@app.route("/lesson")
def get_lesson():
    return lesson_json()

@app.route("/icons")
def show_icons():
    return render_template("icons.html")

@app.route("/index2")
def index_2():
    return render_template("index2.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run(debug=True)