from flask import Flask, render_template, url_for
from flask_paginate import Pagination, get_page_args
from idb_app.mongo import Connector
from idb_app.models import Major, City, University

app = Flask(__name__)

# if connecting to remote DB, need a .env file to load password from
Connector.load_database_creds()

# switch to Connector.connect_prod_database() when done testing
Connector.connect_prod_database()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/majors")
def majors_base():
    model = {"title": "Fields of Study & Majors", "instances": []}
    majors = Major.objects().only("name")

    # Mapping majors to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for major in majors:
        instance = {
            "page_url": url_for("major", major_name=major.name),
            "image_url": url_for("static", filename=(major.name + ".jpg")),
            "name": major.name.replace("_", " ").title(),
        }
        model["instances"].append(instance)

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(majors)
    model["instances"] = model["instances"][offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('model.html', model=model, page=page, per_page=per_page, pagination=pagination)


@app.route("/cities")
def cities_base():
    model = {"title": "Cities", "instances": []}
    cities = City.objects().only("name", "state")
    # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for city in cities:
        instance = {
            "page_url": url_for("city", city_name=city.name),
            "image_url": url_for("static", filename=(city.name + ".jpg")),
            "name": str(city),
        }
        model["instances"].append(instance)

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(cities)
    model["instances"] = model["instances"][offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('model.html', model=model, page=page, per_page=per_page, pagination=pagination)


@app.route("/universities")
def universities_base():
    model = {"title": "Universities", "instances": []}
    universities = University.objects().only("school_name")

    # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for university in universities:
        instance = {
            "page_url": url_for(
                "university", university_name=university.school_name
            ),
            "image_url": url_for("static", filename=(university.school_name.replace("_"," ") + ".jpg")),
            "name": university.school_name.replace("_", " ").title(),
        }
        model["instances"].append(instance)

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(universities)
    model["instances"] = model["instances"][offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('model.html', model=model, page=page, per_page=per_page, pagination=pagination)


@app.route("/major/<string:major_name>")
def major(major_name):
    major_loaded = Major.objects(name=major_name.lower()).first()
    if major_loaded is None:
        return f"Could not find major {major_name}"
    else:
        # TODO figure out a less hacky way to do this
        def format_dollar_amt(amt: int) -> str:
            return f"${amt:,}"

        return render_template(
            "major_instance.html",
            major_name=major_name.replace("_", " ").title(),
            major=major_loaded,
            # TODO - would need to load this model from University data
            schools=[],
            format_dollar_amt=format_dollar_amt,
        )


# TODO change this to add city instance routes
@app.route("/city/<string:city_name>")
def city(city_name):
    # TODO will need to refactor this to include state in the parameter
    city_loaded = City.objects(name=city_name.lower()).first()
    if city_loaded is None:
        return f"Could not find city {city_name}"
    else:
        return render_template(
            "city_instance.html",
            city_name=str(city_loaded),
            city=city_loaded,
            # TODO
            schools=[],
        )


@app.route("/university/<string:university_name>")
def university(university_name):
    # TODO may need more than just name to differentiate universities
    uni_loaded = University.objects(name=university_name).first()
    if uni_loaded is None:
        return f"Could not find university {university_name.replace('_', ' ').title()}"
    else:
        return render_template(
            "university_instance.html",
            university_name=university_name.replace("_", " ").title(),
            university=uni_loaded,
            city_name=str(uni_loaded.city),
        )


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
