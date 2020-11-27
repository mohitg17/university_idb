import urllib.parse
from typing import List
from mongoengine import Document
from flask import url_for, render_template
from mongoengine.fields import StringField, IntField
from flask_paginate import Pagination, get_page_args

from idb_app.models import choices, AbstractModel
from idb_app.filtering.filtering_controls import TextInput, RadioButtonSet


class Major(Document, AbstractModel):
    name = StringField(required=True, unique=True)
    description = StringField()
    # would be "science" or "social studies" or "engineering", etc. Exact choices we use depend on data set
    # major_type = StringField(required=True)
    median_starting_salary = IntField(min_value=0)
    median_midcareer_salary = IntField(min_value=0)
    num_certificate_programs = IntField(min_value=0)
    num_associate_programs = IntField(min_value=0)
    num_bachelor_programs = IntField(min_value=0)

    # TODO - apparently the leading two leading digits of the CIP indicate the major's category (like engineering, etc.)
    # category = StringField(choices=choices.MAJOR_CATEGORIES)

    # internal fields
    # TODO make unique once we remove the others
    cip_code = StringField()
    cip_family = IntField()
    earnings_weighted_sum = IntField(default=0)
    earnings_count = IntField(default=0)
    program_count_estimate = IntField(default=0)

    def average_earnings(self):
        if self.earnings_count == 0:
            return 0
        else:
            return self.earnings_weighted_sum / self.earnings_count

    # factor based on payscale data
    # TODO - more intelligent calculation
    def average_mid_earnings(self):
        return 1.693 * self.average_earnings()

    # assumes the callee will .save()
    @classmethod
    def get_or_create(cls, cip_code: int, title: str):
        created = cls.objects(cip_code=cip_code).first()
        if created is None:
            created = cls.objects(name=title).first()
        if created is None:
            created = cls(
                cip_code=cip_code, name=title, earnings_weighted_sum=0, earnings_count=0
            )
            # created.save()
        return created

    @classmethod
    def get_filtering_buttons(cls) -> List[RadioButtonSet]:
        cip_values = []
        cip_labels = []
        for k, v in choices.CIP_FAMILY_MAP.items():
            cip_labels.append(v)
            cip_values.append(k)
        cip_family_button_set = RadioButtonSet(title="Major Category",
                                               set_name="filter__cip_family",
                                               values=cip_values,
                                               labels=cip_labels)
        return [cip_family_button_set]

    @classmethod
    def get_filtering_text(cls) -> List[TextInput]:
        return []

    @classmethod
    def get_sort_buttons(cls) -> RadioButtonSet:
        return RadioButtonSet(title="Sort By",
                              set_name="order_by",
                              values=["median_starting_salary",
                                      "median_midcareer_salary",
                                      "num_bachelor_programs", ],
                              labels=["Starting Salary", "Mid-Career Salary", "Number of Bachelor's Programs"])

    @classmethod
    def get_name_field(cls) -> str:
        return "name"

    @classmethod
    def get_base_attributes(cls) -> List[str]:
        return ["name",
                "earnings_weighted_sum",
                "earnings_count",
                "num_bachelor_programs",
                "cip_code",
                "program_count_estimate"]

    @classmethod
    def base_queryset(cls):
        return cls.objects(cip_code__ne=None)

    @classmethod
    def create_models(cls, queryset):
        model = {"title": "Fields of Study & Majors",
                 "type": "major",
                 "instances": [],
                 "filter_buttons": cls.get_filtering_buttons(),
                 "filter_text": cls.get_filtering_text(),
                 "sort_buttons": cls.get_sort_buttons(),
                 }

        # Mapping majors to an object that is passed to the template. Assumes naming scheme for page_url and image_url
        for major in queryset:
            instance = {
                "model_type": "major",
                "page_url": url_for(
                    "instance", model_name="major", object_id=major.id
                ),
                "image_url": url_for("static", filename=(major.name + ".jpg")),
                "name": major.name.replace("_", " ").title(),
                "id": major.id,
                "attribute_1": {
                    "name": "Average Starting Salary",
                    "value": f"${int(major.average_earnings()):,}",
                },
                "attribute_2": {
                    "name": "Average Mid-Career Salary",
                    "value": f"${int(major.average_mid_earnings()):,}",
                },
                "attribute_3": {
                    "name": "Number of Bachelor's Programs",
                    "value": f"~{major.program_count_estimate:,}",
                },
            }
            model["instances"].append(instance)

        return model

    @classmethod
    def get_image_class(cls):
        from idb_app.models import MajorImage

        return MajorImage

    def get_template(self):
        from idb_app.models import University

        related_majors = Major.objects(cip_family=self.cip_family).limit(10)

        # TODO figure out a less hacky way to do this
        def format_dollar_amt(amt: float) -> str:
            return f"${int(amt):,}"

        schools = University.objects(majors_cip__ne=None, majors_cip=self.id)
        cities = [school.school_city for school in schools[:3]]
        page, _, _ = get_page_args(page_parameter="page", per_page_parameter="per_page")
        per_page = 6
        offset = (page - 1) * per_page
        total = len(schools)
        schools = schools[offset: offset + per_page]
        pagination = Pagination(
            page=page, per_page=per_page, total=total, css_framework="bootstrap4"
        )

        return render_template(
            "major_instance.html",
            major_name=self.name.replace(".", ""),
            major=self,
            related_majors=related_majors,
            # TODO - would need to load this model from University data
            schools=schools,
            cities=cities,
            num_schools=total,
            format_dollar_amt=format_dollar_amt,
            page=page,
            pagination=pagination,
        )

