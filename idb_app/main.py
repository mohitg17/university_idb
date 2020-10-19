from flask import Flask, render_template, url_for
from idb_app.mongo import Connector

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

    # Mapping majors to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for major in majors:
        instance = {
            "page_url": url_for("major", major_name=major),
            "image_url": url_for("static", filename=(major + ".jpg")),
            "name": major.replace("_", " ").title(),
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
major_stats = {
    "education": {
        "median_starting_salary": 34900,
        "median_midcareer_salary": 52000,
        # for now just < 1 year certificate
        "num_certificate_programs": 376,
        "num_associate_programs": 696,
        "num_bachelor_programs": 1169,
        "schools": [
            "The University of Texas at Austin",
            "Harvard University",
            "Rice University",
        ],
    },
    "history": {
        "median_starting_salary": 39200,
        "median_midcareer_salary": 71000,
        # for now just < 1 year certificate
        "num_certificate_programs": 21,
        "num_associate_programs": 185,
        "num_bachelor_programs": 1233,
        "schools": [
            "The University of Texas at Austin",
            "Harvard University",
            "Rice University",
        ],
    },
    "engineering": {
        # salary is a non-weighted mean of the different engineering major salaries
        # TODO average more intelligently
        "median_starting_salary": 58957,
        "median_midcareer_salary": 99257,
        # for now just < 1 year certificate
        "num_certificate_programs": 95,
        "num_associate_programs": 464,
        "num_bachelor_programs": 619,
        "schools": [
            "The University of Texas at Austin",
            "Harvard University",
            "Rice University",
        ],
    },
}

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
    "the_university_of_texas_at_austin": {
        "student_population": 40329,
        "acceptance_rate": 38.52,
        "in_state_tuition": 10610,
        "out_of_state_tuition": 37580,
        "city": "austin",
        "location": "Austin, TX",
        "website": "http://utexas.edu",
        "sat_median": 1367,
        "act_median": 30,
        "percent_black": 4.23,
        "percent_white": 39.97,
        "percent_asian": 22.11,
        "percent_hispanic": 23.54,
        "percent_male": 46.15,
        "percent_female": 53.85,
        "median_debt": 11514,
        "avg_cost": 16505,
        "predominant_degree": "Bachelor's",
        "highest_degree": "Doctorate",
        "completion_overall": 5938,
        "completion_rate_black": 74.06,
        "completion_rate_asian": 87.93,
        "completion_rate_hispanic": 73.91,
        "completion_rate_white": 86.12,
        "earnings": 58200,
        "retention_rate": 94.95
    },
    "harvard_university": {
        "student_population": 7582,
        "acceptance_rate": 4.73,
        "in_state_tuition": 50420,
        "out_of_state_tuition": 50420,
        "city": "cambridge",
        "location": "Cambridge, MA",
        "website": "http://harvard.edu",
        "sat_median": 1520,
        "act_median": 34,
        "percent_black": 8.03,
        "percent_white": 40.54,
        "percent_asian": 19.22,
        "percent_hispanic": 11.33,
        "percent_male": 51.13,
        "percent_female": 48.87,
        "median_debt": 591,
        "avg_cost": 15561,
        "predominant_degree": "Bachelor's",
        "highest_degree": "Doctorate",
        "completion_overall": 492,
        "completion_rate_black": 99.04,
        "completion_rate_asian": 97.73,
        "completion_rate_hispanic": 98.68,
        "completion_rate_white": 97.60,
        "earnings": 58200,
        "retention_rate": 99.11
    },
    "rice_university": {
        "student_population": 3962,
        "acceptance_rate": 11.13,
        "in_state_tuition": 47350,
        "out_of_state_tuition": 47350,
        "city": "houston",
        "location": "Houston, TX",
        "website": "http://rice.edu",
        "sat_median": 1513,
        "act_median": 34,
        "percent_black": 7.14,
        "percent_white": 33.24,
        "percent_asian": 25.69,
        "percent_hispanic": 15.52,
        "percent_male": 52.30,
        "percent_female": 47.70,
        "median_debt": 537,
        "avg_cost": 20879,
        "predominant_degree": "Bachelor's",
        "highest_degree": "Doctorate",
        "completion_overall": 390,
        "completion_rate_black": 85.94,
        "completion_rate_asian": 98.08,
        "completion_rate_hispanic": 92.31,
        "completion_rate_white": 94.99,
        "earnings": 65400,
        "retention_rate": 97.41
    }
}


@app.route("/major/<string:major_name>")
def major(major_name):
    major_normalized = major_name.lower()
    if major_normalized not in majors:
        return f"Could not find major {major_name}"
    else:
        # TODO figure out a less hacky way to do this
        def format_dollar_amt(amt: int) -> str:
            return f"${amt:,}"

        return render_template(
            "major_instance.html",
            major_name=major_name.replace("_", " ").title(),
            major_stats=major_stats,
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
