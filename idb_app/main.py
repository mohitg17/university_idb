import urllib.parse
import json
from flask import Flask, render_template, url_for, make_response, redirect, request
from flask_paginate import Pagination, get_page_args

from idb_app.mongo import Connector
from idb_app.models import (
    Major,
    City,
    University,
    UniversityImage,
    CityImage,
    MajorImage,
)


app = Flask(__name__)

# if connecting to remote DB, need a .env file to load password from
Connector.load_database_creds()

# switch to Connector.connect_prod_database() when done testing
Connector.connect_prod_database()


@app.route("/")
def index():
    # Connector.reconnect_prod_database()
    return render_template("index.html")


@app.route("/about")
def about():
    # Connector.reconnect_prod_database()
    return render_template("about.html")


@app.route("/majors")
def majors_base():
    # Connector.reconnect_prod_database()
    order = request.args.get('order')
    if order is None:
        order = "+"
    order_by = f"{order}{request.args.get('order_by')}"
    if len(order_by) == 1:
        order_by = ""
    filter_params = get_filter_parameters(request.args, Major)
    majors = Major.objects(cip_code__ne=None, **filter_params).order_by(order_by).only(
        "name",
        "earnings_weighted_sum",
        "earnings_count",
        "num_bachelor_programs",
        "cip_code",
        "program_count_estimate",
    )
    model = create_major_model(majors)
    return render_model(model)


@app.route("/cities")
def cities_base():
    # Connector.reconnect_prod_database()
    order = request.args.get('order')
    if order is None:
        order = "+"
    order_by = f"{order}{request.args.get('order_by')}"
    if len(order_by) == 1:
        order_by = ""
    filter_params = get_filter_parameters(request.args, City)
    cities = City.objects(**filter_params).order_by(order_by).only(
        "name", "state", "population", "community_type", "area"
    )
    model = create_city_model(cities)
    # TODO image_url is currently linked to the wrong images
    return render_model(model)


@app.route("/universities")
def universities_base():
    # Connector.reconnect_prod_database()
    order = request.args.get('order')
    if order is None:
        order = "+"
    order_by = f"{order}{request.args.get('order_by')}"
    if len(order_by) == 1:
        order_by = ""
    filter_params = get_filter_parameters(request.args, University)
    universities = University.objects(**filter_params).order_by(order_by).only(
        "school_name",
        "school_state",
        "latest_student_size",
        "latest_cost_attendance_academic_year",
        "id",
    )
    model = create_university_model(universities)
    # TODO image_url is currently linked to the wrong images
    return render_model(model)


@app.route("/major/<string:major_name>")
def major(major_name):
    # Connector.reconnect_prod_database()
    decoded_name = urllib.parse.unquote_plus(major_name)
    major_loaded = Major.objects(name=decoded_name, cip_code__ne=None).first()
    related_majors = Major.objects(cip_family=major_loaded.cip_family).limit(10)
    if major_loaded is None:
        return f"Could not find major {decoded_name}"
    else:
        # TODO figure out a less hacky way to do this
        def format_dollar_amt(amt: float) -> str:
            return f"${int(amt):,}"

        schools = University.objects(majors_cip__ne=None, majors_cip=major_loaded.id)
        cities = [school.school_city for school in schools[:3]]
        page, _, _ = get_page_args(page_parameter="page", per_page_parameter="per_page")
        per_page = 6
        offset = (page - 1) * per_page
        total = len(schools)
        schools = schools[offset : offset + per_page]
        pagination = Pagination(
            page=page, per_page=per_page, total=total, css_framework="bootstrap4"
        )

        return render_template(
            "major_instance.html",
            major_name=decoded_name.replace(".", ""),
            major=major_loaded,
            related_majors=related_majors,
            # TODO - would need to load this model from University data
            schools=schools,
            cities=cities,
            num_schools=total,
            format_dollar_amt=format_dollar_amt,
            page=page,
            pagination=pagination,
        )


