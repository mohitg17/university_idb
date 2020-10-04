from mongoengine import Document
from mongoengine.fields import StringField

from idb_app.models import choices


class City(Document):
    name = StringField(required=True)
    state = StringField(required=True, choices=choices.STATE_CHOICES)
