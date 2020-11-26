from typing import List
from flask import url_for
from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField

from idb_app.models import choices, AbstractModel
from idb_app.filtering.filtering_controls import TextInput, RadioButtonSet


class City(Document, AbstractModel):
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

    @classmethod
    def get_base_attributes(cls) -> List[str]:
        return ["name", "state", "population", "community_type", "area"]

    @classmethod
    def create_models(cls, query_set):
        model = {"title": "Cities", "type": "city", "instances": [],
                 "filter_buttons": cls.get_filtering_buttons(),
                 "filter_text": cls.get_filtering_text(),
                 "sort_buttons": cls.get_sort_buttons(), }
        # Mapping cities to an object that is passed to the template. Assumes naming scheme for page_url and image_url
        # TODO image_url is currently linked to the wrong images
        for city in query_set:
            instance = {
                "model_type": "city",
                "page_url": url_for("city", city_state=city),
                "image_url": url_for(
                    "static", filename=(city.name + "_" + city.state + ".png")
                ),
                "name": str(city),
                "id": city.id,
                "attribute_1": {"name": "Population",
                                "value": city.population if not city.population == 10000 else "Unavailable"},
                "attribute_2": {"name": "Community Type", "value": city.community_type},
                "attribute_3": {
                    "name": "Area (square miles)",
                    "value": city.area if not city.area == 1000000 else "Unavailable",
                },
            }
            model["instances"].append(instance)

        return model