@app.route("/city/<string:city_state>")
def city(city_state):
    # Connector.reconnect_prod_database()
    city_loaded = City.objects(
        name=city_state.split(",")[0], state=city_state.split(",")[1].lstrip(" ")
    ).first()
    if city_loaded is None:
        return f"Could not find city {city_state}"
    else:
        page, _, _ = get_page_args(page_parameter="page", per_page_parameter="per_page")
        per_page = 6
        offset = (page - 1) * per_page
        schools = University.objects(school_city=city_loaded)[
            offset : offset + per_page
        ]
        suggested_majors = schools.first().majors_cip[:3] if (len(schools.first().majors_cip) > 3) else schools.first().majors_cip
        pagination = Pagination(
            page=page,
            per_page=per_page,
            total=len(University.objects(school_city=city_loaded)),
            css_framework="bootstrap4",
        )
        return render_template(
            "city_instance.html",
            city_name=str(city_loaded),
            city=city_loaded,
            schools=schools,
            suggested_majors=suggested_majors,
            page=page,
            pagination=pagination,
        )


@app.route("/university/<string:university_name>")
def university(university_name):
    # Connector.reconnect_prod_database()
    # TODO may need more than just name to differentiate universities
    uni_loaded = University.objects(school_name=university_name).first()
    if uni_loaded is None:
        return f"Could not find university {university_name.replace('_', ' ').title()}"
    else:
        for property in uni_loaded:
            if uni_loaded[property] == 0:
                uni_loaded[property] = "NA"
            if isinstance(uni_loaded[property], float):
                uni_loaded[property] = round(float(uni_loaded[property] * 100), 4)
        uni_loaded.majors_cip = [
            list(set(uni_loaded.majors_cip))[i : i + 2]
            for i in range(0, len(list(set(uni_loaded.majors_cip))), 2)
        ]
        return render_template(
            "university_instance.html",
            university_name=university_name.replace("_", " ").title(),
            university=uni_loaded,
            city_name=str(uni_loaded.school_city),
            encode=urllib.parse.quote_plus,
        )


@app.route("/images/university/<string:university_id>")
def get_uni_image(university_id: str):
    # Connector.reconnect_prod_database()
    uni_image = UniversityImage.objects(university=university_id).first()
    if uni_image is None:
        return redirect(url_for("static", filename="generic_college.jpg"))
    image_binary = uni_image.image.read()
    response = make_response(image_binary)
    response.headers.set("Content-Type", "image/jpeg")
    response.headers.set(
        "Content-Disposition", "attachment", filename=f"{university_id}.jpg"
    )
    return response


@app.route("/images/city/<string:city_id>")
def get_city_image(city_id: str):
    # Connector.reconnect_prod_database()
    city_image = CityImage.objects(city=city_id).first()
    if city_image is None:
        return redirect(url_for("static", filename="generic_city.jpg"))
    image_binary = city_image.image.read()
    response = make_response(image_binary)
    response.headers.set("Content-Type", "image/png")
    response.headers.set("Content-Disposition", "attachment", filename=f"{city_id}.png")
    return response


@app.route("/images/major/<string:major_id>")
def get_major_image(major_id: str):
    # Connector.reconnect_prod_database()
    major_image = MajorImage.objects(major=major_id).first()
    if major_image is None:
        return redirect(url_for("static", filename="generic_city.jpg"))
    image_binary = major_image.image.read()
    response = make_response(image_binary)
    response.headers.set("Content-Type", "image/png")
    response.headers.set(
        "Content-Disposition", "attachment", filename=f"{major_id}.png"
    )
    return response


# Use this instead of individual suggestions
@app.route("/suggestions<string:model>")
def suggestions(model: str):
    numResults = 5  # The number of suggestion results we want
    # Text is stored in jsdata of the request
    text = request.args.get("jsdata")

    # Depending on the model, we will look through different objects
    objects = []
    if model is "university":
        # Search Uni
        objects = (
            University.objects(school_name__icontains=text)
            .only("school_name")
            .limit(numResults)
        )
    elif model is "city":
        # Search city
        objects = City.objects(name__icontains=text).only("name").limit(numResults)
    elif model is "major":
        # Search major
        objects = Major.objects(name__icontains=text).only("name").limit(numResults)

    # Collect names of search results because the objects haven't been playing nicely with the template for some reason
    names = []
    for o in objects:
        if model is "university":
            names.append(o.school_name)
        else:
            names.append(o.name)
    # Render the suggestions in the template
    return render_template("search_results.html", text=names)


