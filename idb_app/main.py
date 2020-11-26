import urllib.parse
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


def get_model_from_string(s: str):
    s_normalized = s.lower()
    model_class = {
        "major": Major,
        "university": University,
        "city": City,
     }.get(s_normalized)
    if model_class is None:
        raise ValueError(f"{s} is not a known model class")
    return model_class


@app.template_filter('encode')
def encode(name):
    return url_for("major", major_name=urllib.parse.quote_plus(name))

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


@app.route("/base/<string:model_name>")
def base(model_name: str):
    model_class = get_model_from_string(model_name)
    order = request.args.get('order')
    if order is None:
        order = "+"
    order_by = f"{order}{request.args.get('order_by')}"
    if len(order_by) == 1:
        order_by = ""
    filter_params = get_filter_parameters(request.args, model_class)
    model_objects = model_class.base_queryset().filter(**filter_params).order_by(order_by).only(*model_class.get_base_attributes())
    model = model_class.create_models(model_objects)
    return render_model(model)


# TODO get rid of these and the other bases once we fix all links to this
@app.route("/majors")
def majors_base():
    return redirect("/base/major")


@app.route("/cities")
def cities_base():
    return redirect("/base/city")


@app.route("/universities")
def universities_base():
    return redirect("/base/university")


@app.route("/major/<string:major_name>")
def major(major_name):
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


@app.route("/images/<string:model_name>/<string:model_object_id>")
def get_model_image(model_name: str, model_object_id: str):
    img_class = get_model_from_string(model_name).get_image_class()
    img_instance = img_class.objects(**{img_class.get_model_field_name(): model_object_id}).first()
    if img_instance is None:
        return redirect(img_class.get_default_img_url())
    image_binary = img_instance.image.read()
    response = make_response(image_binary)
    response.headers.set("Content-Type", "image/jpeg")
    response.headers.set(
        "Content-Disposition", "attachment", filename=f"{model_object_id}.jpg"
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


def get_filter_parameters(raw_params, model):
    params = {}
    for k,v in raw_params.items():
        if "filter__" in k and v:
            params[k.replace("filter__","")] = v.strip()
        elif k == "searchin" and v:
            params[f"{model.get_name_field()}__icontains"] = v.strip()
    return params


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
