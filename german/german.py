from flask import Blueprint, render_template 
from german.lesson_json import lesson_json

# TODO:
# https://stackoverflow.com/questions/66381380/static-files-are-not-loading-from-static-folder

german_app = Blueprint('german_app', __name__,
    template_folder='templates')

@german_app.route("/")
def german():
    return render_template("german.html")

@german_app.route("/lesson")
def get_lesson():
    return lesson_json()