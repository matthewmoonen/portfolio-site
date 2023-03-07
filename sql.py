from app import db, app
from models import BlogPost

# Create db and db tables
with app.app_context():
    db.create_all()

# insert
db.session.add(BlogPost("Good", "I\'m v. good"))
db.session.add(BlogPost("Well", "I\'m v. well"))

# Commit changes to DB
db.session.commit()