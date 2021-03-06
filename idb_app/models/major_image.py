from flask import url_for
from mongoengine import Document, DENY
from mongoengine.fields import ReferenceField, ImageField, IntField

from idb_app.models import Major

# TODO this should be represented with a field on the Major Model
# can migrate into the Major collection later


class MajorImage(Document):
    major = ReferenceField(Major, reverse_delete_rule=DENY, required=True, unique=True)
    image = ImageField(required=True)
    result_number = IntField(default=0, required=True)

    @classmethod
    def get_default_img_url(cls):
        return url_for("static", filename="education.jpg")

    @classmethod
    def get_model_field_name(cls):
        return "major"
