from mongoengine import Document, DENY
from mongoengine.fields import StringField, IntField, ReferenceField, ListField

from idb_app.models import City, Major, choices


# TODO update these fields as needed based on the info in the CollegeScorecard data dictionary 
class University(Document):
    name = StringField(required=True, unique=True)
    location = ReferenceField(City, reverse_delete_rule=DENY, required=True)
    majors_offered = ListField(ReferenceField(Major, reverse_delete_rule=DENY), required=True)
    highest_degree_offered = StringField(choices=choices.DEGREE_CHOICES)
    endowment = IntField(min_value=0)
    undergrad_population = IntField(min_value=0)
    faculty_population = IntField(min_value=0)
    # may be hard to get; not every US school is in the rankings
    usn_ranking = IntField(min_value=1)
