from mongoengine import Document
from mongoengine.fields import StringField, IntField


class Major(Document):
    name = StringField(required=True, unique=True)
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
    earnings_weighted_sum = IntField(default=0)
    earnings_count = IntField(default=0)
    program_count_estimate = IntField(default=0)

    def average_earnings(self):
        if self.earnings_count == 0:
            return 0
        else:
            return self.earnings_weighted_sum / self.earnings_count

    # TODO - replace this approximation once we have more data
    def average_mid_earnings(self):
        return 1.6 * self.average_earnings()

    # assumes the callee will .save()
    @classmethod
    def get_or_create(cls, cip_code: int, title: str):
        created = cls.objects(cip_code=cip_code).first()
        if created is None:
            created = cls.objects(name=title).first()
        if created is None:
            created = cls(cip_code=cip_code, name=title, earnings_weighted_sum=0, earnings_count=0)
            # created.save()
        return created

