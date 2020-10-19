from mongoengine import Document, DENY
from mongoengine.fields import StringField, IntField, ReferenceField, ListField, FloatField, URLField

from idb_app.models import City, Major, choices


class University(Document):
    name = StringField(required=True, unique=True)
    location = ReferenceField(City, reverse_delete_rule=DENY, required=True)
    majors_offered = ListField(
        ReferenceField(Major, reverse_delete_rule=DENY), required=True
    )
    student_population = IntField(required=True, min_value=0)
    acceptance_rate = FloatField(required=True, min_value=0.0, max_value=100.0)
    in_state_tuition = IntField(required=True, min_value=0)
    out_of_state_tuition = IntField(required=True, min_value=0)
    website = URLField(required=True)
    sat_median = IntField(required=True)
    act_median = IntField(required=True)
    percent_black = FloatField(required=True, min_value=0.0, max_value=100.0)
    percent_white = FloatField(required=True, min_value=0.0, max_value=100.0)
    percent_asian = FloatField(required=True, min_value=0.0, max_value=100.0)
    percent_hispanic = FloatField(required=True, min_value=0.0, max_value=100.0)
    percent_male = FloatField(required=True, min_value=0.0, max_value=100.0)
    percent_female = FloatField(required=True, min_value=0.0, max_value=100.0)
    median_debt = IntField(required=True)
    avg_cost = IntField(required=True)
    predominant_degree = StringField(required=True, choices=choices.DEGREE_CHOICES)
    highest_degree = StringField(required=True, choices=choices.DEGREE_CHOICES)
    completion_overall = FloatField(required=True, min_value=0.0, max_value=100.0)
    completion_rate_black = FloatField(required=True, min_value=0.0, max_value=100.0)
    completion_rate_asian = FloatField(required=True, min_value=0.0, max_value=100.0)
    completion_rate_hispanic = FloatField(required=True, min_value=0.0, max_value=100.0)
    earnings = IntField(required=True, min_value=0)
    retention_rate = FloatField(required=True, min_value=0.0, max_value=100.0)
