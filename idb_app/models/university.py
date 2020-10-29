from mongoengine import Document, DENY
from mongoengine.fields import StringField, IntField, ReferenceField, ListField, FloatField, URLField

from idb_app.models import City, Major, choices


class University(Document):
    school_name = StringField(required=True, unique_with=['school_city', 'school_state'])
    school_city = ReferenceField(City, reverse_delete_rule=DENY, required=True)
    school_state = StringField(required=True, choices=choices.STATE_CHOICES)
    school_locale = StringField(default="City")
    majors_offered = ListField(
        ReferenceField(Major, reverse_delete_rule=DENY), default=[]
    )
    latest_student_size = IntField(default=0, min_value=0)
    latest_admissions_admission_rate_overall = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_cost_tuition_in_state = IntField(default=0, min_value=0)
    latest_cost_tuition_out_of_state = IntField(default=0, min_value=0)
    school_school_url = StringField(required=True)
    latest_admissions_sat_scores_average_overall = IntField(default=0)
    latest_admissions_act_scores_midpoint_cumulative = IntField(default=0)
    latest_student_demographics_race_ethnicity_black = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_student_demographics_race_ethnicity_white = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_student_demographics_race_ethnicity_asian = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_student_demographics_race_ethnicity_hispanic = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_student_demographics_men = FloatField(default=0, min_value=0.0, max_value=100.0)
    latest_student_demographics_women = FloatField(default=0, min_value=0.0, max_value=100.0)
    latest_aid_median_debt_completers_overall = IntField(default=0)
    latest_cost_attendance_academic_year = IntField(default=0)
    school_degrees_awarded_predominant = StringField(required=True, choices=choices.DEGREE_CHOICES)
    school_degrees_awarded_highest = StringField(required=True, choices=choices.DEGREE_CHOICES)
    latest_completion_4_yr_completion_overall = IntField(default=0, min_value=0)
    latest_completion_completion_rate_4yr_150_white = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_completion_completion_rate_4yr_150_black = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_completion_completion_rate_4yr_150_asian = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_completion_completion_rate_4yr_150_hispanic = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    latest_earnings_10_yrs_after_entry_median = IntField(default=0, min_value=0)
    latest_student_retention_rate_four_year_full_time = FloatField(default=0.0, min_value=0.0, max_value=100.0)
    doe_id = IntField()
    latitude = FloatField()
    longitude = FloatField()
    majors_cip = ListField(
        ReferenceField(Major, reverse_delete_rule=DENY), default=[]
    )