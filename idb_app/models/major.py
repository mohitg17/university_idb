from mongoengine import Document
from mongoengine.fields import StringField, IntField


class Major(Document):
    name = StringField(required=True, unique=True)
    # would be "science" or "social studies" or "engineering", etc. Exact choices we use depend on data set
    # major_type = StringField(required=True)
    median_starting_salary = IntField(required=True, min_value=0)
    median_midcareer_salary = IntField(required=True, min_value=0)
    num_certificate_programs = IntField(required=True, min_value=0)
    num_associate_programs = IntField(required=True, min_value=0)
    num_bachelor_programs = IntField(required=True, min_value=0)
    cip_code = StringField()
    earnings_weighted_sum = IntField(min_value=0)
    earnings_count = IntField(min_value=0)
