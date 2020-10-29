from mongoengine import Document, DENY
from mongoengine.fields import ReferenceField, ImageField, IntField

from idb_app.models import City

# TODO this should be represented with a field on the City Model
# can migrate into the City collection later


class CityImage(Document):
    city = ReferenceField(City, reverse_delete_rule=DENY, required=True, unique=True)
    image = ImageField(required=True)