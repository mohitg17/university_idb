from flask import url_for
from mongoengine import Document, DENY
from mongoengine.fields import ReferenceField, ImageField

from idb_app.models import City

# TODO this should be represented with a field on the City Model
# can migrate into the City collection later


class CityImage(Document):
    city = ReferenceField(City, reverse_delete_rule=DENY, required=True, unique=True)
    image = ImageField(required=True)

    @classmethod
    def get_default_img_url(cls):
        return url_for("static", filename="generic_college.jpg")

    @classmethod
    def get_model_field_name(cls):
        return "city"
