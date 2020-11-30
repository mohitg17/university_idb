from idb_app.bases import AbstractBase
from idb_app.models import University
from flask import url_for


class UniversityBase(AbstractBase):
    title = "Universities"
    model_type = type = "university"
    filter_buttons = University.get_filtering_buttons()
    filter_text = University.get_filtering_text()
    sort_buttons = University.get_sort_buttons()

    def build_instances(self, query_set):
        instances = []
        for university in query_set:
            instance = {
                "model_type": "university",
                "page_url": url_for(
                    "instance", model_name="university", object_id=university.id
                ),
                "image_url": url_for(
                    "static",
                    filename=(university.school_name.replace("_", " ") + ".jpg"),
                ),
                "name": university.school_name.replace("_", " ").title(),
                "id": university.id,
                "attribute_1": {"name": "State", "value": university.school_state},
                "attribute_2": {
                    "name": "Student Population",
                    "value": university.latest_student_size,
                },
                "attribute_3": {
                    "name": "Cost of Attendance",
                    "value": university.latest_cost_attendance_academic_year
                    if university.latest_cost_attendance_academic_year
                    else "Unavailable",
                },
            }
            instances.append(instance)
        return instances
