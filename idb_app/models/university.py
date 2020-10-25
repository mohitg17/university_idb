from mongoengine import Document, DENY
from mongoengine.fields import StringField, IntField, ReferenceField, ListField, FloatField, URLField

from idb_app.models import City, Major, choices


class University(Document):
    school_name = StringField(required=True, unique=True)
    school_city = ReferenceField(City, reverse_delete_rule=DENY, required=True)
    school_state = StringField(required=True, choices=choices.STATE_CHOICES, unique=True)
    school_locale = StringField(required=True, unique=True)
    majors_offered = ListField(
        ReferenceField(Major, reverse_delete_rule=DENY), required=True
    )
    latest_student_size = IntField(required=True, min_value=0)
    latest_admissions_admission_rate_overall = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_cost_tuition_in_state = IntField(required=True, min_value=0)
    latest_cost_tuition_out_of_state = IntField(required=True, min_value=0)
    school_school_url = URLField(required=True)
    latest_admissions_sat_scores_average_overall = IntField(required=True)
    latest_admissions_act_scores_midpoint_cumulative = IntField(required=True)
    latest_student_demographics_race_ethnicity_black = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_student_demographics_race_ethnicity_white = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_student_demographics_race_ethnicity_asian = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_student_demographics_race_ethnicity_hispanic = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_student_demographics_men = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_student_demographics_women = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_aid_median_debt_completers_overall = IntField(required=True)
    latest_cost_attendance_academic_year = IntField(required=True)
    school_degrees_awarded_predominant = StringField(required=True, choices=choices.DEGREE_CHOICES)
    school_degrees_awarded_highest = StringField(required=True, choices=choices.DEGREE_CHOICES)
    latest_completion_4_yr_completion_overall = IntField(required=True, min_value=0.0, max_value=20000)
    latest_completion_completion_rate_4yr_150_white = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_completion_completion_rate_4yr_150_black = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_completion_completion_rate_4yr_150_asian = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_completion_completion_rate_4yr_150_hispanic = FloatField(required=True, min_value=0.0, max_value=100.0)
    latest_earnings_10_yrs_after_entry_median = IntField(required=True, min_value=0)
    latest_student_retention_rate_four_year_full_time = FloatField(required=True, min_value=0.0, max_value=100.0)