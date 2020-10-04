from mongoengine import Document
from mongoengine.fields import StringField


class Major(Document):
    name = StringField(required=True, unique=True)
    # would be "science" or "social studies" or "engineering", etc. Exact choices we use depend on data set
    major_type = StringField(required=True)
