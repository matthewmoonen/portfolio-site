from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1 style='color: red'>[ > ]</h1><h3>Hello YouTube</h3>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')