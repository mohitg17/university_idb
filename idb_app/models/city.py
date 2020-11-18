from typing import List
from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField

from idb_app.models import choices, TextInput, RadioButtonSet


class City(Document):
    name = StringField(required=True)
    state = StringField(
        required=True, choices=choices.STATE_CHOICES, unique_with="name"
    )
    area = FloatField(required=True, min_value=0.0)
    population = IntField(required=True, min_value=0)
    population_ranking = IntField(min_value=0)
    population_density = IntField(required=True, min_value=0)
    community_type = StringField(required=True, choices=choices.COMMUNITY_TYPE_CHOICES)
    median_age = IntField(required=True, min_value=0)
    median_gross_rent = IntField(required=True, min_value=0)
    num_schools = IntField(default=0, min_value=0)
    latitude = FloatField()
    longitude = FloatField()

    def __str__(self) -> str:
        return f"{self.name.replace('_', ' ').title()}, {self.state}"

    @classmethod
    def get_filtering_buttons(cls) -> List[RadioButtonSet]:
        size_button_set = RadioButtonSet(title="Community Type",
                                         set_name="filter__community_type",
                                         values=choices.COMMUNITY_TYPE_CHOICES,
                                         labels=choices.COMMUNITY_TYPE_CHOICES)
        return [size_button_set]

    @classmethod
    def get_filtering_text(cls) -> List[TextInput]:
        return [TextInput(html_id="state_filter_input", name="filter__state__iexact", placeholder="State")]

    @classmethod
    def get_sort_buttons(cls) -> RadioButtonSet:
        return RadioButtonSet(title="Sort By",
                              set_name="order_by",
                              values=["median_gross_rent",
                                      "median_age",
                                      "population"],
                              labels=["Median Gross Rent", "Median Age", "Population"])

    @classmethod
    def get_name_field(cls) -> str:
        return "name"
