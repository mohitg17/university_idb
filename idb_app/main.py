from flask import Flask, render_template, make_response, redirect
from flask_paginate import Pagination, get_page_args


from idb_app.mongo import Connector
from idb_app.bases import UniversityFactory, CityFactory, MajorFactory
from idb_app.models import (
    Major,
    City,
    University,
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

def get_factory_from_string(s: str):
    s_normalized = s.lower()
    factory = {
        "major": MajorFactory,
        "university": UniversityFactory,
        "city": CityFactory,
    }.get(s_normalized)
    if factory is None:
        raise ValueError(f"{s} is not a known model class")
    return factory


Connector.load_database_creds()

Connector.connect_prod_database()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/base/<string:model_name>")
def base(model_name: str):
    factory = get_factory_from_string(model_name)
    model_class = get_model_from_string(model_name)
    model = factory.build_base(model_class)
    return render_model(model)


@app.route("/instance/<string:model_name>/<string:object_id>")
def instance(model_name: str, object_id: str):
    return (
        get_model_from_string(model_name).objects(id=object_id).first().get_template()
    )


@app.route("/images/<string:model_name>/<string:model_object_id>")
def get_model_image(model_name: str, model_object_id: str):
    img_class = get_model_from_string(model_name).get_image_class()
    img_instance = img_class.objects(
        **{img_class.get_model_field_name(): model_object_id}
    ).first()
    if img_instance is None:
        return redirect(img_class.get_default_img_url())
    image_binary = img_instance.image.read()
    response = make_response(image_binary)
    response.headers.set("Content-Type", "image/jpeg")
    response.headers.set(
        "Content-Disposition", "attachment", filename=f"{model_object_id}.jpg"
    )
    return response


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


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
