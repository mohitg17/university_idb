from flask import Flask, render_template, url_for
from idb_app.mongo import Connector
from idb_app.models import Major

app = Flask(__name__)

# if connecting to remote DB, need a .env file to load password from
Connector.load_database_creds()

# switch to Connector.connect_prod_database() when done testing
Connector.connect_prod_database()

majors = {
    "engineering",
    "history",
    "education",
}

cities = {
    "austin",
    "cambridge",
    "houston",
}

# TODO currently, the template relies on the naming scheme of these variables so @Harrison will add some formatting in this file to make that more robust to different names
# Sorry I changed up the cities and universities. It was because of a naming problem.
# After phase i, we can just pull the list of model instance names from MongoDB -Silas
universities = {
    "The University Of Texas At Austin",
    "Harvard University",
    "Rice University",
}


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

    return render_template("model.html", model=model)


@app.route("/cities")
def cities_base():
    model = {"title": "Cities", "instances": []}

    # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for city in cities:
        instance = {
            "page_url": url_for("city", city_name=city),
            "image_url": url_for("static", filename=(city + ".jpg")),
            "name": city.title(),
        }
        model["instances"].append(instance)

    return render_template("model.html", model=model)


@app.route("/universities")
def universities_base():
    model = {"title": "Universities", "instances": []}

    # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    # TODO need to replace spaces with underscores in URL
    for university in universities:
        instance = {
            "page_url": url_for(
                "university", university_name=university.lower().replace(" ", "_")
            ),
            "image_url": url_for("static", filename=(university.lower() + ".jpg")),
            "name": university,
        }
        model["instances"].append(instance)

    return render_template("model.html", model=model)


# TODO migrate to mongoengine after phase i

city_stats = {
    "austin": {
        "area": 579.4,
        "population": 950715,
        "population density": 3780,
        "community type": "Urban",
        "median age": 33.4,
        "median gross rent": 1244,
        "schools": ["The University of Texas at Austin"],
    },
    "houston": {
        "area": 251.5,
        "population": 2312717,
        "population density": 3991,
        "community type": "Urban",
        "median age": 33.1,
        "median gross rent": 986,
        "schools": ["Rice University"],
    },
    "cambridge": {
        "area": 6.43,
        "population": 113630,
        "population density": 17.675,
        "community type": "Urban",
        "median age": 30.5,
        "median gross rent": 2102,
        "schools": ["Harvard University"],
    },
}

university_stats = {

}


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
    city_normalized = city_name.lower()
    if city_normalized not in cities:
        return f"Could not find city {city_name}"
    else:
        return render_template(
            "city_instance.html",
            city_name=city_name.replace("_", " ").title(),
            city_stats=city_stats,
        )


@app.route("/university/<string:university_name>")
def university(university_name):
    if university_name.replace("_", " ").title() not in universities:
        return f"Could not find university {university_name.replace('_', ' ').title()}"
    else:
        return render_template(
            "university_instance.html",
            university_name=university_name.replace("_", " ").title(),
            university_stats=university_stats[university_name],
        )


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
