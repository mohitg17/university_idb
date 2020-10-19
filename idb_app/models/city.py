from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField

from idb_app.models import choices


class City(Document):
    name = StringField(required=True)
    state = StringField(required=True, choices=choices.STATE_CHOICES, unique_with='name')
    area = FloatField(required=True, min_value=0.0)
    population = IntField(required=True, min_value=0)
    population_density = IntField(required=True, min_value=0)
    community_type = StringField(required=True, choices=choices.COMMUNITY_TYPE_CHOICES)
    median_age = IntField(required=True, min_value=0)
    median_gross_rent = IntField(required=True, min_value=0)

    def __str__(self) -> str:
        return f"{self.name.replace('_', ' ').title()}, {self.state}"
