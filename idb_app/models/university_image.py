from flask import url_for
from mongoengine import Document, DENY
from mongoengine.fields import ReferenceField, ImageField, IntField

from idb_app.models import University

# TODO this really should be represented with a field on the University Model
# can migrate into the Uni collection later


class UniversityImage(Document):
    university = ReferenceField(
        University, reverse_delete_rule=DENY, required=True, unique=True
    )
    image = ImageField(required=True)
    # the image was from the {result_number}th image for a particular query
    # tracking this allows us to get better images if needed
    # assumes image queries are relatively stable over time
    result_number = IntField(default=0, required=True)

    @classmethod
    def get_default_img_url(cls):
        return url_for("static", filename="generic_college.jpg")

    @classmethod
    def get_model_field_name(cls):
        return "university"
