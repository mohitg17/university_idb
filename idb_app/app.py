from flask import Flask, render_template, url_for

app = Flask(__name__)

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
universities = {
    
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/majors")
def majors_base():
    model = {
        'title': 'Fields of Study & Majors',
        'instances': []
    }

    # Mapping majors to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for major in majors:
        instance = {
            'page_url': url_for('major', major_name=major),
                'image_url': url_for('static', filename=(major + '.jpg')),
                'name': major,
        }
        model['instances'].append(instance)

    return render_template("model.html", model=model)

@app.route("/cities")
def cities_base():
    model = {
        'title': 'Cities',
        'instances': []
    }

    # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for city in cities:
        instance = {
            'page_url': url_for('city', city_name=city),
                'image_url': url_for('static', filename=(city + '.jpg')),
                'name': city,
        }
        model['instances'].append(instance)

    return render_template("model.html", model=model)

    @app.route("/universities")
def universities_base():
    model = {
        'title': 'Universities',
        'instances': []
    }

    # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for university in universities:
        instance = {
            'page_url': url_for('university', university_name=university),
                'image_url': url_for('static', filename=(university + '.jpg')),
                'name': university,
        }
        model['instances'].append(instance)

    return render_template("model.html", model=model)

# TODO migrate to mongoengine after phase i


@app.route("/major/<string:major_name>")
def major(major_name):
    major_normalized = major_name.lower()
    if major_normalized not in majors:
        return f"Could not fine major {major_name}"
    else:
        return render_template("major_instance.html", major_name=major_name.replace("_", " ").title())

# TODO change this to add city instance routes
@app.route("/city/<string:city_name>")
def city(city_name):
    city_normalized = city_name.lower()
    if city_normalized not in cities:
        return f"Could not find city {city_name}"
    else:
        return render_template("major_instance.html", major_name=major_name.replace("_", " ").title())

# TODO change this to add university instance routes
@app.route("/university/<string:university_name>")
def university(university_name):
    university_normalized = university_name.lower()
    if university_normalized not in universities:
        return f"Could not find university {university_name}"
    else:
        return render_template("major_instance.html", major_name=major_name.replace("_", " ").title())

if __name__ == "__main__":
    app.run(debug=True, host="localhost")