# Does a search every time a key is pressed in the search bar and returns the search_results template rendered with the results of the search
@app.route("/suggestions/university")
def suggestions_university():
    text = request.args.get("jsdata")
    objects = University.objects(school_name__icontains=text).only("school_name")
    names = []
    for obj in objects:
        names.append(obj.school_name)
    return render_template("search_results.html", text=names)


# Returns a render of the model that is passed to it by handling the creation of pagination and calling render_template
def render_model(model):
    page, _, _ = get_page_args(page_parameter="page", per_page_parameter="per_page")
    per_page = 18
    offset = (page - 1) * per_page
    total = len(model["instances"])
    if total is not 0:
        model["instances"] = model["instances"][offset : offset + per_page]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )
    return render_template(
        "model.html", model=model, page=page, per_page=per_page, pagination=pagination
    )


# TODO write this as an interface so that it can be called and will check the type of an object before calling the correct helper function
def create_model(objects):
    return objects


def get_filter_parameters(raw_params, model):
    params = {}
    for k,v in raw_params.items():
        if "filter__" in k and v:
            params[k.replace("filter__","")] = v.strip()
        elif k == "searchin" and v:
            params[f"{model.get_name_field()}__icontains"] = v.strip()
    return params


# Returns a university model where the instances are the universities that are passed as an argument
def create_university_model(universities):
    model = {"title": "Universities",
             "type": "university",
             "instances": [],
             "filter_buttons": University.get_filtering_buttons(),
             "filter_text": University.get_filtering_text(),
             "sort_buttons": University.get_sort_buttons(),
             }

    # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    # TODO image_url is currently linked to the wrong images
    for university in universities:
        instance = {
            "model_type": "university",
            "page_url": url_for("university", university_name=university.school_name),
            "image_url": url_for(
                "static", filename=(university.school_name.replace("_", " ") + ".jpg")
            ),
            "name": university.school_name.replace("_", " ").title(),
            "id": university.id,
            "attribute_1": {"name": "State", "value": university.school_state},
            "attribute_2": {
                "name": "Student Population",
                "value": university.latest_student_size,
            },
            "attribute_3": {
                "name": "Cost of Attendance",
                "value": 
                university.latest_cost_attendance_academic_year if university.latest_cost_attendance_academic_year 
                else "Unavailable",
            },
        }
        model["instances"].append(instance)

    return model


# Returns a city model where the instances are the cities that are passed as an argument
def create_city_model(cities):
    model = {"title": "Cities", "type": "city", "instances": [],
             "filter_buttons": City.get_filtering_buttons(),
             "filter_text": City.get_filtering_text(),
             "sort_buttons": City.get_sort_buttons(),}
    # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    # TODO image_url is currently linked to the wrong images
    for city in cities:
        instance = {
            "model_type": "city",
            "page_url": url_for("city", city_state=city),
            "image_url": url_for(
                "static", filename=(city.name + "_" + city.state + ".png")
            ),
            "name": str(city),
            "id": city.id,
            "attribute_1": {"name": "Population", "value": city.population},
            "attribute_2": {"name": "Community Type", "value": city.community_type},
            "attribute_3": {
                "name": "Area (square miles)",
                "value": city.area,
            },
        }
        model["instances"].append(instance)

    return model


# Returns a major model where the instances are the majors that are passed as an argument
def create_major_model(majors):
    model = {"title": "Fields of Study & Majors",
             "type": "major",
             "instances": [],
             "filter_buttons": Major.get_filtering_buttons(),
             "filter_text": Major.get_filtering_text(),
             "sort_buttons": Major.get_sort_buttons(),
             }

    # Mapping majors to an object that is passed to the template. Assumes naming scheme for page_url and image_url
    for major in majors:
        instance = {
            "model_type": "major",
            "page_url": url_for(
                "major", major_name=urllib.parse.quote_plus(major.name)
            ),
            "image_url": url_for("static", filename=(major.name + ".jpg")),
            "name": major.name.replace("_", " ").title(),
            "id": major.id,
            "attribute_1": {
                "name": "Average Starting Salary",
                "value": f"${int(major.average_earnings()):,}",
            },
            "attribute_2": {
                "name": "Average Mid-Career Salary",
                "value": f"${int(major.average_mid_earnings()):,}",
            },
            "attribute_3": {
                "name": "Number of Bachelor's Programs",
                "value": f"~{major.program_count_estimate:,}",
            },
        }
        model["instances"].append(instance)

    return model


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
