from flask import Flask, render_template
from german_json import lesson_json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/german")
def german():
    return render_template("german.html")

@app.route("/lesson")
def get_lesson():
    return lesson_json()


if __name__ == "__main__":
    app.run(host='0.0.0.0')