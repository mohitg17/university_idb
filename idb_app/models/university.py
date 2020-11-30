import urllib.parse
from typing import List
from mongoengine import Document, DENY
from mongoengine.fields import (
    StringField,
    IntField,
    ReferenceField,
    ListField,
    FloatField,
)
from flask import render_template

from idb_app.models import City, Major, AbstractModel, choices
from idb_app.filtering.filtering_controls import TextInput, RadioButtonSet


class University(Document, AbstractModel):
    school_name = StringField(
        required=True, unique_with=["school_city", "school_state"]
    )
    school_city = ReferenceField(City, reverse_delete_rule=DENY, required=True)
    school_state = StringField(required=True, choices=choices.STATE_CHOICES)
    school_locale = StringField(default="City")
    majors_offered = ListField(
        ReferenceField(Major, reverse_delete_rule=DENY), default=[]
    )
    latest_student_size = IntField(default=0, min_value=0)
    latest_admissions_admission_rate_overall = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_cost_tuition_in_state = IntField(default=0, min_value=0)
    latest_cost_tuition_out_of_state = IntField(default=0, min_value=0)
    school_school_url = StringField(required=True)
    latest_admissions_sat_scores_average_overall = IntField(default=0)
    latest_admissions_act_scores_midpoint_cumulative = IntField(default=0)
    latest_student_demographics_race_ethnicity_black = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_student_demographics_race_ethnicity_white = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_student_demographics_race_ethnicity_asian = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_student_demographics_race_ethnicity_hispanic = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_student_demographics_men = FloatField(
        default=0, min_value=0.0, max_value=100.0
    )
    latest_student_demographics_women = FloatField(
        default=0, min_value=0.0, max_value=100.0
    )
    latest_aid_median_debt_completers_overall = IntField(default=0)
    latest_cost_attendance_academic_year = IntField(default=0)
    school_degrees_awarded_predominant = StringField(
        required=True, choices=choices.DEGREE_CHOICES
    )
    school_degrees_awarded_highest = StringField(
        required=True, choices=choices.DEGREE_CHOICES
    )
    latest_completion_4_yr_completion_overall = IntField(default=0, min_value=0)
    latest_completion_completion_rate_4yr_150_white = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_completion_completion_rate_4yr_150_black = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_completion_completion_rate_4yr_150_asian = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_completion_completion_rate_4yr_150_hispanic = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    latest_earnings_10_yrs_after_entry_median = IntField(default=0, min_value=0)
    latest_student_retention_rate_four_year_full_time = FloatField(
        default=0.0, min_value=0.0, max_value=100.0
    )
    size = StringField(choices=choices.UNI_SIZE_CHOICES)
    cost_category = StringField(choices=choices.COST_CATEGORY_CHOICES)

    def calculate_size(self):
        if self.latest_student_size < 5000:
            return choices.UNI_SIZE_SMALL
        elif self.latest_student_size < 15000:
            return choices.UNI_SIZE_MEDIUM
        else:
            return choices.UNI_SIZE_LARGE

    def calculate_cost_cat(self):
        if self.latest_cost_attendance_academic_year < 15000:
            return choices.COST_CATEGORY_LOW
        elif self.latest_cost_attendance_academic_year < 40000:
            return choices.COST_CATEGORY_MEDIUM
        else:
            return choices.COST_CATEGORY_HIGH

    # collegescorecard (by Dept of Ed) internal id -- helpful for re-querying their API
    # TODO make required once all the data is in
    doe_id = IntField()

    latitude = FloatField()
    longitude = FloatField()

    # TODO phase out other major list
    majors_cip = ListField(ReferenceField(Major, reverse_delete_rule=DENY), default=[])

    @classmethod
    def get_filtering_buttons(cls) -> List[RadioButtonSet]:
        size_button_set = RadioButtonSet(
            title="School Size",
            set_name="filter__size",
            values=choices.UNI_SIZE_CHOICES,
            labels=choices.UNI_SIZE_CHOICES,
        )
        cost_button_set = RadioButtonSet(
            title="Cost of Attendance",
            set_name="filter__cost_category",
            values=choices.COST_CATEGORY_CHOICES,
            labels=choices.COST_CATEGORY_CHOICES,
        )
        return [size_button_set, cost_button_set]

    @classmethod
    def get_filtering_text(cls) -> List[TextInput]:
        return [
            TextInput(
                html_id="state_filter_input",
                name="filter__school_state__iexact",
                placeholder="State",
            )
        ]

    @classmethod
    def get_sort_buttons(cls) -> RadioButtonSet:
        return RadioButtonSet(
            title="Sort By",
            set_name="order_by",
            values=[
                "school_name",
                "latest_admissions_admission_rate_overall",
                "latest_student_size",
                "latest_cost_attendance_academic_year",
            ],
            labels=["School Name", "Acceptance Rate", "Size", "Cost of Attendance"],
        )

    @classmethod
    def get_name_field(cls) -> str:
        return "school_name"

    @classmethod
    def get_base_attributes(cls) -> List[str]:
        return [
            "school_name",
            "school_state",
            "latest_student_size",
            "latest_cost_attendance_academic_year",
            "id",
        ]

    # the weird method-level import here is necessary to prevent a circular dependency
    @classmethod
    def get_image_class(cls):
        from idb_app.models import UniversityImage

        return UniversityImage

    def get_template(self):
        for property in self:
            if self[property] == 0:
                self[property] = "NA"
            if isinstance(self[property], float):
                self[property] = round(float(self[property] * 100), 4)
        self.majors_cip = [
            list(set(self.majors_cip))[i : i + 2]
            for i in range(0, len(list(set(self.majors_cip))), 2)
        ]
        return render_template(
            "university_instance.html",
            university_name=self.school_name.replace("_", " ").title(),
            university=self,
            city_name=str(self.school_city),
            encode=urllib.parse.quote_plus,
        )
