from idb_app.bases import AbstractBase
from idb_app.models import Major
from flask import url_for


class MajorBase(AbstractBase):
    title = "Fields of Study & Majors"
    model_type = type = "major"
    filter_buttons = Major.get_filtering_buttons()
    filter_text = Major.get_filtering_text()
    sort_buttons = Major.get_sort_buttons()

    def build_instances(self, query_set):
        instances = []
        for major in query_set:
            instance = {
                "model_type": "major",
                "page_url": url_for("instance", model_name="major", object_id=major.id),
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
            instances.append(instance)
        return instances
