from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/majors")
def majors_base():
    return render_template("majors.html")


# TODO migrate to mongoengine after phase i
majors = {
    "engineering",
    "history",
    "education",
}


@app.route("/major/<string:major_name>")
def major(major_name):
    major_normalized = major_name.lower()
    if major_normalized not in majors:
        return f"Could not fine major {major_name}"
    else:
        return "yolo"


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
