from typing import List
from mongoengine import Document
from flask import render_template
from flask_paginate import Pagination, get_page_args
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
    def get_image_class(cls):
        from idb_app.models import CityImage

        return CityImage

    def get_template(self):
        from idb_app.models import University

        page, _, _ = get_page_args(page_parameter="page", per_page_parameter="per_page")
        per_page = 6
        offset = (page - 1) * per_page
        schools = University.objects(school_city=self)[
                  offset: offset + per_page
                  ]
        suggested_majors = set(schools.first().majors_cip[:3]) if (
                    len(set(schools.first().majors_cip)) > 3) else set(schools.first().majors_cip)
        pagination = Pagination(
            page=page,
            per_page=per_page,
            total=len(University.objects(school_city=self)),
            css_framework="bootstrap4",
        )
        return render_template(
            "city_instance.html",
            city_name=str(self),
            city=self,
            schools=schools,
            suggested_majors=suggested_majors,
            page=page,
            pagination=pagination,
        )